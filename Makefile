test:
	pytest -vv

up:
	docker-compose up

up-d:
	docker-compose up --build

up-dd:
	docker-compose up --build -d

clear:
	rm -Rf GOOGLE_SPREADSHEET_WORKSHEET_ID
	rm -Rf GOOGLE_SPREADSHEET_UPLOAD_FILE_ID

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down

down-v:
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
	python -m src

runc:
	@make clear
	python -m src

req:
	pip freeze > requirements.txt

venv:
	python -m venv .venv
	chmod 777 .venv/bin/activate
	source ./.venv/bin/activate

deactivate:
	deactivate

pip-e:
	pip install -e .
	pip install -r requirements.txt