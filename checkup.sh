#!/bin/bash
BLB='\033[44m';RDT='\033[91m';GNT='\033[92m';NC='\033[0m\n'

if ! poetry --version; then printf $RDT"Please run 'poetry install' before."$NC; exit 1; fi
if ! cd backend/; then printf $RDT"Can't go to backend/ !!!"$NC; exit 1; fi

printf $BLB'Launching ruff...'$NC
poetry run ruff check .
printf $BLB'Launching mypy...'$NC
poetry run mypy .
printf $BLB'Launching black...'$NC
poetry run black .
printf $BLB'Launching isort...'$NC
poetry run isort .


printf $BLB'Starting test DB...'$NC
docker run -d --name test-db -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=test_password -e POSTGRES_DB=test_db \
  -p 55432:5432 postgres:16

set -e
  
until docker exec test-db pg_isready -U test_user > /dev/null 2>&1; do sleep 1; done

export DATABASE_URL="postgresql+asyncpg://test_user:test_password@localhost:55432/test_db"
export PYTHONPATH=$(pwd)

printf $BLB'Applying migrations...'$NC
poetry run python3 -m alembic upgrade head
printf $BLB'Launching pytest...'$NC
poetry run pytest -v --cov=app

echo 'Destroying test DB...'
docker rm -f test-db
cd ..
printf $GNT'Done.'$NC'\n'