run.jarbas:
	docker-compose -f docker-compose-dev.yml up -d --build
	docker exec jarbas_jarbas python manage.py ceapdatasets
	docker exec jarbas_jarbas python manage.py migrate


collectstatic: run.jarbas
	docker exec jarbas_jarbas python manage.py collectstatic --no-input

seed: run.jarbas
	docker exec jarbas_jarbas python manage.py reimbursements /tmp/serenata-data/reimbursements.xz
	docker exec jarbas_jarbas python manage.py companies /tmp/serenata-data/2016-09-03-companies.xz
	docker exec jarbas_jarbas python manage.py irregularities /tmp/serenata-data/irregularities.xz

run.devel: collectstatic

build.elm:
	docker-compose -f docker-compose-dev.yml run elm

stop.jarbas:
	docker-compose -f docker-compose-dev.yml down
