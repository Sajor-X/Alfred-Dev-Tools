import sys

from alfred_dev_tools.alfred import print_json
from alfred_dev_tools.features.passwords import (
    build_results,
    error_response,
    parse_query,
    usage_response,
)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if query.strip().lower() in {"help", "?"}:
        print_json(usage_response())
        return

    parsed, message = parse_query(query)
    if message:
        print_json(error_response(message))
        return

    length, count, include_special = parsed
    print_json(build_results(length, count, include_special))
