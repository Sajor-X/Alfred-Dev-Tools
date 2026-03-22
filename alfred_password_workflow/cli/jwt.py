import sys

from alfred_password_workflow.alfred import print_json
from alfred_password_workflow.features.jwtdecode import build_results


def main():
    token = sys.argv[1] if len(sys.argv) > 1 else ""
    print_json(build_results(token))
