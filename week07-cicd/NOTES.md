# NOTES.md — Week 7: CI/CD Integration Testing

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 142602003
seed: 2899447215

## Why gate integration-test on needs: [lint, unit-test]?

<!-- Why does integration-test need needs: [lint, unit-test] instead of
     just running in parallel with them — what's the actual cost being
     avoided? -->
integration test needs needs: [lint, unit-test] so that the Docker build and
container based integration test only run after linting and unit tests pass.
Building and running the Docker container consumes CI runner time and Docker
resources, so the needs gate avoids spending those resources when the code
already failed linting or unit tests.