from django.contrib import admin
from .models import Ec2Instance, ServerStatus


admin.site.register(Ec2Instance)
admin.site.register(ServerStatus)