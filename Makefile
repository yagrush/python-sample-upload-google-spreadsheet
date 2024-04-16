test:
	pytest -vv

up:
	docker-compose up

up-d:
	docker-compose up --build

up-dd:
	docker-compose up --build -d

clear:
	rm -Rf app/GOOGLE_* app/__pycache__/

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down
	@make rm-vol

rm:
	docker-compose rm

rm-vol:
	docker volume rm python-sample-upload-google-spreadsheet_vol-app-python-sample-upload-google-spreadsheet

log:
	docker-compose logs -f

sh-app:
	docker container exec -it app-python-sample-upload-google-spreadsheet bash

docker-prune:
	docker system prune -a

run:
	python -m app

req:
	pip freeze > requirements.txt