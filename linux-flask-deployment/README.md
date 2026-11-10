# Project 1: Deploying a Flask App on Linux

A small Flask application deployed on a Google Cloud Debian VM the way a production service is run: a dedicated unprivileged user, an isolated Python environment, a `systemd` service that restarts itself, and NGINX as a reverse proxy.

## Architecture

```
Client -> NGINX (:80) -> Flask (127.0.0.1:5000), run by systemd as appuser
```

## What was built

| Area | Implementation |
|---|---|
| Environment | Google Compute Engine VM, Debian GNU/Linux 13 (trixie) |
| Service user | `appuser`, a dedicated account with no sudo rights (least privilege) |
| Application | Flask app in `/opt/student-app`, running in a Python virtual environment (`venv`) |
| Process management | `systemd` unit `student-app.service` with automatic restart |
| Reverse proxy | NGINX on port 80 forwarding to `127.0.0.1:5000` |
| Operations | Logs with `journalctl`, ports and processes with `ss` and `ps` |

## Files in this folder

- `app.py`: the Flask application
- `student-app.service`: the systemd unit file
- NGINX site configuration
- `requirements.txt`: Python dependencies

## Key concepts I can explain

- Linux users, UID, groups, GID and what `/etc/passwd` contains
- Why the app listens on `127.0.0.1` and NGINX faces the internet
- The difference between an application, a process, a PID and a TCP port
- What `755` and other permission modes mean
- `systemctl` (control services) vs `journalctl` (read their logs)
- Why `Restart=always` brings a killed process back, and how I proved it

## Useful commands

```bash
systemctl status student-app          # is the service running?
sudo systemctl restart student-app    # restart it
journalctl -u student-app -f          # follow its logs live
ss -lntp | grep 5000                  # which process listens on 5000?
sudo systemctl enable --now student-app nginx   # start now and at boot
```

## Troubleshooting

I deliberately broke the service and diagnosed it using `systemctl status`, `journalctl` and `ss`. Each fix is documented with the evidence that confirmed it.

## Next

The same application is containerised in [../docker-flask-nginx](../docker-flask-nginx/).
