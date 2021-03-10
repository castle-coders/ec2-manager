from django.shortcuts import get_object_or_404, render
from .models import Ec2Instance

def manage(request):
    servers = Ec2Instance.objects.all()
    context = {
        "servers": servers,
    }
    return render(request, 'manage.html', context)

def manageDetail(request, server_id):
    server = get_object_or_404(Ec2Instance, pk=server_id)
    ec2 = aws.get_instance_info(server.instance_id)
    context = {
        "ec2": ec2,
        "server": server,
    }
    return render(request, 'manageDetail.html', context)