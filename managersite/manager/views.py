import json
from io import StringIO
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import paramiko
from paramiko.client import SSHClient
from .models import Ec2Instance
from .forms import ActionForm
from . import aws

@login_required
def manage(request):
    servers = Ec2Instance.objects.all()
    context = {
        "servers": servers,
    }
    return render(request, 'manage.html', context)

def _shutdown(server):
    ssh_key = server.ssh_key
    privKeyStringIO = StringIO(ssh_key)
    pk = paramiko.Ed25519Key.from_private_key(privKeyStringIO)
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=server.ssh_url, username=server.ssh_user, pkey = pk)
    stdin, stdout, stderr = client.exec_command("./shutdown.sh")

@login_required
def manageDetail(request, server_id):
    server = get_object_or_404(Ec2Instance, pk=server_id)
    
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            if action == "start":
                result_d = aws.start_instance(server.instance_id)
                result = json.dumps(result_d)
            elif action == "stop":
                #result_d = aws.stop_instance(server.instance_id)
                _shutdown(server)
                result = "stopping the server..."
            else:
                result = "unknown..."
            return HttpResponse(result)
    else:
        form = ActionForm()

    ec2 = aws.get_instance_info(server.instance_id)
    context = {
        "ec2": ec2,
        "server": server,
        "form": form,
    }
    return render(request, 'manageDetail.html', context)
