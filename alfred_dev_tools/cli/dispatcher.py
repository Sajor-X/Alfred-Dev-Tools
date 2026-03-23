import importlib
import sys


COMMAND_MODULES = {
    "b64": "alfred_dev_tools.cli.b64",
    "catalog": "alfred_dev_tools.cli.catalog",
    "case": "alfred_dev_tools.cli.caseconv",
    "cron": "alfred_dev_tools.cli.cron",
    "help": "alfred_dev_tools.cli.catalog",
    "html": "alfred_dev_tools.cli.htmlcodec",
    "json": "alfred_dev_tools.cli.jsonfmt",
    "jsonfmt": "alfred_dev_tools.cli.jsonfmt",
    "jwt": "alfred_dev_tools.cli.jwt",
    "md5": "alfred_dev_tools.cli.md5",
    "pwd": "alfred_dev_tools.cli.passwords",
    "pwg": "alfred_dev_tools.cli.passwords",
    "sha": "alfred_dev_tools.cli.sha",
    "textstat": "alfred_dev_tools.cli.textstat",
    "tc": "alfred_dev_tools.cli.textstat",
    "timer": "alfred_dev_tools.cli.timer",
    "timer-worker": "alfred_dev_tools.cli.timer_worker",
    "ts": "alfred_dev_tools.cli.ts",
    "url": "alfred_dev_tools.cli.url",
    "urldecode": "alfred_dev_tools.cli.urldecode",
    "urlencode": "alfred_dev_tools.cli.urlencode",
    "uuid": "alfred_dev_tools.cli.uuidgen",
}


def main():
    if len(sys.argv) < 2:
        available = ", ".join(sorted(COMMAND_MODULES))
        raise SystemExit(f"Usage: python3 workflow.py <command> [args]\nAvailable: {available}")

    command = sys.argv[1]
    module_name = COMMAND_MODULES.get(command)
    if module_name is None:
        available = ", ".join(sorted(COMMAND_MODULES))
        raise SystemExit(f"Unknown command: {command}\nAvailable: {available}")

    module = importlib.import_module(module_name)
    sys.argv = [sys.argv[0], *sys.argv[2:]]
    module.main()
