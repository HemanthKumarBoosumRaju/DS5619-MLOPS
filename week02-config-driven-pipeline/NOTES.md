# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
142602003

## What was hardcoded, and what would switching it have required?

<!-- What specifically was hardcoded in the original script, and what would
     have had to happen to change the threshold or switch formats before
     your refactor? -->

in the original code INPUT_PATH, HIGH_VALUE_THRESHOLD, and OUTPUT_PATH were hardcoded  and it only supported csv file format due to load_csv() function, it doesent support json. 
To change threshold or switch formats before my refactor i need to manually change the code in the file and redeploy it 