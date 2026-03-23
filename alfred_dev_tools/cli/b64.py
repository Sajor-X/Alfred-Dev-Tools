import sys

from alfred_dev_tools.alfred import print_json
from alfred_dev_tools.features.b64 import build_results, usage_response


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if query.strip().lower() in {"help", "?"}:
        print_json(usage_response())
        return

    print_json(build_results(query))
