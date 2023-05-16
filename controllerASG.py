import time
import boto3
from pymongo import MongoClient

# Crea una instancia del cliente EC2 de AWS
ec2_client = boto3.client('ec2')

def create_instances(count):
    # Crea nuevas instancias EC2
    response = ec2_client.run_instances(
        ImageId='ami-057fdd985f1bcf237',
        InstanceType='t2.micro',
        MinCount=count,
        MaxCount=count,
        SecurityGroupIds=["sg-025b36a67c4532340"]
    )
    instance_ids = []
    configuration = collection.find_one()
    time.sleep(5)
    for instance in response["Instances"]:
        instance_ids.append(instance["InstanceId"])
        newHost = {
            "id_instance":instance["InstanceId"],
            "ip":get_public_ip(instance["InstanceId"])
        }
        newStatus = {
            "id_instance":instance["InstanceId"],
            "state": False
        }
        configuration["hosts"].append(newHost)
        configuration["status"].append(newStatus)
    collection.update_one({'_id': configuration['_id']}, {'$set': configuration})
    print(f'Se han creado {count} nuevas instancias: {instance_ids}')

def get_public_ip(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')
    while not public_ip:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')
    return public_ip

def terminate_instances(count):
    instance_ids = []
    configuration = collection.find_one()
    for host in configuration["hosts"]:
        instance_ids.append(host['id_instance'])
    instances_to_terminate = instance_ids[:count]
    hosts_filtrados = [host for host in configuration["hosts"] if host['id_instance'] not in instances_to_terminate]
    status_filtrados = [host for host in configuration["status"] if host['id_instance'] not in instances_to_terminate]
    configuration['hosts'] = hosts_filtrados
    configuration['status'] = status_filtrados
    collection.update_one({'_id': configuration['_id']}, {'$set': configuration})

    # Termina las instancias seleccionadas
    response = ec2_client.terminate_instances(
        InstanceIds=instances_to_terminate
    )
    print(f'Se han terminado {count} instancias: {instances_to_terminate}')

def monitor_cpu_usage():
    return collection.find_one()["average_memory"]

def scale_instances():
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    instance_count = 0
    for group in response['Reservations']:
        instance_count += len(group['Instances'])
    cpu_usage = monitor_cpu_usage()

    if instance_count == 0:
        configuration = collection.find_one()
        configuration['hosts'] = []
        configuration['status'] = []
        collection.update_one({'_id': configuration['_id']}, {'$set': configuration})

    if (cpu_usage > cpu_up_threshold and instance_count < max_instances) or instance_count < min_instances:
        new_instance_count = min(max_instances, instance_count * scale_up_factor)
        if new_instance_count == 0:
            new_instance_count = 1
        instances_to_create = new_instance_count - instance_count
        create_instances(instances_to_create)
    elif cpu_usage < cpu_down_threshold and instance_count > min_instances:
        instances_to_terminate = int(max(instance_count * scale_down_factor, min_instances))
        terminate_instances(instances_to_terminate)

if __name__ == '__main__':
    global client, database, collection, min_instances, max_instances, cpu_up_threshold, cpu_down_threshold,scale_up_factor, scale_down_factor
    client = MongoClient("mongodb://localhost:27017")
    database = client["ASG"]
    collection = database["config"]
    config = collection.find_one()
    min_instances = config["min_instances"]
    max_instances = config["max_instances"]
    cpu_up_threshold = config["cpu_up_threshold"]
    cpu_down_threshold = config["cpu_down_threshold"]
    scale_up_factor = config["scale_up_factor"]
    scale_down_factor = config["scale_down_factor"]
    while True:
        # Ejecuta la lógica de escalado cada X segundos
        scale_instances()
        time.sleep(60)  # Espera 60 segundos antes de la siguiente iteración
