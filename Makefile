run.jarbas:
	docker-compose pull
	docker-compose up -d --build
	docker-compose run --rm jarbas python manage.py ceapdatasets
	docker-compose run --rm jarbas python manage.py migrate

seed.sample: run.jarbas
	docker-compose run --rm jarbas python manage.py reimbursements contrib/sample-data/reimbursements_sample.xz
	docker-compose run --rm jarbas python manage.py companies contrib/sample-data/companies_sample.xz
	docker-compose run --rm jarbas python manage.py irregularities contrib/sample-data/irregularities_sample.xz

