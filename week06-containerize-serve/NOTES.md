# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 142602003
seed: 3739705879

## Built image size

<!-- What image size did `docker images` report for week6-detector? -->

IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
week6-detector:latest   35e3f62e66a8        246MB         60.3MB       
## Swapping in a real checkpoint

<!-- What's the single biggest thing you'd change about this Dockerfile if
     src/mock_detector.py were swapped for a real torch-based checkpoint?
     (Think about what that does to build time and image size.) -->
If src/mock_detector.py were replaced with a real torch-based checkpoint, I would add the required PyTorch and model dependencies to the Docker image and use an appropriate base image. This would significantly increase the Docker image size and build time because PyTorch and its dependencies are much larger than the current lightweight dependencies.