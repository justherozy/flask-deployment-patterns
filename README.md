# DevOps Portfolio: Linux to Docker

Hands-on projects where I deploy the same Flask web application two ways on Google Cloud: first **directly on Linux** (systemd and NGINX), then **containerised with Docker and Docker Compose**. Each project has its own write-up with commands, explanations, real output, screenshots and troubleshooting notes.

**Author:** Henry Oribe

## Projects

| # | Project | What it demonstrates | Write-up |
|---|---|---|---|
| 1 | **Flask on Linux** | Least-privilege service user, Python virtual environment, `systemd` service with automatic restart, NGINX reverse proxy, logs with `journalctl`, process and port inspection | [linux-flask-deployment](linux-flask-deployment/) |
| 2 | **Flask + NGINX in Docker** | Dockerfile and image layers, build caching, port publishing, environment variables, custom networks and DNS, volumes, restart policies, Docker Compose | [docker-flask-nginx](docker-flask-nginx/) |
| 3 | Kubernetes *(planned)* | The same application on Kubernetes | Coming next |

## Architecture

**Project 1: directly on Linux**
```
Client -> NGINX (:80) -> Flask (127.0.0.1:5000), managed by systemd
```

**Project 2: containerised**
```
Client -> NGINX container (:80) -> Docker network (DNS) -> Flask container (:5000)
                                                              |
                                                       Docker volume (/data)
```
Only NGINX is published to the internet; the Flask container is reachable only through it.

## Skills demonstrated

- **Linux:** users and groups, file permissions, `systemd`, `journalctl`, `ss`, process management
- **Web serving:** NGINX reverse proxy, HTTP status codes (502 diagnosis)
- **Containers:** Dockerfile authoring, image layers and caching, `docker run/exec/logs/inspect`
- **Networking:** port publishing, bridge networks, container DNS, why `0.0.0.0` matters inside containers
- **Storage:** ephemeral container storage vs volumes vs bind mounts
- **Orchestration basics:** Docker Compose, restart policies, service dependencies
- **Cloud:** Google Compute Engine, VPC firewall rules
- **Troubleshooting:** working from the outside in, and reading `curl` exit codes (7 vs 56)

## Tech stack

`Python 3` · `Flask` · `NGINX` · `Docker Engine` · `Docker Compose` · `systemd` · `Debian 13` · `Google Cloud (Compute Engine)`

## How to run the Docker project

```bash
git clone https://github.com/justherozy/devops-portfolio.git
cd devops-portfolio/docker-flask-nginx
docker compose up -d --build
curl http://localhost
```
Expected response: `Hello from my Docker container! Environment:production`

Stop it with `docker compose down`.

## What I would add next

HTTPS with a certificate, a non-root `USER` in the Dockerfile, a production WSGI server (gunicorn), image vulnerability scanning, a CI pipeline to build and test the image, then Kubernetes.
