# Welcome to my 6.0001 Coursework

All the assignments and tests will be in this repository.

## Clone repository

```sh
git clone <this-repo>
```

### Make sure you have Python installed

```sh
python -V
```

## Setup virtual environment (venv)

```sh
python3 -m venv .venv
```

## Activate venv and install dependencies

**Important: check the correct way of activation depending on your shell. Consult [here.](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)** (I use [fish shell](https://fishshell.com/))

```sh
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
```

## Run any of the programs

```sh
python <program-name>.py
```
