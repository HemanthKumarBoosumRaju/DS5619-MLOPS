# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 142602003
seed: 3115386422


## Which candidate reached Production, and why?

<!-- Which candidate ended up in Production, and why? -->
Candidate B reached Production because it had a completed model card and its F1 score was 0.835, which is above the Production threshold of 0.70. Candidate A was blocked because its F1 score was 0.544, which is below the required threshold. Candidate A was also initially blocked because it did not have a model card

## Gating stale feature data

<!-- What would you need to add to promote_model's gate if you also wanted
     to block promotion of a model trained on stale (e.g. >30-day-old)
     feature data? -->

We would need to store the feature data timestamp or age in the model's metadata and then check whether the feature data is older than 30 days. If it is, promotion to production would be blocked with a GovernanceError.

if feature_data_age_days > 30:
raise GovernanceError("Production promotion blocked: feature data is older than 30 days")


## Scaling the gate to 40 candidates

<!-- Tying back to this week's AutoML/HPO framing: if a hyperparameter
     search had handed you 40 candidates instead of 2, what in your
     register_model/promote_model design would need to change (or
     genuinely wouldn't) to gate 40 instead of 2? -->
The current design already supports multiple candidates because `register_model` creates a new version for each registered model, and `promote_model` applies the governance checks to the specific model version being promoted. Therefore, the basic governance gate does not need to change just because there are 40 candidates.

For 40 AutoML/HPO candidates, I would register each candidate as a separate model version with its metrics and generate a model card for each one. The pipeline could then apply the same `promote_model` checks to each candidate.

Main addition will be ranking or selection step to compare the 40 candidates and identify the strongest candidates for promotion. The governance rules themselves should remain the same and be applied consistently to every candidate.