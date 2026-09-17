# Docker verification

Fill this in after you build and run your container (see README.md,
"Part 2 — Dockerfile"). This is how we confirm your container actually works, since an
automated grader running in a sandbox may not always have Docker-in-Docker
available.

## Build

Paste the command you ran and its final output line (the one showing the
built image ID/tag):

docker build -t week6-detector .

docker.io/library/week6-detector:latest

```
TODO
```

## Run

Paste the command you used to start the container (should map a host port
to the container's 8080):

```
TODO
```
docker run --rm -p 8080:8080 week6-detector
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.17.0.2:8080
Press CTRL+C to quit
172.17.0.1 - - [17/Sep/2026 16:48:57] "GET /health HTTP/1.1" 200 -
172.17.0.1 - - [17/Sep/2026 16:50:18] "POST /detect HTTP/1.1" 200 -
172.17.0.1 - - [17/Sep/2026 16:57:05] "GET /health HTTP/1.1" 200 -
## Verify

Paste the exact `curl` commands and their JSON output for both endpoints,
run against the running container (not against `python src/app.py` directly
— the point is to prove the *container* works):

```
TODO: curl http://localhost:PORT/health
TODO: <paste JSON response>

TODO: curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:PORT/detect
TODO: <paste JSON response>
```
curl.exe http://localhost:8080/health

{"status":"ok"}

curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect

{"count":3,"detections":[{"bbox":[61,33,18,22],"category_id":4,"id":0,"image_id":0,"score":0.98},{"bbox":[91,52,22,17],"category_id":10,"id":1,"image_id":0,"score":0.98},{"bbox":[36,66,44,16],"category_id":4,"id":2,"image_id":0,"score":0.98}]}