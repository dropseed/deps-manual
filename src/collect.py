import os
import sys
import json
from run import run_script


def get_deps():
    deps = json.loads(os.environ.get("DEPS_SETTING_DEPS", "{}"))

    if not deps:
        raise Exception('The "deps" setting needs to be defined.')

    return deps


def collect(input_path, output_path):
    deps = get_deps()

    current_archives = {}
    updated_archives = {}

    for name, settings in deps.items():
        print(f"Collecting {name}")

        installed_version = run_script(
            input_path, settings["collect"], return_output=True
        )

        if not installed_version:
            raise Exception(f"Could not detect installed version of {name}")

        run_script(input_path, settings["act"])

        latest = run_script(input_path, settings["collect"], return_output=True)

        current_archives[name] = {
            "constraint": installed_version,
            "source": "manual",
        }

        if latest and latest != installed_version:
            updated_archives[name] = {
                "constraint": latest,
                "source": "manual",
            }

    output = {
        "manifests": {
            input_path: {
                "current": {"dependencies": current_archives,},
                "updated": {"dependencies": updated_archives,},
            }
        }
    }

    with open(output_path, "w+") as f:
        json.dump(output, f)


if __name__ == "__main__":
    collect(sys.argv[1], sys.argv[2])
