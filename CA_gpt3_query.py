import argparse
import csv
import math
import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI()


def query(text: str, n=1):
    """
    Queries the GPT-3.5 Turbo model with the given text prompt and returns the generated responses.

    Args:
        text (str): The text prompt to query the model with.
        n (int, optional): The number of responses to generate. Defaults to 1.

    Returns:
        list: A list of generated responses from the GPT-3.5 Turbo model.
    """
    response = openai_client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=text,
        temperature=0.5,
        max_tokens=10,
        top_p=1,
        n=n,
        frequency_penalty=0,
        presence_penalty=0,
        logprobs=5,
        stop=".",
    )

    return response.choices


def addOther(log_prob_dict: dict):
    """
    Make a log probability dictionary a probability distribution by adding an 'OTHER' category.

    This function takes a log probability dictionary as input and adds an 'OTHER' category to it. The 'OTHER' category represents the probability of all other categories that are not explicitly listed in the dictionary. The function calculates the probability of the 'OTHER' category by subtracting the sum of probabilities of all other categories from 1.

    Args:
        log_prob_dict (dict): A dictionary containing log probabilities of different categories.

    Returns:
        dict: A modified log probability dictionary with the 'OTHER' category added.

    Raises:
        AssertionError: If the sum of probabilities in the modified dictionary is not equal to 1, it indicates that some probability has been lost during the calculation.

    Example:
        >>> log_prob_dict = {'A': -1.3862943611198906, 'B': -0.6931471805599453}
        >>> addOther(log_prob_dict)
        {'A': -1.3862943611198906, 'B': -0.6931471805599453, 'OTHER': -0.4054651081081644}
    """
    total = sum((math.exp(v) for v in log_prob_dict.values()))
    other_prob = 1 - total
    log_prob_dict["OTHER"] = math.log(other_prob)

    assert sum((math.exp(v) for v in log_prob_dict.values())) == 1  # Some probability has been lost if this fails

    return log_prob_dict


def stripKeys(prob_dict: dict[str, float]):
    """
    Strips leading and trailing whitespace from the keys of a dictionary.

    Args:
        prob_dict (dict): The dictionary whose keys need to be stripped.

    Returns:
        dict: The dictionary with stripped keys.
    """
    keys = list(prob_dict.keys())

    for k in keys:
        key = k.strip()

        if "\n" in key:
            key = key.replace("\\n", "\n")

        if key != k:
            prob_dict[key] = prob_dict[k]
            prob_dict.pop(k)

    return prob_dict


def run_one_item(textprompt, n):
    """
    Runs the GPT-3 query for a single item.

    Args:
        textprompt (str): The text prompt for the GPT-3 query.
        n (int): The number of responses to retrieve.

    Returns:
        tuple: A tuple containing the following:
            - new_probs (dict): A dictionary containing the normalized probabilities of the top logprobs.
            - texts (list): A list of strings representing the generated texts from the GPT-3 responses.
    """

    responses = query(textprompt, n=n)
    texts = [r.text.strip().split("\n")[0].strip() for r in responses]

    print(texts)

    log_prob_dicts = [r.logprobs.top_logprobs[0] for r in responses]
    log_prob_dicts = [addOther(d) for d in log_prob_dicts]
    log_prob_dicts = [stripKeys(d) for d in log_prob_dicts]

    print([log_prob_dict.keys() for log_prob_dict in log_prob_dicts])

    all_log_probs = [i for d in log_prob_dicts for i in d.items()]
    new_probs = {}

    for k, v in all_log_probs:  # Add probabilities across samples
        if k in new_probs:
            new_probs[k] += math.exp(v)
        else:
            new_probs[k] = math.exp(v)

    norm = sum(new_probs.values())  # Re-normalize

    for k, v in new_probs.items():
        new_probs[k] = new_probs[k] / norm

    return new_probs, texts


def export(fn, item_list, prob_dicts: list[dict], texts):
    """
    Export the results to a TSV file.

    Args:
        fn (str): The filename prefix for the output file.
        item_list (list): A list of items.
        prob_dicts (list): A list of probability dictionaries.
        texts (list): A list of texts.

    Returns:
        None
    """
    with open(fn + "_results.tsv", "w", newline="") as of:

        writer = csv.writer(of, delimiter="\t")

        for i, item in enumerate(item_list):
            problist = [item for k in sorted(prob_dicts[i].keys()) for item in [k, prob_dicts[i][k]]]
            bits = item + problist + texts[i]
            line = [str(b) for b in bits]

            writer.writerow(line)


def main():
    parser = argparse.ArgumentParser(description="GPT-3 Query")

    parser.add_argument("infile", help="Input file")

    args = parser.parse_args()

    infile: str = args.infile
    outfile = infile.split(".")[0]
    items = [s.strip().split("\t") for s in open(infile, "r").readlines()]
    results = [run_one_item(item[2], 5) for item in items]
    probs = [r[0] for r in results]
    texts = [r[1] for r in results]

    export(outfile, items, probs, texts)


if __name__ == "__main__":
    main()
