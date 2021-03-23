import uuid
from django.db import models

class Ec2Instance(models.Model):
  instance_id = models.CharField(max_length=19)
  name = models.CharField(max_length=200)
  ssh_key = models.TextField()
  ssh_user = models.CharField(max_length=50)
  ssh_url = models.CharField(max_length=200)
  api_key = models.CharField(max_length=36, default=uuid.uuid4)

  def __str__(self):
    return self.name

class ServerStatus(models.Model):
  timestamp = models.DateTimeField(auto_now=True)
  player_count = models.IntegerField()
  for_server = models.ForeignKey(Ec2Instance, on_delete=models.CASCADE)

  def __str__(self):
    return "{for_server} @ {timestamp} : {player_count}".format(timestamp=self.timestamp, player_count=self.player_count, for_server=self.for_server)