# Dependency management: pip to uv

## Before

This repo already had a `pyproject.toml` (setuptools backend, dependencies
`matplotlib`, `tqdm`, optional `test` extra `pytest`), plus a stray
`requirements.txt` left over from before `pyproject.toml` existed (see
commit 54253c9, "Migrate packaging to pyproject.toml; add tqdm dependency").
The two files listed the same three packages (matplotlib, tqdm, pytest), no
version mismatch, just a redundant flat file duplicating what `pyproject.toml`
already declared.

- Command: `pip install --no-cache-dir -r requirements.txt` (fresh venv)
- Measured time: 6.196s wall clock
- Packages installed: 16 (3 direct + 13 transitive)

## After

- `uv lock` generated `uv.lock` directly from the existing `pyproject.toml`.
  No changes to `pyproject.toml` were needed; the lock resolved cleanly.
- Command: `uv sync` (fresh `.venv`)
- Measured time: 1.200s wall clock
- Packages installed: 13 (base dependencies only; `matplotlib`/`tqdm` plus
  transitives and the project itself). The `test` extra (`pytest` + 3 deps)
  installs separately via `uv sync --extra test` and is not part of the
  default sync, unlike `requirements.txt`, which flattened runtime and test
  deps into one list.
- `requirements.txt` was deleted. `pyproject.toml` + `uv.lock` are now the
  single source of truth.
- Verified with `uv run --extra test pytest`: 5 passed.

Note: uv's install benefits from its shared local package cache (already
warm on this machine from prior use), which is part of its design and a
real part of the speed difference versus pip's cold, no-cache install above.
This is not an apples-to-apples "cold cache vs cold cache" number.

## Takeaway

uv resolves and installs from the same dependency set in a fraction of the
time pip took, while collapsing two sources of truth (`requirements.txt` +
`pyproject.toml`) into one (`pyproject.toml` + `uv.lock`).
