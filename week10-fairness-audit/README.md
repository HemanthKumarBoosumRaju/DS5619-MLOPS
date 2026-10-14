# Week 10: Fairness and Robustness Audit

**Course:** DS5619 Machine Learning Systems Operations  
**Track:** BMD-45 Vehicle Detection

## 1. Purpose of the Experiment

This experiment checks whether a vehicle detector performs poorly for certain vehicle classes and whether its performance decreases when images are deliberately modified.

The experiment focuses on two questions:

- **Fairness:** Are some vehicle classes harder to detect than others?
- **Robustness:** How does detection performance change when image colours are perturbed?

## 2. What I Implemented

I completed the TODO functions in `src/fairness_audit.py` and `src/adversarial.py`.

### `src/fairness_audit.py`

- `compute_iou()`: Calculates the overlap between two bounding boxes.
- `match_ground_truth()`: Checks whether each ground-truth vehicle was detected.
- `audit_by_category()`: Calculates recall separately for each vehicle class.
- `find_underperforming_categories()`: Identifies classes with recall below the threshold.

### `src/adversarial.py`

- `perturb_image()`: Lowers red-channel values and increases green and blue values within the specified perturbation limit.
- `audit_under_attack()`: Evaluates recall at different attack strengths.
- `find_most_fragile()`: Ranks classes by their decrease in recall.

I used the provided `mock_detector.py` and `run_pipeline.py` without modifying them.

## 3. Project Structure

```text
week10-fairness-audit/
├── data/
│   └── fixtures/
│       ├── camera_A_daylight/
│       ├── camera_B_lowlight/
│       └── _annotations.coco.json
├── src/
│   ├── adversarial.py
│   ├── fairness_audit.py
│   ├── mock_detector.py
│   └── run_pipeline.py
├── tests/
├── .gitignore
├── fairness_report.json
├── generate_for_student.py
├── NOTES.md
├── prep_data.py
├── README.md
├── README.pdf
└── requirements.txt
```

### Purpose of the Files

- `data/fixtures/`: Contains generated vehicle images from two camera profiles and their annotations.
- `_annotations.coco.json`: Stores ground-truth vehicle classes and bounding boxes.
- `src/fairness_audit.py`: Implements the fairness audit and recall calculations.
- `src/adversarial.py`: Implements image perturbations and robustness evaluation.
- `src/mock_detector.py`: Provides the colour-rule-based detector.
- `src/run_pipeline.py`: Runs both audits and generates the report.
- `tests/`: Contains automated tests for checking the implementation.
- `generate_for_student.py`: Generates personalized images using the student ID.
- `fairness_report.json`: Stores clean audit and adversarial results.
- `NOTES.md`: Records the student ID, findings, fairness considerations, and attack analysis.
- `requirements.txt`: Lists the required Python packages.
- `.gitignore`: Specifies files Git should ignore.
- `prep_data.py`: Older preparation script, superseded by `generate_for_student.py`. Do not use it for this experiment.
- `README.md`: Documents the experiment and reproduction steps.
- `README.pdf`: PDF documentation, if required for submission.

## 4. Clean Fairness Audit Results

The audit uses recall to measure how many actual vehicles were detected.

**Recall = Detected ground-truth vehicles / Total ground-truth vehicles × 100**

The threshold for flagging a class is 90% recall. Four classes were flagged:

- **Bicycle:** 12/16 = 75.0%
- **Two-wheeler:** 19/23 = 82.6%
- **Three-wheeler:** 11/13 = 84.6%
- **LCV:** 17/19 = 89.5%

Smaller vehicles generally have smaller bounding boxes and fewer visible pixels, making them harder to detect. LCV's result is close to the threshold and could partly be due to the small number of examples.

## 5. Adversarial Audit Results

The experiment tested epsilon values of 0, 10, 20, 30, and 40. Epsilon controls the maximum change to each colour channel.

At epsilon = 20:

- **Bicycle:** Recall fell from 75% to 25%, a drop of 50 percentage points.
- **Truck:** Recall fell from 100% to approximately 71%, a drop of 29 percentage points.
- **Two-wheeler:** Recall fell from approximately 83% to 61%, a drop of 22 percentage points.

Bicycle was the most fragile class at epsilon = 20. Truck was not flagged in the clean audit but suffered a substantial recall decrease under attack.

The largest-drop ranking identifies classes that deteriorate most relative to their clean performance. The lowest-recall ranking identifies classes with the worst final recall under attack. Both measures are useful for understanding different types of failure.

## 6. What I Recorded in `NOTES.md`

The notes cover:

- Why certain vehicle classes have lower recall.
- How fairness audits become more important when comparing demographic groups.
- How data poisoning could corrupt audit results and how dataset integrity checks can reduce the risk.
- Why SHAP and LIME need a suitable explanation target for bounding-box detectors.
- How adversarial attacks affect recall and how adversarial training and input validation could reduce risks.

## 7. How to Reproduce the Experiment

Run the following commands in Windows PowerShell from the `week10-fairness-audit` directory.

### Step 1: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 2: Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Generate the dataset

```powershell
python generate_for_student.py --student-id 142602003
```

This generates personalized synthetic images and annotations. The student ID must match the value recorded in `NOTES.md`. Regenerating the dataset overwrites the existing fixtures.

### Step 5: Run the tests

```powershell
pytest tests/ -q
```

The tests check whether the implementation behaves as expected.

### Step 6: Run the complete pipeline

```powershell
python src/run_pipeline.py
```

The pipeline:

1. Runs the detector on the generated images.
2. Calculates recall for each vehicle class.
3. Identifies underperforming classes.
4. Evaluates recall under different perturbation strengths.
5. Writes the results to `fairness_report.json`.

## 8. Conclusion

The experiment showed that detection performance differs across vehicle classes and that image perturbations can significantly reduce recall.

The clean audit identified classes that were already difficult to detect, while the adversarial audit revealed additional weaknesses, including a substantial recall drop for Truck.

Evaluating both clean performance and performance under attack helps identify underperforming classes and assess the robustness of a detection system.

**Note:** The detector used in this lab is a simple colour-rule-based mock detector. Its results demonstrate the audit methods and the effect of the chosen perturbation, but they should not be treated as representative measurements of a real vehicle-detection model.