# LLM Cultural Assumption Bias

## Usage

Install the required libraries with:

```sh
pip install -r requirements.txt
```

To query GPT3.5 use the `CS_gpt3_query.py` script, it takes just one argument, which should be a file containing all queries.

```sh
python CA_gpt3_query.py breakfast_prompts.tsv
```

The script will then output the queries and their most probably completions in a new file called `<query_file>_results.tsv`.

To score these results you can use the `CA_gpt3_scoring.py` script, which will output the distances of all queries from the neutral query. (less is closer)

```sh
python CA_gpt3_scoring.py breakfast_prompts.tsv
```