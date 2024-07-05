## BLOG APP API

This is the repository for the backend services

# Getting started

Follow the next instructions to get the project ready to use.

## Requirements:

- [Python version 3](https://www.python.org/download/releases/3.0/) (recommended 3.8 or less) in your path. It will install
  automatically [pip](https://pip.pypa.io/en/stable/) as well.
- A virtual environment, namely [.venv](https://docs.python.org/3/library/venv.html).
- Docker

### Create a virtual environment

Execute the next command at the root of the project:

```shell
python -m venv .venv
```

**Activate the environment**

Windows:
```shell
.venv\Scripts\activate.bat
```

In Unix based operative systems:

```shell
source .venv/bin/activate
```

## Dependencies:

The dependencies are defined inside requirements file.

### Installation

#### Dependencies

Execute the next command once you have created the venv:

```shell
pip install -r requirements.txt
```

#### Docker file
To create a database for local testing you can run the docker-compose structure defiend in docker-compose.local.yml

```shell
docker compose -f docker-compose.local.yml up -d
```

#### Load env variables

You should create a .env file in the root of the project. You should copy the env variables that exist in .env-template and ask for values.

You can load the env varaibles with the next command:

```shell
source .env
```

#### Run the app

To run the app you can use the next command:

```shell
uvicorn app.main:app --reload
```