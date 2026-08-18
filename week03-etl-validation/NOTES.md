# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 142602003
seed: 2936299248

## Quarantine count vs. the 7 known injected problems

<!-- How many rows ended up quarantined, and does that match the 7 known
     injected problems? (It won't match exactly — some rows may trip more
     than one expectation. Explain the discrepancy if there is one.) -->
The pipeline has 600 rows and quarantined 6 rows. There were 8 total validation violations.

6 rows were quarantined instead of 7 because there is no validation check for the country code. Therefore, the row with the invalid country code was not detected or quarantined.

Some rows failed more than one expectation. The two rows with empty/null amount values failed both the not_null and positive`checks. 

expect_column_not_null: 3 (2(amount)+1(card_id)) violations
expect_column_positive: 3 violations
expect_column_in_set: 1 violation
expect_column_unique: 1 violation