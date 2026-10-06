Lab 9 — Orchestrated Batch Scoring
Purpose

This lab demonstrates how a simple DAG (Directed Acyclic Graph) can be used to run machine learning batch-scoring tasks in the correct order.

The main goals were:

Run tasks according to their dependencies.

Handle branching in a DAG.

Detect missing dependencies and dependency cycles.

Retry tasks that fail temporarily.

Stop the DAG when a task permanently fails.

Share information between tasks using a common context.

Understand how retry decisions can affect cost.

DAG Used

The pipeline has four tasks:

extract
   |
   v
 score
 /    \
v      v
load  notify


extract finds all images in data/fixtures/.

score runs the vehicle detector on the images and counts detections.

load writes the results to batch_report.json.

notify represents a flaky API/webhook call. It fails twice and succeeds on the third attempt.

load and notify are independent branches because both depend on score, but neither depends on the other.

What I Implemented

I completed the three functions in:

src/mini_orchestrator.py

1. topological_order()

This finds a valid order for running the tasks while respecting their dependencies.

It also:

Detects missing dependencies.

Detects dependency cycles.

Handles branching DAGs.

2. run_task_with_retry()

This runs a task and retries it when it fails.

The number of additional attempts is controlled by max_retries.

For example, if:

max_retries = 2


the task can run up to three times in total.

3. run_dag()

This runs the complete DAG using the correct task order.

It:

Passes the same context to every task.

Records the status and number of attempts.

Stops when a task fails permanently.

Does not run downstream tasks after an unrecoverable failure.

Setup

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate


Install the required packages:

pip install -r requirements.txt

Generate the Dataset

Generate the personalized fixture images using the student ID:

python generate_for_student.py --student-id 142602003


This creates the images used by the batch-scoring pipeline in:

data/fixtures/


The fixtures should not be edited manually.

Run the Tests

Run the provided self-check:

pytest tests/ -q


The tests check:

Correct task ordering.

Branching DAGs.

Cycle detection.

Missing dependency detection.

Retry behaviour.

Context sharing.

Stopping after a failed task.

The complete pipeline.

Run the Pipeline

Run:

python src/run_pipeline.py


The pipeline runs the tasks in dependency order.

It creates:

batch_report.json
dag_run_summary.json


batch_report.json contains the batch-scoring results.

dag_run_summary.json contains the DAG execution order and the result of each task.

Retry Behaviour

The notify task is intentionally designed to fail twice and then succeed.

Therefore, the expected result is:

notify
status: success
attempts: 3


This demonstrates that a temporary failure can be handled by retrying the task instead of immediately failing the whole DAG.

Branch Independence

load and notify are sibling tasks. Both depend on score.

Therefore, a failure in notify does not prevent load from running because load does not depend on notify.

This demonstrates that a failure in one branch should not automatically stop an unrelated branch of the DAG.

FinOps and Retry Cost

If notify were a paid API call, retries could increase the cost because every attempt would be another API call.

For this reason, I would use fewer retries and possibly a longer delay between attempts for an expensive API call. I would retry mainly when the failure is likely to be temporary.

Using the same retry settings for every task is risky because tasks have different costs and failure types. A cheap local task can be retried more, while an expensive API call should have fewer retries.

The retry strategy should balance reliability and cost.

Reproducing the Lab

A fresh setup can reproduce the work with:

git clone <repository-url>
cd <repository-directory>

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python generate_for_student.py --student-id 142602003

pytest tests/ -q

python src/run_pipeline.py


After the pipeline finishes, the following files should be available:

batch_report.json
dag_run_summary.json


The dag_run_summary.json should show that notify succeeded after three attempts.

Files
src/
├── mini_orchestrator.py   # DAG and retry implementation
├── mock_detector.py       # Provided detector
└── run_pipeline.py        # Pipeline driver

data/
└── fixtures/              # Generated input images

batch_report.json          # Batch-scoring output
dag_run_summary.json       # DAG execution summary
NOTES.md                   # Lab observations and FinOps reasoning
README.md                  # Project documentation