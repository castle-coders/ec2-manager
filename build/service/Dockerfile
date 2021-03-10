FROM python:3-slim

# Create a group and user to run our app
ARG APP_USER=managerapp
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
COPY requirements.txt /requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
# ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn
RUN pip install pymysql

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
WORKDIR /
COPY managersite /
COPY build/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

# uWSGI will lißsten on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=managersite.settings.prod

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN DATABASE_URL='' python manage.py collectstatic --noinput

#TODO: Exclude static

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start uWSGI
CMD ["gunicorn", "-b", ":8000", "managersite.wsgi:application"]
