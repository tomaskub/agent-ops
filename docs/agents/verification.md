# Verification

Use Python 3.10 or later and Git on a Unix host. The fixture uses the Python standard library and temporary Git repositories. It runs without Docker, Hermes, network access, or credentials.

Run these checks from the repository root on the exact candidate commit:

```sh
python3 -B tests/distributed_fixture.py
git diff --check <base-sha> <head-sha>
```

Replace the placeholders with the pinned implementation base and candidate commit. In a distributed run, the verification worker runs the fixture. The trusted host checks the base-to-head diff before integrating and publishing the candidate. Repeat both checks after a repair.

The fixture must exit zero and report completed delivery and review evidence. The whitespace check must exit zero. A failed, skipped, or unavailable check blocks review handoff. Record the command, directory, Python version, tested SHAs, exit status, and results in the run record and PR.
