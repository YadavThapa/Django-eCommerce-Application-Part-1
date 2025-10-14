scripts/
=======

This folder contains developer helper scripts that were previously saved at the
project root as `tmp_*.py`. They are convenience utilities for local
development and are not part of the test suite or production code.

Files:
- create_test_order_dev.py — developer-friendly version kept for manual runs.
- create_test_order_runtime.py — variant using runtime `shop.models` imports.

Notes:
- These scripts perform `django.setup()` in-file and therefore intentionally
  perform imports after setup; they include per-file linter ignores.
- Keep these in the repo if you rely on them, or move them to a separate
  dotfiles / personal-scripts repository if you prefer not to track them in
  the project.
