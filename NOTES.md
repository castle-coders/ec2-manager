new plan 
https://www.digitalocean.com/community/tutorials/how-to-build-a-django-and-gunicorn-application-with-docker

1. gunicorn container, only hosts app
2. nginx container, only static files
3. kubernetes two separate deployments
4. ingress route maps /static to nginx
5. everything else goes to gunicorn

