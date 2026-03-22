import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.sha import (
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

    algorithm, text, error = parse_query(query)
    if error == "empty":
        print_json(usage_response())
        return
    if error:
        print_json(error_response(error))
        return

    print_json(build_results(algorithm, text))
