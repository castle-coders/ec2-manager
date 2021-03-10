#!/bin/sh
set -e

python manage.py migrate --noinput

cat <<EOF | python manage.py shell
import os, sys
from django.contrib.auth import get_user_model

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASS = os.getenv('ADMIN_PASS')

if not ADMIN_EMAIL or not ADMIN_PASS:
    sys.exit(1)

User = get_user_model()  # get the currently active user model,

User.objects.filter(username=ADMIN_USERNAME).exists() or \
    User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASS)
EOF

exec "$@"