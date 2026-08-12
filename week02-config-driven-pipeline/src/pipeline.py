"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json

import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
    # TODO: implement
    with open(path,"r") as file:
        data=yaml.safe_load(file)
    
    missingKeySet=set(REQUIRED_KEYS)-set(data.keys())

    if missingKeySet:
        raise ValueError(f"Missing the following REQUIRED_KEYS{list(missingKeySet)}")

    return data


def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    # TODO: implement
    if fmt not in ("csv","json"):
        raise ValueError(f"Unsupported format given: {fmt}, format needs to be in csv or json")
    
    elif fmt=="json":
        with open(path,"r") as file:
            data=json.load(file)
        transactions=data

    elif fmt=="csv":
        with open(path,"r",newline="") as file:
            #convert csv and read it as list because csv.DictReader() creates stream of data not list
            transactions=list(csv.DictReader(file))

    for t in transactions:
        if not isinstance(t,dict) or "amount" not in t or "is_fraud" not in t:
            raise ValueError("Each transaction must be a dict containing both amount and is_fraud")

        if not isinstance(t["amount"], (str, float)):
            raise ValueError('"amount" must be a string or float')

        if not (t["is_fraud"] in ("True", "False") or isinstance(t["is_fraud"], bool)):
            raise ValueError('"is_fraud" must be "True", "False", or a boolean')  

    return transactions 
                                                                                  
                                                                                 
def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    # TODO: implement
    transactions=load_transactions(config["input_path"], config["input_format"])

    n_transactions=len(transactions)

    total_amount = 0
    no_of_fraud = 0
    n_high_value = 0

    for t in transactions:
        total_amount+=float(t["amount"])

        if str(t["is_fraud"]).lower()=="true":
            no_of_fraud+=1

        if float(t["amount"])>config["high_value_threshold"]:
            n_high_value+=1


    fraud_rate=round(no_of_fraud/n_transactions,2) if n_transactions>0 else 0

    report = {
        "n_transactions": n_transactions,
        "total_amount": round(total_amount,2),
        "fraud_rate": fraud_rate,
        "n_high_value": n_high_value,
        "high_value_threshold": config["high_value_threshold"]
    }

    with open(config["output_path"],"w") as file:
        json.dump(report,file,indent=2)

    return report


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
