# k-Aufgaben

A tool for managing math exercises ("Aufgaben"). Users can register, browse, and add exercises with metadata such as subject, level, difficulty, and file path.

## Status

Early skeleton. The database models, connection helpers, and menu structure are in place; the main CLI logic is not yet implemented.

## Features

- SQLAlchemy ORM models for users and exercises
- PostgreSQL connection helpers with connection testing
- Interactive credential prompts powered by [questionary](https://github.com/tmbo/questionary)
- Rich console output

## Project structure

```
main.py               # Entry point: banner and main loop
firstMenu.py          # Database connection menu (new / saved DB)
tools.py              # Input validators and credential prompt helpers
DB.py                 # Database class: URL building, JSON saving, connectivity test
databaseStructure.py  # SQLAlchemy models (User, Exercise)
test.py               # REPL demo / playground script
```

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Requires a PostgreSQL database.

## Database models

- **User**: email, username, hashed password, names, admin flag, timestamps
- **Exercise**: title, subjects, level, difficulty (1–5), file path, comment, author (FK to User)

## License

MIT — see [LICENSE](LICENSE).
