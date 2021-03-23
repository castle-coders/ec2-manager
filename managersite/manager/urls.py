from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('manage', views.manage, name='manage'),
    path('manage/<int:server_id>', views.manageDetail, name='manageDetail'),
    path('ping/<int:server_id>', views.serverPing, name='serverPing')
]