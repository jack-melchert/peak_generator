# force color
export PYTEST_ADDOPTS="--color=yes"

pytest --cov peak_gen --cov-report term-missing -v tests/
