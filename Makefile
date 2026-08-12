alembic_create_table:
	alembic revision --autogenerate -m "create table"
	alembic upgrade head  

run_dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build