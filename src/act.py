import json
import sys

from collect import get_deps
from run import run_script


def act(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    deps = get_deps()

    for manifest_path, manifest_data in data.get("manifests", {}).items():
        for dependency_name, updated_dependency_data in manifest_data["updated"][
            "dependencies"
        ].items():
            version_to_update_to = updated_dependency_data["constraint"]

            run_script(manifest_path, deps[dependency_name]["act"])
            updated_dependency_data["constraint"] = run_script(
                manifest_path, deps[dependency_name]["collect"], return_output=True
            )

    with open(output_path, "w+") as f:
        json.dump(data, f)


if __name__ == "__main__":
    act(sys.argv[1], sys.argv[2])
