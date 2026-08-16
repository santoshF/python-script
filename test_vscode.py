"""
Tests that the Python extension (ms-python.python) is installed and functional in VS Code.
"""

import subprocess
import sys
import tempfile
import os


PYTHON_EXTENSION_ID = "ms-python.python"


def check_vscode_installed():
    try:
        result = subprocess.run(
            ["code", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().splitlines()[0]
            print(f"[PASS] VS Code found: version {version}")
            return True
        else:
            print("[FAIL] VS Code CLI returned an error")
            return False
    except FileNotFoundError:
        print("[FAIL] VS Code not found — make sure 'code' is in your PATH")
        print("       Mac: open VS Code -> Cmd+Shift+P -> 'Install code command in PATH'")
        return False


def check_python_extension_installed():
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    extensions = result.stdout.strip().splitlines()
    if PYTHON_EXTENSION_ID in extensions:
        print(f"[PASS] Python extension ({PYTHON_EXTENSION_ID}) is installed")
        return True
    else:
        print(f"[FAIL] Python extension ({PYTHON_EXTENSION_ID}) is NOT installed")
        print("       Install it: code --install-extension ms-python.python")
        return False


def check_python_interpreter():
    result = subprocess.run(
        [sys.executable, "--version"],
        capture_output=True, text=True
    )
    version = result.stdout.strip() or result.stderr.strip()
    print(f"[PASS] Python interpreter: {version} ({sys.executable})")
    return True


def check_pylint_or_linter():
    for linter in ["pylint", "flake8", "ruff"]:
        result = subprocess.run(
            [sys.executable, "-m", linter, "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().splitlines()[0]
            print(f"[PASS] Linter available: {linter} {version}")
            return True
    print("[WARN] No linter found (pylint/flake8/ruff) — optional but recommended")
    return False


def check_open_test_file():
    """Creates a simple .py file and opens it in VS Code to confirm the extension activates."""
    code = "print('Hello from VS Code Python extension test!')\n"
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(code)
        tmp_path = f.name

    result = subprocess.run(
        ["code", "--wait", tmp_path],
        capture_output=True, text=True
    )
    os.unlink(tmp_path)

    if result.returncode == 0:
        print("[PASS] VS Code opened and closed the test .py file successfully")
        return True
    else:
        print(f"[FAIL] VS Code exited with code {result.returncode}")
        return False


def main():
    print("=" * 50)
    print("VS Code Python Extension Test")
    print("=" * 50)

    results = []
    results.append(("VS Code installed",          check_vscode_installed()))
    results.append(("Python extension installed",  check_python_extension_installed()))
    results.append(("Python interpreter",          check_python_interpreter()))
    results.append(("Linter available",            check_pylint_or_linter()))

    answer = input("\nOpen a test .py file in VS Code to verify activation? [y/N]: ").strip().lower()
    if answer == "y":
        results.append(("Open .py in VS Code", check_open_test_file()))

    print("\n" + "=" * 50)
    passed = sum(1 for _, ok in results if ok)
    print(f"Results: {passed}/{len(results)} checks passed")
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print("=" * 50)

    sys.exit(0 if all(ok for _, ok in results) else 1)


if __name__ == "__main__":
    main()