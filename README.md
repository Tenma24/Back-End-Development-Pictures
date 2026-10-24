# Back-End-Development-Pictures

Flask REST service with the original IBM seed data and all 11 IBM tests passing.

```sh
python -m pip install -r requirements.txt
python -m pytest -v
waitress-serve --listen=127.0.0.1:8081 backend:app
```

Endpoints: GET /health, GET /count, GET/POST /picture, GET/PUT/DELETE /picture/<id>.
The course uses an in-memory picture list; changes reset when the service restarts.
Duplicate POST returns 302 to match the course tests.

## Source

Based on the [official IBM Skills Network starter](https://github.com/ibm-developer-skills-network/luggb-Back-End-Development-Pictures). Original starter history and course fixtures are retained.
