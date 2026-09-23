# Week 7 --- CI/CD Integration Testing

## Objective

The objective of this assignment was to build a CI pipeline that
verifies a vehicle detection application at three levels: linting, unit
testing, and integration testing against the actual Docker container.

The integration test verifies the real built container by starting it,
checking the `/health` endpoint, sending a sample CCTV image to
`/detect`, and confirming that the response contains `"detections"`. The
CI pipeline is designed so that the container-based integration test
runs only after linting and unit tests have passed.

## Setup

Create and activate a virtual environment, then install the required
dependencies:

``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate the personalized synthetic CCTV dataset using the student ID:

``` bash
python generate_for_student.py --student-id 142602003
```

The generated fixtures are stored in:

``` text
data/fixtures/
```

The student ID used for this lab was `142602003`.

## Usage

### Run the Unit Tests

Run the complete test suite:

``` bash
pytest tests/ -q
```

The tests include checks for the application and structural checks for
the CI configuration.

### Run the Integration Test

Make the integration script executable:

``` bash
chmod +x scripts/integration_test.sh
```

Run the container-based integration test:

``` bash
./scripts/integration_test.sh
```

The script performs the following operations:

1.  Builds the Docker image.
2.  Starts the container in detached mode.
3.  Maps host port `8080` to container port `8080`.
4.  Polls the `/health` endpoint until the container responds.
5.  Sends `data/fixtures/camera_A_daylight/000.jpg` to `/detect`.
6.  Checks that the response contains `"detections"`.
7.  Removes the container after the test.

## CI/CD Pipeline

The GitHub Actions workflow contains three jobs:

``` text
lint ──────────────┐
                   ├──> integration-test
unit-test ─────────┘
```

### 1. Lint

The `lint` job installs the project dependencies and runs:

``` bash
flake8 src/
```

### 2. Unit Test

The `unit-test` job installs the dependencies and runs:

``` bash
pytest tests/ -q
```

### 3. Integration Test

The `integration-test` job runs only after both `lint` and `unit-test`
succeed:

``` yaml
needs: ["lint", "unit-test"]
```

It then executes:

``` bash
./scripts/integration_test.sh
```

This prevents CI from spending runner time and Docker resources building
and starting a container when the code has already failed linting or
unit tests.

## Process Followed

1.  Generated the personalized synthetic CCTV fixtures using student ID
    `142602003`.
2.  Completed the GitHub Actions CI workflow with `lint`, `unit-test`,
    and `integration-test` jobs.
3.  Configured `integration-test` to depend on both `lint` and
    `unit-test`.
4.  Completed the Docker-based integration test script.
5.  Tested the CI configuration locally using `pytest tests/ -q`.
6.  Pushed the workflow to GitHub.
7.  Verified the workflow on a real GitHub Actions runner.
8.  Confirmed that all three CI jobs completed successfully.
9.  Recorded the successful GitHub Actions run in `CI_VERIFICATION.md`.

## Results

-   Student ID used for personalized fixtures: **142602003**
-   CI workflow: **Successful**
-   `lint`: **PASS --- 9s**
-   `unit-test`: **PASS --- 15s**
-   `integration-test`: **PASS --- 15s**
-   Total GitHub Actions workflow duration: **37s**
-   Integration test: **Successfully built and tested the Docker
    container**
-   `/health`: **Passed**
-   `/detect`: **Passed and response contained `"detections"`**
-   CI dependency gate: **`integration-test` ran after `lint` and
    `unit-test`**

## CI Verification

The successful GitHub Actions run is documented in `CI_VERIFICATION.md`.

Successful workflow run:

``` text
https://github.com/HemanthKumarBoosumRaju/DS5619-MLOPS/actions/runs/35846789434
```

## Files

The main Week 7 deliverables are:

``` text
.github/workflows/ci.yml
scripts/integration_test.sh
CI_VERIFICATION.md
NOTES.md
```

The Week 7 application and container files used by the CI pipeline are:

``` text
src/app.py
Dockerfile
data/fixtures/
tests/
```
