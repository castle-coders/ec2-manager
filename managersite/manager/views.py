from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

@login_required
def manageDetail(request, server_id):
    server = get_object_or_404(Ec2Instance, pk=server_id)
    
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            if action == "start":
                aws.start_instance(server.instance_id)
            elif action == "stop":
                aws.stop_instance(server.instance_id)
            else:
                action = "unknown..."
            return HttpResponse(action)
    else:
        form = ActionForm()

    ec2 = aws.get_instance_info(server.instance_id)
    context = {
        "ec2": ec2,
        "server": server,
        "form": form,
    }
    return render(request, 'manageDetail.html', context)
