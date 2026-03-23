import sys

from alfred_dev_tools.alfred import print_json
from alfred_dev_tools.features.jsonfmt import build_result, parse_query, usage_response


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if query.strip().lower() in {"help", "?"}:
        print_json(usage_response())
        return

    mode, text = parse_query(query)
    print_json(build_result(mode, text))
