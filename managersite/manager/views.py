import json
import logging
from io import StringIO
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
import paramiko
from paramiko.client import SSHClient
from .models import Ec2Instance, ServerStatus
from .forms import ActionForm
from . import aws

logger = logging.getLogger(__name__)

@login_required
def manage(request):
    servers = Ec2Instance.objects.all()
    context = {
        "servers": servers,
    }
    return render(request, 'manage.html', context)

def _shutdown(server):
    status = ServerStatus()
    status.player_count = -1 
    status.for_server = server
    status.save()
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
                #result_d = aws.start_instance(server.instance_id)
                #result = json.dumps(result_d)
                result = "fake start"
            elif action == "stop":
                #result_d = aws.stop_instance(server.instance_id)
                _shutdown(server)
                result = "stopping the server..."
            else:
                result = "unknown..."
            logger.info("{user} requested {action} on {server} and got: {result}".format(user=request.user, action=action, server=server, result=result))
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

def _genericNotFound():
    return HttpResponseNotFound("not found")

@csrf_exempt
def serverPing(request, server_id):
    try:
        server = Ec2Instance.objects.get(pk=server_id)
    except Ec2Instance.DoesNotExist:
        return _genericNotFound() 

    if request.method == 'POST':
        body = json.loads(request.body)
        api_key = body['api-key']
        if api_key != server.api_key:
            return _genericNotFound()

        check_idle_threshold = datetime.now() - timedelta(minutes=15)
        pings_in_threshold = ServerStatus.objects.filter(for_server_id=server_id).filter(timestamp__gt=check_idle_threshold).order_by('-timestamp')
        count_pings = pings_in_threshold.count()

        if count_pings > 0:
            has_players = False
            for ping in pings_in_threshold:
                if ping.player_count != 0:
                    has_players = True
                    break
            if not has_players:
                logger.info("server {server} idle, shutting down".format(server=server))
                _shutdown(server)
                return HttpResponse(status=201)

        ssh_key = server.ssh_key
        privKeyStringIO = StringIO(ssh_key)
        pk = paramiko.Ed25519Key.from_private_key(privKeyStringIO)
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=server.ssh_url, username=server.ssh_user, pkey = pk)
        stdin, stdout, stderr = client.exec_command("./bin/valheim-status")
        status_record_json = json.loads(stdout.read()) 
        # TODO key error will exist when server is not running
        status = ServerStatus()
        status.player_count = status_record_json['player_count']
        status.for_server = server
        status.save()
        return HttpResponse(status=201)
    else: 
        return _genericNotFound()
