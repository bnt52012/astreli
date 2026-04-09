"""
Utility to load all generated data from the AdGenAI dataset into a unified,
queryable format.  Supports lazy loading with in-memory caching.

Usage:
    from load_dataset import DatasetLoader
    loader = DatasetLoader()
    loader.print_statistics()
"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


class DatasetLoader:
    """Loads and indexes the AdGenAI dataset for fast querying."""

    def __init__(self, base_path: str = "dataset/") -> None:
        self.base_path = Path(base_path)

        # Raw storage keyed by category
        self._scenarios: list[dict] | None = None
        self._storyboards: list[dict] | None = None
        self._brand_profiles: list[dict] | None = None
        self._performance: list[dict] | None = None

        # Indexes (built on first access)
        self._idx_scenarios_by_industry: dict[str, list[dict]] | None = None
        self._idx_storyboards_by_industry: dict[str, list[dict]] | None = None
        self._idx_storyboards_by_format: dict[str, list[dict]] | None = None
        self._idx_brands_by_name: dict[str, dict] | None = None
        self._idx_brands_by_industry: dict[str, list[dict]] | None = None
        self._idx_perf_by_platform: dict[str, list[dict]] | None = None
        self._idx_perf_by_industry: dict[str, list[dict]] | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_json(path: Path) -> dict | None:
        """Safely load a single JSON file, returning None on failure."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    @staticmethod
    def _collect_json_files(directory: Path) -> list[Path]:
        """Recursively collect all .json files under *directory*."""
        if not directory.is_dir():
            return []
        return sorted(
            p for p in directory.rglob("*.json")
            if not p.name.startswith("_")  # skip progress/meta files
        )

    def _load_all(self, directory: Path) -> list[dict]:
        """Load every JSON file under *directory*, skipping bad ones."""
        results: list[dict] = []
        for path in self._collect_json_files(directory):
            data = self._load_json(path)
            if data is not None:
                # Attach source path for traceability
                data.setdefault("_source_file", str(path))
                results.append(data)
        return results

    # ------------------------------------------------------------------
    # Lazy loaders
    # ------------------------------------------------------------------

    def _ensure_scenarios(self) -> list[dict]:
        if self._scenarios is None:
            self._scenarios = self._load_all(self.base_path / "scenarios")
        return self._scenarios

    def _ensure_storyboards(self) -> list[dict]:
        if self._storyboards is None:
            self._storyboards = self._load_all(self.base_path / "storyboards")
        return self._storyboards

    def _ensure_brand_profiles(self) -> list[dict]:
        if self._brand_profiles is None:
            self._brand_profiles = self._load_all(self.base_path / "brand_profiles")
        return self._brand_profiles

    def _ensure_performance(self) -> list[dict]:
        if self._performance is None:
            self._performance = self._load_all(self.base_path / "performance")
        return self._performance

    # ------------------------------------------------------------------
    # Index builders (called once per category on first query)
    # ------------------------------------------------------------------

    def _build_scenario_indexes(self) -> None:
        if self._idx_scenarios_by_industry is not None:
            return
        self._idx_scenarios_by_industry = defaultdict(list)
        for s in self._ensure_scenarios():
            industry = s.get("industry", "unknown").lower()
            self._idx_scenarios_by_industry[industry].append(s)

    def _build_storyboard_indexes(self) -> None:
        if self._idx_storyboards_by_industry is not None:
            return
        self._idx_storyboards_by_industry = defaultdict(list)
        self._idx_storyboards_by_format = defaultdict(list)
        for sb in self._ensure_storyboards():
            industry = sb.get("industry", "unknown").lower()
            self._idx_storyboards_by_industry[industry].append(sb)
            fmt = sb.get("format", sb.get("ad_format", "unknown")).lower()
            self._idx_storyboards_by_format[fmt].append(sb)

    def _build_brand_indexes(self) -> None:
        if self._idx_brands_by_name is not None:
            return
        self._idx_brands_by_name = {}
        self._idx_brands_by_industry = defaultdict(list)
        for bp in self._ensure_brand_profiles():
            name = bp.get("brand", bp.get("brand_name", "")).lower()
            if name:
                self._idx_brands_by_name[name] = bp
            industry = bp.get("industry", "unknown").lower()
            self._idx_brands_by_industry[industry].append(bp)

    def _build_performance_indexes(self) -> None:
        if self._idx_perf_by_platform is not None:
            return
        self._idx_perf_by_platform = defaultdict(list)
        self._idx_perf_by_industry = defaultdict(list)
        for p in self._ensure_performance():
            platform = p.get("platform", "unknown").lower()
            self._idx_perf_by_platform[platform].append(p)
            industry = p.get("industry", "unknown").lower()
            self._idx_perf_by_industry[industry].append(p)

    # ------------------------------------------------------------------
    # Public query API
    # ------------------------------------------------------------------

    def load_all(self) -> None:
        """Eagerly load all datasets and build all indexes."""
        self._ensure_scenarios()
        self._ensure_storyboards()
        self._ensure_brand_profiles()
        self._ensure_performance()
        self._build_scenario_indexes()
        self._build_storyboard_indexes()
        self._build_brand_indexes()
        self._build_performance_indexes()
        sc = len(self._scenarios or [])
        sb = len(self._storyboards or [])
        bp = len(self._brand_profiles or [])
        pf = len(self._performance or [])
        print(f"Loaded {sc} scenarios, {sb} storyboards, {bp} brand profiles, {pf} performance data")

    def get_similar_scenarios(
        self, industry: str, mode: str | None = None, n: int = 5
    ) -> list[dict]:
        """Return n example scenarios for the given industry and optional mode.

        Used as few-shot examples for GPT-4o RAG enrichment.
        """
        self._build_scenario_indexes()
        assert self._idx_scenarios_by_industry is not None
        pool = self._idx_scenarios_by_industry.get(industry.lower(), [])
        if mode:
            mode_lower = mode.lower()
            pool = [s for s in pool if s.get("mode", "").lower() == mode_lower]
        if not pool:
            # Fallback to luxury if industry not found
            pool = self._idx_scenarios_by_industry.get("luxury", [])
        import random
        if len(pool) <= n:
            return list(pool)
        return random.sample(pool, n)

    def get_industry_storyboards(self, industry: str, n: int = 3) -> list[dict]:
        """Return n example storyboards for the given industry.

        Used to show GPT-4o how ads in this industry are typically structured.
        """
        self._build_storyboard_indexes()
        assert self._idx_storyboards_by_industry is not None
        pool = self._idx_storyboards_by_industry.get(industry.lower(), [])
        if not pool:
            pool = self._idx_storyboards_by_industry.get("luxury", [])
        import random
        if len(pool) <= n:
            return list(pool)
        return random.sample(pool, n)

    def get_brand_profile(self, brand_name: str) -> dict | None:
        """Return the brand profile for *brand_name*, or None."""
        self._build_brand_indexes()
        assert self._idx_brands_by_name is not None
        return self._idx_brands_by_name.get(brand_name.lower())

    def get_all_brands(self, industry: str | None = None) -> list[dict]:
        """Return all brand profiles, optionally filtered by industry."""
        self._build_brand_indexes()
        assert self._idx_brands_by_industry is not None
        if industry is not None:
            return list(self._idx_brands_by_industry.get(industry.lower(), []))
        return list(self._ensure_brand_profiles())

    def get_scenarios_by_industry(self, industry: str, limit: int = 100) -> list[dict]:
        """Return up to *limit* scenarios for the given industry."""
        self._build_scenario_indexes()
        assert self._idx_scenarios_by_industry is not None
        return self._idx_scenarios_by_industry.get(industry.lower(), [])[:limit]

    def get_storyboards_by_industry(self, industry: str, limit: int = 50) -> list[dict]:
        """Return up to *limit* storyboards for the given industry."""
        self._build_storyboard_indexes()
        assert self._idx_storyboards_by_industry is not None
        return self._idx_storyboards_by_industry.get(industry.lower(), [])[:limit]

    def get_storyboard_by_format(
        self, format: str, industry: str | None = None
    ) -> list[dict]:
        """Return storyboards matching *format*, optionally filtered by industry."""
        self._build_storyboard_indexes()
        assert self._idx_storyboards_by_format is not None
        results = self._idx_storyboards_by_format.get(format.lower(), [])
        if industry is not None:
            ind = industry.lower()
            results = [r for r in results if r.get("industry", "").lower() == ind]
        return results

    def get_performance_by_platform(
        self, platform: str, limit: int = 100
    ) -> list[dict]:
        """Return up to *limit* performance records for *platform*."""
        self._build_performance_indexes()
        assert self._idx_perf_by_platform is not None
        return self._idx_perf_by_platform.get(platform.lower(), [])[:limit]

    def get_top_performing(
        self,
        platform: str | None = None,
        industry: str | None = None,
        top_pct: float = 0.25,
    ) -> list[dict]:
        """Return the top *top_pct* fraction of performance records.

        Records are ranked by a composite score derived from available
        numeric metrics (engagement_rate, ctr, conversion_rate, roas, etc.).
        """
        self._build_performance_indexes()
        assert self._idx_perf_by_platform is not None
        assert self._idx_perf_by_industry is not None

        # Select pool
        if platform is not None:
            pool = list(self._idx_perf_by_platform.get(platform.lower(), []))
        else:
            pool = list(self._ensure_performance())

        if industry is not None:
            ind = industry.lower()
            pool = [p for p in pool if p.get("industry", "").lower() == ind]

        if not pool:
            return []

        # Score each record using available numeric metrics
        score_keys = [
            "engagement_rate",
            "ctr",
            "click_through_rate",
            "conversion_rate",
            "roas",
            "view_rate",
            "completion_rate",
        ]

        def _score(rec: dict) -> float:
            total = 0.0
            for k in score_keys:
                v = rec.get(k)
                if isinstance(v, (int, float)):
                    total += float(v)
            return total

        pool.sort(key=_score, reverse=True)
        n = max(1, int(len(pool) * top_pct))
        return pool[:n]

    def get_performance_insights(
        self, industry: str, platform: str | None = None
    ) -> dict:
        """Return aggregated performance metrics for an industry.

        Returns a dict with keys: count, and for each numeric metric found,
        the mean, median, min, and max values.
        """
        self._build_performance_indexes()
        assert self._idx_perf_by_industry is not None

        records = list(self._idx_perf_by_industry.get(industry.lower(), []))
        if platform is not None:
            plat = platform.lower()
            records = [r for r in records if r.get("platform", "").lower() == plat]

        result: dict[str, Any] = {"count": len(records)}
        if not records:
            return result

        # Collect all numeric keys across records
        numeric_keys: set[str] = set()
        for r in records:
            for k, v in r.items():
                if isinstance(v, (int, float)) and not k.startswith("_"):
                    numeric_keys.add(k)

        for key in sorted(numeric_keys):
            vals = [
                float(r[key]) for r in records
                if isinstance(r.get(key), (int, float))
            ]
            if vals:
                result[key] = {
                    "mean": round(statistics.mean(vals), 4),
                    "median": round(statistics.median(vals), 4),
                    "min": round(min(vals), 4),
                    "max": round(max(vals), 4),
                }

        return result

    def search_scenarios(self, query: str, limit: int = 20) -> list[dict]:
        """Simple keyword search across scenario text fields."""
        q = query.lower()
        matches: list[dict] = []
        for s in self._ensure_scenarios():
            searchable = " ".join(
                str(s.get(k, ""))
                for k in (
                    "scenario_text",
                    "brand",
                    "product",
                    "campaign_name",
                    "mood",
                    "target_audience",
                    "industry",
                )
            ).lower()
            if q in searchable:
                matches.append(s)
                if len(matches) >= limit:
                    break
        return matches

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def print_statistics(self) -> None:
        """Print a summary of loaded dataset counts."""
        scenarios = self._ensure_scenarios()
        storyboards = self._ensure_storyboards()
        brands = self._ensure_brand_profiles()
        performance = self._ensure_performance()

        print("=" * 60)
        print("  AdGenAI Dataset Statistics")
        print("=" * 60)
        print(f"  Scenarios:       {len(scenarios):>8,}")
        print(f"  Storyboards:     {len(storyboards):>8,}")
        print(f"  Brand Profiles:  {len(brands):>8,}")
        print(f"  Performance:     {len(performance):>8,}")
        print("-" * 60)

        # Scenario breakdown by industry
        if scenarios:
            self._build_scenario_indexes()
            assert self._idx_scenarios_by_industry is not None
            print("  Scenarios by industry:")
            for ind in sorted(self._idx_scenarios_by_industry):
                count = len(self._idx_scenarios_by_industry[ind])
                print(f"    {ind:<25} {count:>6,}")
            # Breakdown by mode
            modes: dict[str, int] = defaultdict(int)
            for s in scenarios:
                modes[s.get("mode", "unknown")] += 1
            print("  Scenarios by mode:")
            for mode in sorted(modes):
                print(f"    {mode:<25} {modes[mode]:>6,}")
            print("-" * 60)

        # Storyboard breakdown
        if storyboards:
            self._build_storyboard_indexes()
            assert self._idx_storyboards_by_industry is not None
            print("  Storyboards by industry:")
            for ind in sorted(self._idx_storyboards_by_industry):
                count = len(self._idx_storyboards_by_industry[ind])
                print(f"    {ind:<25} {count:>6,}")
            print("-" * 60)

        # Brand breakdown
        if brands:
            self._build_brand_indexes()
            assert self._idx_brands_by_industry is not None
            print("  Brand Profiles by industry:")
            for ind in sorted(self._idx_brands_by_industry):
                count = len(self._idx_brands_by_industry[ind])
                print(f"    {ind:<25} {count:>6,}")
            print("-" * 60)

        # Performance breakdown
        if performance:
            self._build_performance_indexes()
            assert self._idx_perf_by_platform is not None
            print("  Performance by platform:")
            for plat in sorted(self._idx_perf_by_platform):
                count = len(self._idx_perf_by_platform[plat])
                print(f"    {plat:<25} {count:>6,}")
            print("-" * 60)

        print("=" * 60)


# ======================================================================
# CLI entry point
# ======================================================================

if __name__ == "__main__":
    loader = DatasetLoader()
    loader.print_statistics()

    print("\n--- Example Queries ---\n")

    # Example: scenarios for a specific industry
    fashion = loader.get_scenarios_by_industry("fashion", limit=3)
    print(f"Fashion scenarios (first 3 of {len(loader.get_scenarios_by_industry('fashion', limit=999999))}): ")
    for s in fashion:
        print(f"  - [{s.get('brand')}] {s.get('campaign_name')} ({s.get('mode')})")

    # Example: keyword search
    print()
    results = loader.search_scenarios("sunset", limit=5)
    print(f"Scenarios matching 'sunset': {len(results)} found")
    for s in results:
        print(f"  - [{s.get('brand')}] {s.get('campaign_name')}")

    # Example: brand profile lookup
    print()
    bp = loader.get_brand_profile("gucci")
    if bp:
        print(f"Brand profile found: {bp.get('brand')} ({bp.get('industry')})")
    else:
        print("No brand profile for 'gucci' (brand_profiles/ may not exist yet)")

    # Example: top performing
    print()
    top = loader.get_top_performing(top_pct=0.1)
    print(f"Top 10% performance records: {len(top)}")
