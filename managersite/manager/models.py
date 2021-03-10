from django.db import models

class Ec2Instance(models.Model):
  instance_id = models.CharField(max_length=19)
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name
