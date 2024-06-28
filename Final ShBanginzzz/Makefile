
migrate:
	docker compose run -it web poetry run python manage.py migrate

migrations:
	docker compose run -it web poetry run python manage.py makemigrations

runserver: migrations migrate
	docker compose run -it -p 8000:8000 web
