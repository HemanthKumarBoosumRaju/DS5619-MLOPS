# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->

student_id: 142602003
seed: 34416517
Wrote 60 images across 2 camera profiles -> /home2/mlops/Downloads/MLOPSLAB/week10-fairness-audit/data/fixtures
Wrote 238 annotations -> /home2/mlops/Downloads/MLOPSLAB/week10-fairness-audit/data/fixtures/_annotations.coco.json
Sanity-checked recall (using the mock detector, not your fairness_audit.py):
  Bicycle               75.0% <-- below threshold
  Two-wheeler           82.6% <-- below threshold
  Three-wheeler         84.6% <-- below threshold
  LCV                   89.5% <-- below threshold
  Van                   91.7%
  Hatchback             95.0%
  Truck                100.0%
  SUV                  100.0%
  Bus                  100.0%
  Sedan                100.0%
  MUV                  100.0%
  Other                100.0%
  Tempo-traveller      100.0%
  Mini-bus             100.0%

Record this seed in NOTES.md when you submit (see README.md).
## Which classes got flagged?

<!-- Which classes got flagged, and does that match what you'd expect given
     how generate_for_student.py built the fixtures? -->


## If the grouping variable were a protected attribute

<!-- Tying back to the framing note: what would change about this audit's
     stakes and your obligations as an engineer if the grouping variable
     were a protected demographic attribute instead of a vehicle class? -->


## Which attack could corrupt this audit?

<!-- Name one lifecycle stage and attack from the lecture (data poisoning,
     model theft, or adversarial examples) that could silently corrupt THIS
     audit's result, and one control from the lecture that would reduce the
     risk. -->


## Would SHAP or LIME explain a missed detection?

<!-- Pick one missed ground-truth box in a flagged class. An auditor asks
     you to explain WHY the detector missed it, not just that it did. Would
     SHAP or LIME actually help you answer that for a bounding-box detector
     — and if not, what's different about this detector's inputs/outputs
     that breaks the assumption both tools make? -->


## What did your attack show?

<!-- Using fairness_report.json["adversarial"]: at what eps does each flagged
     class fall further? Which class is most fragile, and is it the same
     class the clean audit flagged? Compare the drop ranking
     (most_fragile) with lowest_recall_under_attack — do they agree, and
     which is the better measure of who is hurt? What does that say about who bears the
     cost of an attack (or of an unmonitored failure)? Then: what would
     adversarial training or input validation look like for this detector,
     and why does a rule this simple break so much more easily than a CNN
     (or does it)? -->
