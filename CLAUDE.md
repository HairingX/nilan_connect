# Conventions for this repository

An event-driven, async Python library for Nilan and Genvex ventilation units behind their
gateway, over its local micro_nabto protocol: every value typed, and told when it changes. It is
built on the `modbus_event_connect` and `event_connect` libraries, developed alongside it. The
Home Assistant integration `ha_nilan_connect` is built on it.

## This library

- The email the gateway is paired with is a credential: never logged, never in a tracked file.
- Live tests (`tests/test_live_*.py`) only read, and never write to a controller. They take the
  gateway's address and email from environment variables or the gitignored `mysecrets.py`, and
  skip without them.
- Everything a consumer uses comes from `nilan_connect`, nothing from `modbus_event_connect` or
  `event_connect`; `nilan_connect.testing` gives its tests a simulated gateway and a clock the test moves.
- `__version__` reads the version from the installed package.
- `docs/models/` holds the manufacturers' manuals with every register extracted; the PDF is the
  authority, the extracts working copies.

<!-- BEGIN HairingX/workflows: shared; edit it there -->
## Shared by every library

This section, the workflows and the release tools are the same in every Python library of the
owner. They come from `HairingX/workflows`: the workflows in `.github/` are copies of its
template, which call its reusable workflows and actions at `@v2`, and this section is a copy of
its `python/template/CLAUDE.md`. The tests check that the copies agree; a change to any of them is
made there, released, and synced into every repository with its
`common/tools/template.py sync python`. What is this repository's own is above this section.

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

## Conventions

- All documentation, comments and commit messages are in English.
- The package lives in `src/<package>/` and ships its types (`py.typed`). It supports the Python
  Home Assistant runs on, 3.14, and later (`requires-python = ">=3.14"`), as it is made for its
  integrations; the tests run on 3.14 alone.
- pyright strict must report 0 errors (`pyright`); the configuration is in `pyproject.toml`.
  No `# type: ignore` and no rule turned off.
- The tests are pytest, in `tests/`, and cover every line of the package; the build fails below
  100%. They import the installed package, as its users do, never `src.<package>`: a packaging
  mistake then fails a test before a release. Tests that need a real device are marked `live`,
  skip themselves without one, and never run in CI.
- A repository on its way to this standard says so under `[tool.hairingx-workflows]` in
  `pyproject.toml`: `transition` says why, and `coverage` the percentage its tests must reach
  meanwhile; pyright, still strict, may leave the files listed in `[tool.pyright] ignore`
  unchecked. Every run warns while it lasts. Each pull request raises the coverage and takes
  files off the list, never the reverse, until the transition is removed.
- Every problem found gets a test that fails without the fix.
- The test tools are pinned with `==` in `requirements-test.txt`, pyright, pytest and
  pytest-cov among them: `pip install -e . -r requirements-test.txt`.
- No real IP addresses, hostnames, serial numbers, email addresses or credentials in tracked
  files; real values live in a gitignored file or in environment variables. Examples use the
  documentation ranges, such as 192.0.2.0/24. A credential is never logged.

## Releasing

**The version is the release's tag, and the draft release is never published by hand.** The
package has no version in a file: setuptools-scm works it out from the tags when it is built, so a
checkout between releases says a development version such as `0.2.1.dev3+g1a2b3c4`.

1. Merge pull requests into `main`. Release Drafter keeps a draft release proposing the next
   version: a minor bump for the label `breaking-change` or `minor`, a patch otherwise.
   **A new major version is never worked out**, as a label placed wrongly must not release one;
   type it into Release as the override.
2. Wait until the Release Drafter run on `main` has finished. Release refuses a draft that is not
   up to date with `main`.
3. Show the maintainer the draft's notes and its version, and get explicit approval before
   running Release.
4. Run the **Release** workflow from the Actions tab, on `main`, and choose **release
   candidate** or **final release**. It works out the version: the next release candidate of the
   open series (`0.2.0rc1` -> `0.2.0rc2`), or the final release that ends it (`0.2.0`); a draft
   naming a higher version starts a new series. Type a version only for a new major, or to
   override one worked out wrongly: canonical PEP 440, of the kind chosen.

Release refuses any version not higher than every version tagged or on PyPI, yanked ones
included, and a version with no pull request merged since the release before it - for a final
release, the final release before it. It runs the tests on the exact commit it releases, tags
that commit, builds, checks that the built package says the version, and only then pushes the
tag - nothing is pushed to `main`. Then PyPI, then the GitHub release with the distributions,
marked as a pre-release where it is one.

A release candidate's notes are written by GitHub from the pull requests merged since the
previous release candidate or final release, grouped by label as `.github/release.yml` says, and
the draft is kept. A final release's notes are the draft's - the first final release says only
that it is the initial release - and the final release deletes the draft. To change what a
release says, change the pull requests: the title is the line, the labels decide the section.

If publishing fails part-way, **Re-run failed jobs** resumes it: the tag, PyPI and the GitHub
release each accept what an earlier attempt already did.

PyPI trusted publishing is bound to this repository, the workflow file `release.yml` and the
`pypi` environment: renaming either breaks the upload. Actions are referred to by their major
version. Dependabot proposes each update of the test tools once it is three days old, all
that are no new major version in one pull request a week, and **Merge Dependabot's updates**
merges it once every check passes, then updates the release draft. It assigns the owner only an
update that needs them: a new major version, or one a check fails. The actions are the
template's, kept up to date in HairingX/workflows.
Packages Home Assistant decides, and the owner's own libraries, are left out.

## Libraries developed together

A library this one depends on and develops alongside is listed, in install order, under
`[tool.hairingx-workflows] libraries` in `pyproject.toml`. A development branch is tested with
that library's branch of the same name, where it has one, over its release; the check
"Libraries released and pinned" then fails until the library is released, its version required
in `pyproject.toml`, and its branch deleted. **Release a library first**, then require its
version here.

## Branches and pull requests

- Every change goes through a branch and a pull request: `main` takes no push. The ruleset in
  `.github/rulesets/main.json` enforces it, with the checks "Python 3.14" and "Libraries
  released and pinned" required; its only bypass is the owner's, and only for merging a pull
  request. A change to what a user gets - the library's code or
  documentation - comes with its tests.
- Name every branch by the kind of change, as the release draft's labels follow the name;
  `.github/rulesets/branch-names.json` refuses any other name. `feature/<what>` is labelled
  `feature request`, `fix/<what>` is labelled `bug`, `docs/<what>` is labelled `documentation`,
  and `chore/<what>` - CI, tooling, anything that stays in the repository - is labelled `chore`.
  The release notes list features and fixes; documentation, chores and Dependabot's
  `dependencies` are left out. A change to what a user installs, such as a new dependency, is a
  `fix/` or a `feature/`, never a `chore/`.
- A pull request's text describes only its own change: what it does and how it was tested. Never
  releases to come, merge order, or other repositories.
- Put `breaking-change` on a pull request that breaks the API - a `feature/` or `fix/` one, as a
  chore is left out of the notes - and `minor` on one that needs a minor bump; both give a minor
  bump, and a patch is the default. No label gives a major.
<!-- END HairingX/workflows -->
