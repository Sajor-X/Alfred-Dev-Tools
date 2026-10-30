import sys

from alfred_dev_tools.alfred import print_json
from alfred_dev_tools.features.rgb import build_results


def main():
    print_json(build_results(" ".join(sys.argv[1:])))
