"""
╔══════════════════════════════════════════════════════════════════════╗
║  AdGenAI — OpenAI Fine-Tuning Runner                                 ║
║                                                                      ║
║  1. Uploads dataset/finetuning/train.jsonl and val.jsonl             ║
║  2. Creates a fine-tuning job for gpt-4o-mini                        ║
║  3. Polls progress until the job finishes (or fails)                 ║
║  4. Writes FINETUNED_MODEL_ID=<id> to .env on success                ║
║                                                                      ║
║  Usage:                                                              ║
║    python3 run_finetuning.py                 # full pipeline         ║
║    python3 run_finetuning.py --upload-only   # just upload files     ║
║    python3 run_finetuning.py --job ftjob-... # attach to existing    ║
║    python3 run_finetuning.py --status                                ║
╚══════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_api_key = os.environ.get("OPENAI_API_KEY")
if not _api_key:
    print("❌ OPENAI_API_KEY is not set", file=sys.stderr)
    sys.exit(1)
client = OpenAI(api_key=_api_key)

FT_DIR = Path("dataset/finetuning")
TRAIN_PATH = FT_DIR / "train.jsonl"
VAL_PATH = FT_DIR / "val.jsonl"
STATE_PATH = FT_DIR / "_ft_state.json"
ENV_PATH = Path(".env")

BASE_MODEL = "gpt-4o-mini-2024-07-18"  # currently the cheapest FT-capable model
POLL_INTERVAL = 60  # seconds


def _load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def upload_files() -> tuple[str, str]:
    """Upload train + val JSONL. Returns (train_file_id, val_file_id)."""
    if not TRAIN_PATH.exists() or not VAL_PATH.exists():
        print(f"❌ Missing {TRAIN_PATH} or {VAL_PATH}. Run prepare_finetuning.py first.")
        sys.exit(1)

    state = _load_state()

    if state.get("train_file_id") and state.get("val_file_id"):
        print(f"ℹ️  Reusing uploaded files: {state['train_file_id']}, {state['val_file_id']}")
        return state["train_file_id"], state["val_file_id"]

    print(f"📤 Uploading {TRAIN_PATH}...")
    with TRAIN_PATH.open("rb") as f:
        train_file = client.files.create(file=f, purpose="fine-tune")
    print(f"   ✅ {train_file.id}")

    print(f"📤 Uploading {VAL_PATH}...")
    with VAL_PATH.open("rb") as f:
        val_file = client.files.create(file=f, purpose="fine-tune")
    print(f"   ✅ {val_file.id}")

    state["train_file_id"] = train_file.id
    state["val_file_id"] = val_file.id
    _save_state(state)
    return train_file.id, val_file.id


def create_job(train_file_id: str, val_file_id: str) -> str:
    state = _load_state()
    if state.get("job_id"):
        print(f"ℹ️  Reusing existing job: {state['job_id']}")
        return state["job_id"]

    print(f"🚀 Creating fine-tuning job on {BASE_MODEL}...")
    job = client.fine_tuning.jobs.create(
        training_file=train_file_id,
        validation_file=val_file_id,
        model=BASE_MODEL,
        suffix="astreli-scenario",
    )
    print(f"   ✅ {job.id}")

    state["job_id"] = job.id
    state["base_model"] = BASE_MODEL
    _save_state(state)
    return job.id


def poll(job_id: str) -> str | None:
    """Poll job status until terminal. Returns fine_tuned_model or None."""
    print(f"⏳ Polling job {job_id} every {POLL_INTERVAL}s...")
    last_status = None
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        if job.status != last_status:
            print(f"   [{time.strftime('%H:%M:%S')}] status: {job.status}")
            last_status = job.status

        if job.status == "succeeded":
            print(f"🎉 Finished. Fine-tuned model: {job.fine_tuned_model}")
            return job.fine_tuned_model
        if job.status in {"failed", "cancelled"}:
            print(f"❌ Job {job.status}: {getattr(job, 'error', None)}")
            return None

        time.sleep(POLL_INTERVAL)


def write_env_var(key: str, value: str) -> None:
    """Write or update KEY=VALUE in .env (preserves other lines)."""
    lines: list[str] = []
    if ENV_PATH.exists():
        lines = ENV_PATH.read_text().splitlines()

    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(lines) + "\n")
    print(f"📝 Wrote {key}={value} to {ENV_PATH}")


def status() -> None:
    state = _load_state()
    if not state:
        print("(no state — nothing to show)")
        return
    print(json.dumps(state, indent=2))
    job_id = state.get("job_id")
    if job_id:
        try:
            job = client.fine_tuning.jobs.retrieve(job_id)
            print(f"\nJob status: {job.status}")
            if job.fine_tuned_model:
                print(f"Fine-tuned model: {job.fine_tuned_model}")
        except Exception as e:
            print(f"(could not retrieve job: {e})")


def run_pipeline() -> None:
    train_id, val_id = upload_files()
    job_id = create_job(train_id, val_id)
    model_id = poll(job_id)

    if model_id:
        state = _load_state()
        state["fine_tuned_model"] = model_id
        _save_state(state)
        write_env_var("FINETUNED_MODEL_ID", model_id)
        print("\n✅ Pipeline complete. Restart the backend to pick up the new model.")
    else:
        print("\n❌ Pipeline did not produce a fine-tuned model. Check job logs.")


def attach(job_id: str) -> None:
    state = _load_state()
    state["job_id"] = job_id
    _save_state(state)
    model_id = poll(job_id)
    if model_id:
        state = _load_state()
        state["fine_tuned_model"] = model_id
        _save_state(state)
        write_env_var("FINETUNED_MODEL_ID", model_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OpenAI fine-tuning for Astreli")
    parser.add_argument("--upload-only", action="store_true", help="Upload files and stop")
    parser.add_argument("--job", help="Attach to an existing ftjob-... id")
    parser.add_argument("--status", action="store_true", help="Show current state")
    args = parser.parse_args()

    if args.status:
        status()
    elif args.upload_only:
        upload_files()
    elif args.job:
        attach(args.job)
    else:
        run_pipeline()


if __name__ == "__main__":
    main()
