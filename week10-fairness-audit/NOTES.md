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

## Which classes got flagged?

<!-- Which classes got flagged, and does that match what you'd expect given
     how generate_for_student.py built the fixtures? -->

The clean audit flagged four classes below 90% recall:

Bicycle: 75.0% (12/16)

Two-wheeler: 82.6% (19/23)

Three-wheeler: 84.6% (11/13)

LCV: 89.5% (17/19)

This is expected because smaller vehicles have smaller bounding boxes and fewer visible pixels, making them harder to detect. LCV's result is close to the threshold, so it could partly be sampling noise because each class has relatively few examples


## If the grouping variable were a protected attribute

<!-- Tying back to the framing note: what would change about this audit's
     stakes and your obligations as an engineer if the grouping variable
     were a protected demographic attribute instead of a vehicle class? -->

If the groups represented demographic attributes instead of vehicle classes, poor performance could unfairly affect certain groups of people.

As an engineer, I would need to:

Investigate the causes of the disparity.
Check the quality and representation of the data.
Assess possible harm and document limitations.
Follow relevant privacy and legal requirements.

Such disparities should not be dismissed as noise without proper investigation because they could affect people's rights or access to services.
## Which attack could corrupt this audit?

<!-- Name one lifecycle stage and attack from the lecture (data poisoning,
     model theft, or adversarial examples) that could silently corrupt THIS
     audit's result, and one control from the lecture that would reduce the
     risk. -->

Attack: Data poisoning

An attacker could change images or ground-truth annotations.
For example, removing some Bicycle annotations could make the reported recall misleading.
This could lead engineers to believe that the detector performs better than it actually does.

Control:

Use checksums to detect unexpected file changes.
Restrict access to datasets.
Validate annotations against trusted source files.

## Would SHAP or LIME explain a missed detection?

<!-- Pick one missed ground-truth box in a flagged class. An auditor asks
     you to explain WHY the detector missed it, not just that it did. Would
     SHAP or LIME actually help you answer that for a bounding-box detector
     — and if not, what's different about this detector's inputs/outputs
     that breaks the assumption both tools make? -->

SHAP and LIME cannot directly explain a missed detection without a suitable explanation setup.
They need a clearly defined model output to explain.

Object detectors produce a variable number of bounding boxes, class labels, and confidence scores, so we must first define which output we want to explain.

Our mock detector uses fixed colour thresholds rather than a learned neural network.
Therefore, inspecting the pixel values, colour mask, and bounding-box overlap is more direct.

Eg: If a Bicycle is missed, I would check whether its pixel colours satisfy the detector's colour rule and whether a detection overlaps its ground-truth bounding box sufficiently.

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

The attack changes image colours by lowering red and increasing green and blue. Epsilon (ε) controls the maximum change to each colour channel.

The pipeline tested ε = 0, 10, 20, 30, and 40.

Results at ε = 20

Bicycle: Clean recall = 75%, attacked recall = 25%. Drop = 50 percentage points.
Truck: Clean recall = 100%, attacked recall ≈ 71%. Drop = 29 percentage points.
Two-wheeler: Clean recall ≈ 83%, attacked recall ≈ 61%. Drop = 22 percentage points.

What do these results mean?

Bicycle had the largest recall drop and the lowest final recall.
Truck started at 100% recall but became vulnerable under attack.
Two-wheeler also experienced a significant decline.
The largest-drop ranking identifies classes that deteriorate most. The lowest-recall ranking identifies classes that perform worst after the attack.

How can we reduce the risk?

Adversarial training: For a learned detector, train using perturbed images with correct annotations and test whether performance improves.

Input validation: Check image formats, dimensions, and pixel ranges to reject malformed inputs.

Our mock detector is vulnerable because it depends directly on pixel colours. Small colour changes can break its rule. This does not prove that every CNN is more robust; robustness depends on the model, training data, and attack.