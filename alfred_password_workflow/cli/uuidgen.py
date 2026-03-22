import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.uuidgen import (
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

    version, count = parsed
    print_json(build_results(version, count))
