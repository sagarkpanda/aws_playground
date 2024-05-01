import boto3
region = 'ap-south-1'
instances = ['i-0841b5e5fc3d1789a']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
