"""
Brand Analyzer — scrapes website + Instagram, extracts visual DNA.

Pipeline:
  1. Fetch homepage HTML → extract colors, logo, text, social links
  2. Download logo/favicon → extract dominant colors via Pillow
  3. If Instagram found → fetch profile page → download recent posts → GPT-4o-mini vision analysis
  4. Merge scraped data with stored brand profile (if we have one in the 499 dataset)
  5. Send all data to GPT-4o for final comprehensive brand analysis
  6. Fallback chain: GPT-4o guess → stored profile → safe defaults
"""
from __future__ import annotations

import base64
import io
import json
import logging
import re
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 10.0
_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]


# ── 1. Website Scraping ────────────────────────────────────────────────

def _fetch_html(url: str) -> str | None:
    """Fetch a URL's HTML, trying multiple User-Agent headers."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    for ua in _USER_AGENTS:
        try:
            r = httpx.get(
                url,
                headers={"User-Agent": ua},
                timeout=HTTP_TIMEOUT,
                follow_redirects=True,
            )
            if r.status_code == 200:
                return r.text
            logger.debug("Got %d for %s with UA %s", r.status_code, url, ua[:30])
        except Exception as e:
            logger.debug("Fetch failed for %s: %s", url, e)
    return None


def _extract_website_data(html: str, base_url: str) -> dict[str, Any]:
    """Extract brand signals from homepage HTML."""
    soup = BeautifulSoup(html, "html.parser")

    data: dict[str, Any] = {}

    # Title and meta description
    title_tag = soup.find("title")
    data["page_title"] = title_tag.get_text(strip=True) if title_tag else ""

    meta_desc = soup.find("meta", attrs={"name": "description"})
    data["meta_description"] = meta_desc.get("content", "") if meta_desc else ""

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc:
        data["og_description"] = og_desc.get("content", "")

    # Colors from inline styles and style tags
    data["css_colors"] = _extract_css_colors(html)

    # Logo URL
    data["logo_url"] = _find_logo_url(soup, base_url)

    # Favicon URL
    data["favicon_url"] = _find_favicon_url(soup, base_url)

    # Social media links
    data["social_links"] = _extract_social_links(soup)

    # Hero/key text content
    data["key_text"] = _extract_key_text(soup)

    return data


def _extract_css_colors(html: str) -> list[str]:
    """Extract hex color codes from CSS in the HTML."""
    hex_pattern = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
    matches = hex_pattern.findall(html)

    # Normalize 3-char to 6-char hex
    normalized = set()
    for c in matches:
        c = c.upper()
        if len(c) == 4:  # #RGB → #RRGGBB
            c = f"#{c[1]*2}{c[2]*2}{c[3]*2}"
        normalized.add(c)

    # Remove very common/boring colors
    boring = {"#FFFFFF", "#000000", "#FFF", "#000", "#333333", "#666666", "#999999", "#CCCCCC"}
    filtered = [c for c in normalized if c not in boring]

    # Return most common first (via count in original matches)
    counts = {}
    for c in matches:
        c = c.upper()
        if len(c) == 4:
            c = f"#{c[1]*2}{c[2]*2}{c[3]*2}"
        if c not in boring:
            counts[c] = counts.get(c, 0) + 1

    return sorted(counts, key=lambda x: counts[x], reverse=True)[:15]


def _find_logo_url(soup: BeautifulSoup, base_url: str) -> str | None:
    """Find logo image URL by checking common patterns."""
    # Check <img> tags with "logo" in src, alt, class, or id
    for img in soup.find_all("img"):
        attrs_text = " ".join([
            str(img.get("src", "")),
            str(img.get("alt", "")),
            " ".join(img.get("class", [])) if isinstance(img.get("class"), list) else str(img.get("class", "")),
            str(img.get("id", "")),
        ]).lower()
        if "logo" in attrs_text:
            src = img.get("src", "")
            if src:
                return urljoin(base_url, src)

    # Check SVG with "logo" in class/id
    for svg in soup.find_all("svg"):
        attrs_text = " ".join([
            " ".join(svg.get("class", [])) if isinstance(svg.get("class"), list) else str(svg.get("class", "")),
            str(svg.get("id", "")),
        ]).lower()
        if "logo" in attrs_text:
            return None  # SVG inline, can't download

    # Check <link> with rel="icon" or "apple-touch-icon"
    for link in soup.find_all("link", rel=True):
        rels = link.get("rel", [])
        if isinstance(rels, list):
            rels_str = " ".join(rels)
        else:
            rels_str = str(rels)
        if "icon" in rels_str and link.get("href"):
            return urljoin(base_url, link["href"])

    return None


def _find_favicon_url(soup: BeautifulSoup, base_url: str) -> str | None:
    """Find favicon URL."""
    for link in soup.find_all("link", rel=True):
        rels = link.get("rel", [])
        rels_str = " ".join(rels) if isinstance(rels, list) else str(rels)
        if ("icon" in rels_str or "shortcut" in rels_str) and link.get("href"):
            href = link["href"]
            # Prefer apple-touch-icon (larger, better for color extraction)
            if "apple-touch" in rels_str:
                return urljoin(base_url, href)
    # Fallback: try standard paths
    for link in soup.find_all("link", rel=True):
        rels = link.get("rel", [])
        rels_str = " ".join(rels) if isinstance(rels, list) else str(rels)
        if "icon" in rels_str and link.get("href"):
            return urljoin(base_url, link["href"])
    return urljoin(base_url, "/favicon.ico")


def _extract_social_links(soup: BeautifulSoup) -> dict[str, str]:
    """Extract social media profile URLs from the page."""
    social_domains = {
        "instagram.com": "instagram",
        "facebook.com": "facebook",
        "twitter.com": "twitter",
        "x.com": "twitter",
        "linkedin.com": "linkedin",
        "tiktok.com": "tiktok",
        "youtube.com": "youtube",
        "pinterest.com": "pinterest",
    }

    links: dict[str, str] = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        for domain, platform in social_domains.items():
            if domain in href and platform not in links:
                links[platform] = href
    return links


def _extract_key_text(soup: BeautifulSoup) -> list[str]:
    """Extract hero text, taglines, and prominent text."""
    texts: list[str] = []

    # h1, h2 tags (often hero text)
    for tag in soup.find_all(["h1", "h2"], limit=5):
        text = tag.get_text(strip=True)
        if text and len(text) > 3 and len(text) < 200:
            texts.append(text)

    # Meta og:title
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        texts.append(og_title["content"])

    return texts[:8]


# ── 2. Image Color Extraction ──────────────────────────────────────────

def _download_image(url: str) -> bytes | None:
    """Download an image, return raw bytes or None."""
    try:
        r = httpx.get(
            url,
            headers={"User-Agent": _USER_AGENTS[0]},
            timeout=HTTP_TIMEOUT,
            follow_redirects=True,
        )
        if r.status_code == 200 and len(r.content) > 100:
            return r.content
    except Exception as e:
        logger.debug("Image download failed for %s: %s", url, e)
    return None


def _extract_dominant_colors(image_bytes: bytes, n_colors: int = 5) -> list[str]:
    """Extract dominant colors from image using Pillow quantization."""
    try:
        from PIL import Image

        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert("RGB")
        # Resize for speed
        img = img.resize((150, 150))
        # Quantize to n_colors
        quantized = img.quantize(colors=n_colors, method=0)
        palette = quantized.getpalette()
        if not palette:
            return []

        colors: list[str] = []
        for i in range(n_colors):
            r, g, b = palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]
            hex_color = f"#{r:02X}{g:02X}{b:02X}"
            colors.append(hex_color)
        return colors
    except Exception as e:
        logger.debug("Color extraction failed: %s", e)
        return []


# ── 3. Instagram Scraping ──────────────────────────────────────────────

def _scrape_instagram(instagram_url: str) -> dict[str, Any] | None:
    """Scrape public Instagram profile page for brand signals."""
    try:
        html = _fetch_html(instagram_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        data: dict[str, Any] = {}

        # Profile name from og:title
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title:
            data["profile_name"] = og_title.get("content", "")

        # Bio from description
        meta_desc = soup.find("meta", attrs={"property": "og:description"})
        if meta_desc:
            data["bio"] = meta_desc.get("content", "")

        # Profile picture from og:image
        og_image = soup.find("meta", attrs={"property": "og:image"})
        if og_image:
            data["profile_picture_url"] = og_image.get("content", "")

        # Try to find post image URLs from meta tags or JSON-LD
        post_images: list[str] = []
        for meta in soup.find_all("meta", attrs={"property": "og:image"}):
            url = meta.get("content", "")
            if url and url not in post_images:
                post_images.append(url)

        data["post_image_urls"] = post_images[:5]

        return data if data else None
    except Exception as e:
        logger.debug("Instagram scraping failed: %s", e)
        return None


def _analyze_instagram_images(
    image_urls: list[str],
    openai_api_key: str,
) -> dict[str, Any] | None:
    """Download Instagram images and analyze with GPT-4o-mini vision."""
    if not image_urls or not openai_api_key:
        return None

    # Download up to 3 images
    image_data: list[dict[str, Any]] = []
    for url in image_urls[:3]:
        img_bytes = _download_image(url)
        if img_bytes:
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            image_data.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "low"},
            })

    if not image_data:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": (
                "You are a brand visual analyst. Analyze these Instagram posts from a brand. "
                "Extract and return JSON with: dominant_colors (list of 5 hex codes), "
                "photography_style (description), lighting_preference (description), "
                "mood (description), composition_style (description), "
                "content_type (product/lifestyle/editorial/mixed)."
            )},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze these brand Instagram posts:"},
                *image_data,
            ]},
        ]

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"},
            messages=messages,
        )
        return json.loads(resp.choices[0].message.content or "{}")
    except Exception as e:
        logger.warning("Instagram image analysis failed: %s", e)
        return None


# ── 4. Stored Profile Lookup ───────────────────────────────────────────

def _get_stored_profile(brand_name: str) -> dict[str, Any] | None:
    """Look up brand in the 499 stored profiles."""
    try:
        from load_dataset import DatasetLoader
        ds = DatasetLoader()
        return ds.get_brand_profile(brand_name)
    except Exception:
        return None


# ── 5. GPT-4o Final Analysis ───────────────────────────────────────────

def _gpt4o_brand_analysis(
    url: str,
    brand_name: str,
    website_data: dict[str, Any] | None,
    logo_colors: list[str],
    instagram_analysis: dict[str, Any] | None,
    stored_profile: dict[str, Any] | None,
    openai_api_key: str,
) -> dict[str, Any]:
    """Send all collected data to GPT-4o for comprehensive analysis."""
    from openai import OpenAI

    # Build the context from all sources
    context_parts: list[str] = []
    context_parts.append(f"Brand URL: {url}")
    context_parts.append(f"Extracted brand name: {brand_name}")

    if website_data:
        context_parts.append(f"Page title: {website_data.get('page_title', '')}")
        context_parts.append(f"Meta description: {website_data.get('meta_description', '')}")
        if website_data.get("og_description"):
            context_parts.append(f"OG description: {website_data['og_description']}")
        if website_data.get("css_colors"):
            context_parts.append(f"Colors found in CSS: {website_data['css_colors'][:10]}")
        if website_data.get("key_text"):
            context_parts.append(f"Key text from website: {website_data['key_text']}")
        if website_data.get("social_links"):
            context_parts.append(f"Social media: {list(website_data['social_links'].keys())}")

    if logo_colors:
        context_parts.append(f"Dominant colors from logo/favicon: {logo_colors}")

    if instagram_analysis:
        context_parts.append(f"Instagram visual analysis: {json.dumps(instagram_analysis)}")

    if stored_profile:
        vi = stored_profile.get("visual_identity", {})
        photo = stored_profile.get("photography_dna", {})
        context_parts.append(
            f"Known brand profile — industry: {stored_profile.get('industry', '')}, "
            f"brand_essence: {stored_profile.get('brand_essence', '')}, "
            f"primary_colors: {vi.get('primary_colors', [])}, "
            f"prompt_prefix: {stored_profile.get('prompt_prefix', '')}"
        )
        if photo:
            context_parts.append(f"Photography DNA: {json.dumps(photo)}")

    context = "\n".join(context_parts)

    system_prompt = (
        "You are a senior brand strategist and creative director specializing in "
        "advertising photography. Analyze ALL the data provided about this brand "
        "and return a comprehensive visual identity analysis.\n\n"
        "Return JSON with exactly these keys:\n"
        "{\n"
        '  "brand_name": "official brand name",\n'
        '  "website_url": "the URL",\n'
        '  "instagram_handle": "@handle or null",\n'
        '  "industry": "one of: luxury, beauty, fragrance, jewelry_watches, fashion, '
        'automotive, sport, food_beverage, tech, travel, real_estate, home_design",\n'
        '  "visual_identity": {\n'
        '    "primary_colors": ["#hex1", "#hex2", "#hex3"],\n'
        '    "secondary_colors": ["#hex4", "#hex5"],\n'
        '    "color_mood": "warm|cool|neutral|vibrant",\n'
        '    "typography_style": "serif|sans-serif|mixed",\n'
        '    "overall_aesthetic": "minimalist|maximalist|classic|modern|avant-garde"\n'
        '  },\n'
        '  "photography_dna": {\n'
        '    "lighting_style": "description of preferred lighting",\n'
        '    "color_grading": "description of color grading style",\n'
        '    "composition_style": "description of composition preferences",\n'
        '    "retouching_level": "natural|polished|heavy"\n'
        '  },\n'
        '  "prompt_prefix": "2-3 sentences to prepend to ALL image generation prompts '
        'for this brand, capturing their exact visual DNA",\n'
        '  "mood_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],\n'
        '  "tone": "1-2 sentence description of brand tone and personality",\n'
        '  "confidence": 0.0 to 1.0\n'
        "}\n\n"
        "Use REAL brand colors based on your knowledge. If CSS colors and logo colors "
        "are provided, cross-reference them with your knowledge. For well-known brands, "
        "your knowledge of their official brand guidelines should take priority over "
        "noisy CSS colors."
    )

    client = OpenAI(api_key=openai_api_key)
    resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=2048,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
    )
    return json.loads(resp.choices[0].message.content or "{}")


# ── 6. Public API ──────────────────────────────────────────────────────

def analyze_brand(url: str, openai_api_key: str) -> dict[str, Any]:
    """Full brand analysis pipeline.

    Args:
        url: Brand website URL (e.g. "https://www.chanel.com").
        openai_api_key: OpenAI API key for GPT-4o calls.

    Returns:
        Comprehensive brand analysis dict. Never raises — always returns
        something useful.
    """
    # Normalize URL
    clean_url = url.strip()
    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    # Extract brand name from domain
    parsed = urlparse(clean_url)
    hostname = parsed.hostname or ""
    brand_name = hostname.replace("www.", "").split(".")[0].capitalize()

    logger.info("Analyzing brand: %s (from %s)", brand_name, clean_url)

    # Step 1: Fetch and parse homepage
    website_data: dict[str, Any] | None = None
    html = _fetch_html(clean_url)
    if html:
        website_data = _extract_website_data(html, clean_url)
        logger.info(
            "Website scraped: title=%s, colors=%d, social=%s",
            website_data.get("page_title", "")[:40],
            len(website_data.get("css_colors", [])),
            list(website_data.get("social_links", {}).keys()),
        )
    else:
        logger.warning("Could not fetch website: %s", clean_url)

    # Step 2: Extract colors from logo/favicon
    logo_colors: list[str] = []
    if website_data:
        for img_url in [website_data.get("logo_url"), website_data.get("favicon_url")]:
            if img_url and not logo_colors:
                img_bytes = _download_image(img_url)
                if img_bytes:
                    logo_colors = _extract_dominant_colors(img_bytes)
                    logger.info("Extracted %d colors from %s", len(logo_colors), img_url[:60])

    # Step 3: Instagram analysis
    instagram_analysis: dict[str, Any] | None = None
    ig_url = (website_data or {}).get("social_links", {}).get("instagram")
    if ig_url:
        logger.info("Found Instagram: %s", ig_url)
        ig_data = _scrape_instagram(ig_url)
        if ig_data and ig_data.get("post_image_urls"):
            instagram_analysis = _analyze_instagram_images(
                ig_data["post_image_urls"], openai_api_key,
            )
            if instagram_analysis:
                # Add the handle
                if ig_data.get("profile_name"):
                    instagram_analysis["profile_name"] = ig_data["profile_name"]
                logger.info("Instagram analysis complete: %d colors extracted",
                            len(instagram_analysis.get("dominant_colors", [])))

    # Step 4: Check stored brand profiles
    stored_profile = _get_stored_profile(brand_name)
    if stored_profile:
        logger.info("Found stored brand profile for %s", brand_name)

    # Step 5: GPT-4o comprehensive analysis
    try:
        result = _gpt4o_brand_analysis(
            url=clean_url,
            brand_name=brand_name,
            website_data=website_data,
            logo_colors=logo_colors,
            instagram_analysis=instagram_analysis,
            stored_profile=stored_profile,
            openai_api_key=openai_api_key,
        )
        logger.info("GPT-4o brand analysis complete for %s", brand_name)
    except Exception as e:
        logger.warning("GPT-4o brand analysis failed: %s — building fallback", e)
        result = _build_fallback(brand_name, clean_url, website_data, logo_colors, stored_profile)

    # Ensure required fields
    result.setdefault("brand_name", brand_name)
    result.setdefault("website_url", clean_url)
    result.setdefault("industry", "luxury")
    result.setdefault("confidence", 0.5)

    # Merge stored profile data if GPT-4o missed it
    if stored_profile:
        _merge_stored_profile(result, stored_profile)

    # Add frontend-compatible fields
    result["colors"] = (
        result.get("visual_identity", {}).get("primary_colors", [])
        + result.get("visual_identity", {}).get("secondary_colors", [])
    )
    result.setdefault("keywords", result.get("mood_keywords", []))
    result.setdefault("tone", "")

    # Add scraping metadata
    result["_sources"] = {
        "website_scraped": website_data is not None,
        "logo_colors_extracted": len(logo_colors) > 0,
        "instagram_analyzed": instagram_analysis is not None,
        "stored_profile_found": stored_profile is not None,
    }

    return result


def _build_fallback(
    brand_name: str,
    url: str,
    website_data: dict[str, Any] | None,
    logo_colors: list[str],
    stored_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a fallback result when GPT-4o fails."""
    result: dict[str, Any] = {
        "brand_name": brand_name,
        "website_url": url,
        "instagram_handle": None,
        "industry": "luxury",
        "visual_identity": {
            "primary_colors": logo_colors[:3] or ["#1A1A1A", "#C4A265", "#FFFFFF"],
            "secondary_colors": logo_colors[3:5] or ["#8B7355", "#F5F0EB"],
            "color_mood": "neutral",
            "typography_style": "sans-serif",
            "overall_aesthetic": "minimalist",
        },
        "photography_dna": {
            "lighting_style": "Soft studio lighting with golden accents",
            "color_grading": "Warm, desaturated tones with rich shadows",
            "composition_style": "Clean, centered compositions with negative space",
            "retouching_level": "polished",
        },
        "prompt_prefix": f"Create a visual in the style of {brand_name}, emphasizing elegance and sophistication.",
        "mood_keywords": ["elegant", "sophisticated", "refined", "timeless", "exclusive"],
        "tone": "Sophisticated and timeless luxury",
        "confidence": 0.3,
    }

    if website_data and website_data.get("css_colors"):
        result["visual_identity"]["primary_colors"] = website_data["css_colors"][:3] or result["visual_identity"]["primary_colors"]

    return result


def _merge_stored_profile(result: dict[str, Any], stored_profile: dict[str, Any]) -> None:
    """Merge stored brand profile data into the GPT-4o result."""
    vi = stored_profile.get("visual_identity", {})
    photo = stored_profile.get("photography_dna", {})

    # Stored colors override if GPT-4o used generic ones
    if vi.get("primary_colors"):
        result.setdefault("visual_identity", {})
        result["visual_identity"]["primary_colors"] = vi["primary_colors"]
    if vi.get("secondary_colors"):
        result.setdefault("visual_identity", {})
        result["visual_identity"]["secondary_colors"] = vi["secondary_colors"]

    # Photography DNA from stored profile
    if photo.get("lighting_style"):
        result.setdefault("photography_dna", {})
        result["photography_dna"].setdefault("lighting_style", photo["lighting_style"])

    # Prompt prefix — stored profile's is usually better
    if stored_profile.get("prompt_prefix"):
        result["prompt_prefix"] = stored_profile["prompt_prefix"]

    # Mood keywords
    if stored_profile.get("mood_keywords"):
        result["mood_keywords"] = stored_profile["mood_keywords"]

    # Industry
    if stored_profile.get("industry"):
        result.setdefault("industry", stored_profile["industry"])
