import tempfile
from subprocess import check_output, run


def run_script(cwd, script, return_output=False):
    output = ""

    print(f"Running script:\n{script}")

    with tempfile.NamedTemporaryFile() as f:
        f.write(script.encode("utf-8"))
        f.seek(0)

        if return_output:
            output = (
                check_output(["/bin/sh", "-euo", "pipefail", f.name], cwd=cwd)
                .decode("utf-8")
                .strip()
            )
        else:
            run(["/bin/sh", "-euo", "pipefail", f.name], cwd=cwd, check=True)

    print(f"Returning output:\n{output}")

    return output
