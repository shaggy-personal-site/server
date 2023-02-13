# Personal Site Server

```zsh
python -m venv .venv
. .venv/bin/activate

poetry install
pre-commit install

shaggy migrate
```