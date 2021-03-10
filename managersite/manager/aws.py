import boto3


def _get_client():
  return boto3.client('ec2')

def get_instance_info(iid):
  client = _get_client()
  instance = client.Instance(iid)
  return {
      "state": instance.state['Name'],
      "ip": instance.public_ip_address,
      "launch_time": instance.launch_time,
  }

def stop_instance(iid):
  client = _get_client()
  client.stop_instances([iid])


def start_instance(iid):
  client = _get_client()
  client.start_instances([iid])
