import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.ts import build_response


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print_json(build_response(query))
