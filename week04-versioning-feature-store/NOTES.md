# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
142602003

## v1 vs. v2 manifest comparison

<!-- What's different between the v1 and v2 feature group's manifest.json?
     (Look at both.) -->
the v1 and v2 feature groups are both named card_activity but they are stored as separate feature group versions.

The v1 feature group has:

feature_group_version_id: v1
source_raw_version_id: v1
transform_version: v1
row_count: 379

The v2 feature group has:

feature_group_version_id: v2
source_raw_version_id: v2
transform_version: v1
row_count: 118

but the raw source schemas are different. in v1 the transaction data contains amount and country. in v2 these are changed to amount_minor_units and country_code, and a new device_fingerprint field is added.

due to this the schema change creates a new raw data version and a new feature-group version instead of overwriting the existing v1 history.feature-group v1 is linked to raw v1, while feature-group v2 is linked to raw v2.
## Why treat amount_minor_units differently from amount?

<!-- Why does build_features need to treat amount_minor_units differently
     from amount for the aggregates to be comparable across versions? -->
in v1 amount is stored in normal units while v2 stores the amount in cents using amount_minor_units
so build_features divides amount_minor_units by 100 before calculating so it converts v2 amounts to the same unit as v1
without this conversion the v2 avg_amount and max_amount values would be 100 times larger and would not be comparable with v1