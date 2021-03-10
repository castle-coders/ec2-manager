
install-requirements:
	pip install -r requirements.txt

freeze-requirements:
	pip freeze > requirements.txt

service-docker:
	docker build -f build/service/Dockerfile -t docker.local.pw10n.pw/ec2manager:latest .

staticassets:
	rm -rf build/staticassets/static
	cd managersite && DATABASE_URL='' python manage.py collectstatic --noinput && mv managersite/settings/static ../build/staticassets

staticassets-docker: staticassets
	docker build -f build/staticassets/Dockerfile -t docker.local.pw10n.pw/ec2manager-staticassets:latest .

clean:
	rm -rf build/.staticassets/static