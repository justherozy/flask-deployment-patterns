# Host-based deployment: Flask on Linux with systemd and NGINX

A Flask service run the way a traditional host-based service is run: a dedicated unprivileged account, an isolated Python environment, a `systemd` unit that restarts it on failure, and NGINX as the only component facing the network.

```
Client -> NGINX (:80) -> Flask (127.0.0.1:5000), supervised by systemd as appuser
```

## Components

| Area | Implementation |
|---|---|
| Platform | Google Compute Engine VM, Debian GNU/Linux 13 |
| Service account | `appuser`, no sudo rights (least privilege) |
| Application | `/opt/student-app`, Python virtual environment in `venv/` |
| Supervision | `student-app.service`, `Restart=always`, starts after `network.target`, enabled at boot |
| Reverse proxy | NGINX on port 80, `proxy_pass http://127.0.0.1:5000`, forwards `Host` and `X-Real-IP` |

## Files

| File | Purpose |
|---|---|
| `app.py` | Flask application; `/` and `/health`; binds `127.0.0.1:5000` |
| `student-app.service` | systemd unit: runs the venv's Python as `appuser` from `/opt/student-app` |
| `nginx-student-app.conf` | NGINX site configuration (the reverse proxy) |
| `requirements.txt` | Python dependencies |

## Design notes

- **Loopback binding.** Flask listens on `127.0.0.1`, so the only way in from the network is through NGINX. A direct request to port 5000 from outside the VM fails.
- **Least privilege.** The unit runs as `appuser`, so a compromise of the app does not grant root.
- **Self-healing.** `Restart=always` brings the process back after a crash or `kill`; this was verified by killing the process and watching `systemd` start a new PID.
- **Separation of concerns.** NGINX handles the public interface (and is where TLS would be added); `systemd` handles the process lifecycle; Flask handles requests.

## Operations

```bash
systemctl status student-app                    # state, PID, recent log lines
sudo systemctl restart student-app              # restart the service
journalctl -u student-app -f                    # follow logs
ss -lntp | grep -E ':80|:5000'                  # who is listening where
sudo nginx -t && sudo systemctl reload nginx    # validate then apply proxy config
sudo systemctl enable --now student-app nginx   # start now and at every boot
```

## Limitations

Flask's development server is used rather than a WSGI server such as `gunicorn`; there is no TLS; the unit file has no sandboxing directives (`NoNewPrivileges`, `ProtectSystem`, and similar). See the hardening roadmap in the [repository README](../README.md).

## Next

The same service, containerised: [`../docker-flask-nginx`](../docker-flask-nginx/).
