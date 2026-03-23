import sys

from alfred_dev_tools.alfred import print_json
from alfred_dev_tools.features.cron import build_results


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print_json(build_results(query))
