docker-compose-file  ?= docker-compose-prod.yml

run.jarbas.devel:
	docker-compose up -d --build
	docker-compose run --rm jarbas python manage.py ceapdatasets
	docker-compose run --rm jarbas python manage.py migrate

run.jarbas:
	docker-compose -f $(docker-compose-file) pull
	docker-compose -f $(docker-compose-file) up -d --build
	docker-compose -f $(docker-compose-file) run --rm jarbas python manage.py ceapdatasets
	docker-compose -f $(docker-compose-file) run --rm jarbas python manage.py migrate

seed.sample: run.jarbas
	docker-compose run --rm jarbas python manage.py reimbursements contrib/sample-data/reimbursements_sample.xz
	docker-compose run --rm jarbas python manage.py companies contrib/sample-data/companies_sample.xz
	docker-compose run --rm jarbas python manage.py irregularities contrib/sample-data/irregularities_sample.xz

run.devel: run.jarbas.devel

run: run.jarbas
