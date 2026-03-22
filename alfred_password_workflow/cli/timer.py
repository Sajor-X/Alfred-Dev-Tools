import subprocess
import sys
from pathlib import Path

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.timer import (
    format_duration,
    parse_query,
    usage_response,
)


def start_worker(seconds, message):
    project_root = Path(__file__).resolve().parents[2]
    worker = project_root / "timer_worker.py"
    subprocess.Popen(
        [sys.executable, str(worker), str(seconds), message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        seconds, message = parse_query(query)
        print_json({"seconds": seconds, "message": message})
        return

    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if query.strip().lower() in {"help", "?"}:
        print_json(usage_response())
        return

    seconds, message = parse_query(query)
    start_worker(seconds, message)
    print(f"Timer set for {format_duration(seconds)}: {message}")
