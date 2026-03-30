import subprocess, re, sys

def check_pylint():
    result = subprocess.run(
        ["pylint", "app", "tests", "--score=y"],
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    if result.returncode not in (0, 32):  # 32 means pylint warnings/errors
        sys.exit(result.returncode)

    m = re.search(r"Your code has been rated at ([0-9]+\.[0-9]+)/10", result.stdout)
    if not m:
        print("Could not detect pylint score")
        sys.exit(1)
    score = float(m.group(1))
    print(f"Pylint score {score}")
    if score < 8.0:
        print("ERROR: pylint score below threshold")
        sys.exit(1)

if __name__ == "__main__":
    check_pylint()
    