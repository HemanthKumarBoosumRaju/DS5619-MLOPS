# NOTES.md — Week 8: Drift and Observability Monitoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 142602003
seed: 3455375467

## Drift level vs. expectation

<!-- What drift level did the report show, and does that match what you'd
     expect given the two cameras were built with deliberately different
     visual statistics? -->
PSI = 0.1303, so the drift level is moderate.

This is expected because the two cameras have different visual conditions, so their confidence scores are different.

## What confidence-score-only monitoring misses

<!-- What would you monitor IN ADDITION to confidence score if you had
     access to ground-truth labels a day later? (Tie this to the kinds of
     drift from the lecture — which one does confidence-score-only
     monitoring miss?) -->
If ground truth labels are available, I would also monitor precision, recall, F1-score, and mAP by comparing the model's predictions with the ground truth labels.

Confidence scores  only detects detect changes in the distribution of prediction confidence so it misses all cases where the model's predictions become incorrect.

This is called concept drift  where the correct output changes even though the confidence scores remain similar because model may produce confidence scores with a similar distribution while its actual prediction accuracy decreases