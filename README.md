## To run:
Clone repository on your computer:
```bash
git clone https://github.com/RynhAleh/rynh-aleh-test-project.git && cd rynh-aleh-test-project
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