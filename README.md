# LLM Cultural Assumption Bias

## Requirements

Install Python 3.11.x from [here](https://www.python.org/downloads/release/python-3119/)

## Create an environment

Create the environment **inside this directory**.

```sh
python -m venv .venv
```

activate it like so:

```sh
& .\.venv\Scripts\activate
```

or like this on Linux/Max:

```sh
. ./.venv/bin/activate
```

## Usage

Make sure your environment is activated, it should say the name of the environment in you terminal: `(.venv) yourpath>`

Install the required libraries with:

```sh
pip install -r requirements.txt
```

To query GPT3.5 use the `CA_gpt3_query.py` script, it takes just one argument, which should be a file containing all queries, the `breakfast_prompts.csv` is an example.

```sh
python CA_gpt3_query.py breakfast_prompts.tsv
```

The script will then output the queries and their most probably completions in a new file called `<query_file>_results.tsv`.

To score these results you can use the `CA_gpt3_scoring.py` script, which will output the distances of all queries from the neutral query. (less is closer)

```sh
python CA_gpt3_scoring.py breakfast_prompts_results.tsv
```