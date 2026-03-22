import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.htmlcodec import build_result, parse_query


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    mode, text = parse_query(query)
    print_json(build_result(mode, text))
