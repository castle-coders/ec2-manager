import boto3


def _get_client():
  return boto3.client('ec2')

def get_instance_info(iid):
  client = _get_client()
  info = client.describe_instances(InstanceIds=[iid])
  instance = info['Reservations'][0]['Instances'][0] # TODO: fail gracefully
  return {
      "state": instance['State']['Name'],
      "ip": instance['PublicIpAddress'],
      "launch_time": instance['LaunchTime'],
  }

def stop_instance(iid):
  client = _get_client()
  client.stop_instances([iid])

def start_instance(iid):
  client = _get_client()
  client.start_instances([iid])
