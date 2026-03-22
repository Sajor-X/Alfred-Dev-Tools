import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.md5 import build_result, usage_response


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    if not text:
        print_json(usage_response())
        return

    print_json(build_result(text))
