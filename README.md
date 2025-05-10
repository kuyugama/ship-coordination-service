# _# FastAPI Boilerplate_
> By Kuyugama (Of course)

This FastAPI boilerplate uses asynchronous SQLAlchemy to work with database and pytest to test endpoints

## Structure
```
┌─ fastapi-boilerplate -- Project directory
└──┌─ src
   │  ├─ models -- SQLAlchemy models
   │  ├─ route -- Root route
   │  │  ├─ service.py -- General business logic
   │  │  ├─ dependencies.py -- General dependencies(Such as token validation)
   │  │  ├─ errors.py -- General errors
   │  │  └─ auth -- Subroute
   │  ├─ constants -- Service constants
   │  ├─ util -- Utility functions
   │  ├─ schema -- Schemas of responses as Pydantic models
   │  ├─ error.py -- Powerfull error class
   │  ├─ error_handlers.py -- FastAPI error handlers
   │  ├─ make_app.py -- Function to create FastAPI app
   │  ├─ session_holder.py -- Global database connection holder
   │  └─ protocols.py -- typing.Protocol subclasses 
   ├─ tests -- Tests
   ├─ alembic -- Alembic revisions
   ├─ main.py -- Create and optionally run the FastAPI app
   ├─ alembic.ini -- Alembic configuration
   ├─ Dockerfile -- Dockerfile to build and run this boilerplate inside docker
   ├─ docker-compose.yaml -- Docker compose file to run this boilerplate with one command(requires environment variables)
   ├─ .secrets.yaml -- Service secrets (e.g. access tokens, encrypting keys, database urls)
   └─ settings.yaml -- Service settings
```

### Start FastAPI project using this boilerplate
1. Clone this repository
2. Update details in pyproject.toml
3. Install requirements (`pip install -r requirements.txt` / `uv sync`)
4. Set your `sqlalchemy.url` in `.secrets.yaml`
5. Set `app.title` and `app.version` in `settings.yaml`
6. Run?
