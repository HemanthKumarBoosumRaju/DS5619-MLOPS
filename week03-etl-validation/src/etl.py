"""
Extract -> Validate -> Transform -> Load pipeline for the fraud transaction
data. Run with:

    python src/etl.py --config config.yaml

(a default config.yaml pointing at data/raw_transactions.csv is provided)
"""
import argparse
import csv
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expectations as exp

KNOWN_CATEGORIES = {
    "grocery", "electronics", "fuel", "travel", "restaurant",
    "online_retail", "utilities", "pharmacy", "entertainment", "atm_withdrawal",
}


def build_expectation_suite():
    """The data contract for this dataset. Each entry says which expectation
    function to run, and with what arguments. This is provided — read it to
    know exactly what your expectation functions in expectations.py need to
    handle correctly.
    """
    return [
        (exp.expect_column_not_null, {"column": "amount"}),
        (exp.expect_column_not_null, {"column": "card_id"}),
        (exp.expect_column_positive, {"column": "amount"}),
        (exp.expect_column_in_set, {"column": "merchant_category", "allowed_values": KNOWN_CATEGORIES}),
        (exp.expect_column_unique, {"column": "transaction_id"}),
    ]


def extract(input_path):
    with open(input_path, newline="") as f:
        return list(csv.DictReader(f))


def run_etl(config):
    """Implement the four ETL steps described in ASSIGNMENT.md:
    extract, validate (run every expectation in build_expectation_suite()
    and collect ALL violations, not just the first), transform (split into
    clean vs quarantined rows — a row with ANY violation is quarantined),
    load (write clean_output_path, quarantine_output_path, and
    report_output_path as described in the assignment).

    Return the validation_report dict as well as writing it to disk.
    """
    # TODO: implement
    input_path=config["input_path"]
    rows=extract(input_path)
    violations = []
    expectation_results = []

    for expectation, arguments in build_expectation_suite():
        result = expectation(rows, **arguments)

        violations.extend(result)

        expectation_results.append({
            "expectation": expectation.__name__,
            "column": arguments["column"],
            "n_violations": len(result),
            "row_indices": [violation.row_index for violation in result]
        })

    bad_rows=set()
    for violation in violations:
        bad_rows.add(violation.row_index)

    clean_rows=[]
    quarantined_rows=[]

    for i, row in enumerate(rows):
        if i in bad_rows:
            quarantined_rows.append(row)
        else:
            clean_rows.append(row)

    # Write for clean CSV
    with open(config["clean_output_path"], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())

        writer.writeheader()
        writer.writerows(clean_rows)

    # Write for quarantined CSV
    with open(config["quarantine_output_path"], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())

        writer.writeheader()
        writer.writerows(quarantined_rows)

    # write validation report
    validation_report = {
        "expectations": expectation_results,
        "summary": {
            "total_rows": len(rows),
            "clean_rows": len(clean_rows),
            "quarantined_rows": len(quarantined_rows),
            "total_violations": len(violations)
        }
    }
    

    # return validation_report
    with open(config["report_output_path"], "w") as f:
        json.dump(validation_report, f, indent=2)
    return validation_report
    # raise NotImplementedError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    report = run_etl(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
