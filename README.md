## To run:
Clone repository on your computer:
```bash
git clone https://github.com/RynhAleh/rynh-aleh-test-project.git && cd rynh-aleh-test-project
```
Clone secrets, if you don't have your own:
```bash
cp .env.example .env --update=none
```
To arrange development environment on your machine:
```bash
cd backend/ && \
poetry config virtualenvs.in-project true --local && \
poetry install && \
cd ..
```
To launch linters and tests before deployment (in dev environment):
```bash
./checkup.sh
```
Run / deploy:
```bash
docker-compose up --build -d
```

The project is configured for easy evaluation (Development Mode):
- Frontend runs on port 3000.
- Backend runs on port 8000.
- Database runs on port 5432.

Navigation supports back button via React Router.
For testing, use curl as in the task.
Unique selects in Page3 fetch all possible names by querying history with today's date (minimal, no extra endpoint).

*Note: For a real production environment, I would set up Nginx as a reverse proxy, configure SSL (Let's Encrypt), and use multi-stage Docker builds to serve static frontend files.*

#### MVP vs Current version:
- main.py -> layered (core/config, db/session, api/routers, services/crud, schemas), connected routers via APIRouter
- Base.metadata.create_all() -> replaced with Alembic/SQLAlchemy migrations (docker command at the start of the service) so that the scheme is manageable and portable
- pip, requirements.txt -> switched to Poetry with pyproject.toml/poetry.lock, fixed versions and dev dependencies (uvicorn, ruff, black, mypy, isort, pytest)
- Tests -> tests added with coverage and creation of a test database (using all Alembic migrations)
- Linters -> linters added (ruff, mypy, black, isort)