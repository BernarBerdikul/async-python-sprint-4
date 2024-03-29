start:  # Building Docker images and start
	docker compose -f docker-compose.yml up -d --build

test:  # Start Docker test containers
	docker compose -f docker-compose.test.yml up -d --build

migrate:  # Run migrations
	poetry run alembic upgrade head

localtest:  # start pytest
	poetry run pytest -vv

pre-commit:  # Run pre-commit
	poetry run pre-commit run --all-files
