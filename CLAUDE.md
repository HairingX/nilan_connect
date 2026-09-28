# Conventions for this repository

## Comments and docstrings

Based on PEP 8 (Comments), PEP 257 (Docstring Conventions) and the Google Python Style Guide
(3.8 Comments and Docstrings).

**Docstrings describe the unit's own contract, and nothing else.**
- Every public module, class, function and method has one.
- The first line is a one-sentence summary. Add more only when a caller needs it: arguments,
  return value, exceptions raised, side effects, invariants.
- Use Google style sections (`Args:`, `Returns:`, `Raises:`) only when they say something the
  signature and type hints do not. Never repeat types; the hints carry them.
- Describe what the unit does, not who calls it, how other classes use its data, or where its
  result ends up. That knowledge belongs to those other units and goes stale here.

**Comments explain why, never what.**
- Write one only where the code cannot say it: a protocol quirk, a non-obvious constraint, the
  reason for an order of operations.
- No history: no "used to", "previously", "the old code", "this was a bug". Version control
  holds history; a regression test's name holds the reason it exists.
- No references to other files, classes, line numbers or design-document sections. They rot the
  moment the other side changes.
- No commented-out code. No TODO without an issue reference.

**Keep them short.** A comment longer than a few lines is design rationale; it belongs in
`docs/`, where it can cover several modules at once.

**Tests.** The test name states the behaviour. Add a docstring only when the reason is not
obvious from the name - one or two lines, no narrative.

## Other conventions

- pyright strict must report 0 errors (`pyright`); the configuration is in `pyproject.toml`.
  The release scripts are a project of their own: `pyright -p .github/scripts`.
- Every problem found gets a test that fails without the fix.
- Live tests (`tests/test_live_*.py`) only read, and skip themselves unless a device is
  configured. CI runs `pytest -m "not live"`.
- Test tools are pinned in `requirements-test.txt`: `pip install -e . -r requirements-test.txt`.
- Tests import the installed package, as its users do, never `src.<package>`: a packaging
  mistake then fails a test before a release.
- No real IP addresses, hostnames or email addresses in tracked files; real values live in the
  gitignored `mysecrets.py` or in environment variables.

## Releasing

**Never edit the version by hand, and never publish the draft release by hand.** Publishing the
draft creates the tag at whatever `main` points to, before the version is set; every tag of
`modbus_event_connect` up to `v0.1.8` carries the previous version for that reason.

1. Merge pull requests into `main`. Release Drafter keeps a draft release proposing the next
   version: a minor bump for the label `breaking-change` or `minor`, a patch otherwise.
   **A new major version is never worked out**, as a label placed wrongly must not release one;
   type it into Release as the override.
2. Run the **Release** workflow from the Actions tab, on `main`, and choose **release
   candidate** or **final release**. It works out the version: the next release candidate of the
   open series (`0.2.0rc1` -> `0.2.0rc2`), or the final release that ends it (`0.2.0`); a draft
   naming a higher version starts a new series. Type a version only for a new major, or to
   override one worked out wrongly: canonical PEP 440, of the kind chosen.

Release refuses a version with no pull request merged since the release before it - for a
final release, the final release before it: a change pushed straight to `main` is nothing
to release.

Release refuses any version not higher than every version tagged or on PyPI, yanked ones
included. It runs the tests on the commit it releases, sets `__version__`, builds, installs the
wheel and checks that `__version__` and the metadata say the version, and only then pushes the
version commit and the tag together - a fast-forward of `main` from the tested commit, refused
if `main` moved. Then PyPI, then the GitHub release, marked as a pre-release where it is one.

A release candidate's notes are written by GitHub from the pull requests merged since the
previous release candidate or final release, grouped by label as `.github/release.yml` says. A
final release's notes are the draft's: edit the draft - it lists what was merged since the last
final release - and run Release before anything else is merged, as a merge rewrites the draft.
Without a draft, GitHub writes them from the pull requests since the previous final release.

This package depends on `modbus_event_connect`, and `Release` installs the built wheel with its
dependencies from PyPI. **Release the library first**: a version of this package that needs
an unpublished library fails that check, and nothing is tagged.

PyPI trusted publishing is bound to this repository, the file `release.yml` and the `pypi`
environment: renaming either breaks the upload. Actions are referred to by their major version;
Dependabot proposes a new major, and updates to the test tools, as pull requests.

## Branches and pull requests

- Process changes - CI, tests and test tools, the release, the release draft, these
  conventions - go straight to `main`: they change nothing a user of the library gets. A change
  to what a user gets - the library's code or documentation - goes through a branch and a pull
  request, with its tests.
- Name every branch by the kind of change, as the release draft's labels follow the name:
  `feature/<what>` is labelled `feature request`, `fix/<what>` is labelled `bug`, and
  `chore/<what>` - CI, tooling, documentation - is labelled `chore`.
- A pull request's text describes only its own change: what it does and how it was tested. Never
  releases to come, merge order, or other repositories.
- Put `breaking-change` on a pull request that breaks the API, and `minor` on one that needs a
  minor bump; both give a minor bump, and a patch is the default. No label gives a major.
