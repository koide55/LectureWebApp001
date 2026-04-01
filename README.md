# vuln-webapp

Flask based lecture scaffold for authentication and web security exercises.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m app.db.seed
python3 run.py
```

## Default users

- `alice / alicepass`
- `bob / bobpass`
- `admin / adminpass`

## Auth modes

- `cookie`
- `server_session`

`AUTH_MODE` sets the default mode.
You can also switch modes from the page header, which logs the current user out.

## Useful flags

- `ENABLE_VULN_SQLI=true` sets the default `/users` mode to vulnerable.
- `ENABLE_VULN_STORED_XSS=true` sets the default `/board` mode to vulnerable.
- `ENABLE_CSRF_PROTECTION=true` sets the default CSRF protection mode to enabled.
- `ENABLE_VULN_REFLECTED_XSS=true` sets the default `/reflect` mode to vulnerable.
- `ENABLE_VULN_COMMAND_INJECTION=true` sets the default `/ping` mode to vulnerable.

All lab modes can be switched from `/lab-settings`.

## CSRF demo server

Run the main app on one port and the attacker server on another:

```bash
python3 run.py
python3 csrf_demo_server.py
```

Optional settings:

- `ATTACKER_HOST` default: `127.0.0.1`
- `ATTACKER_PORT` default: `5001`
- `TARGET_BASE` default: `http://127.0.0.1:5000`

Example:

```bash
ATTACKER_HOST=localhost TARGET_BASE=http://127.0.0.1:5000 python3 csrf_demo_server.py
```

Note:

- Different ports are different origins, so CSRF can still be demonstrated.
- But `http://127.0.0.1:5000` and `http://127.0.0.1:5001` are still same-site for SameSite cookie behavior.
- To demonstrate SameSite blocking, use different hostnames such as `127.0.0.1` and `localhost`.
