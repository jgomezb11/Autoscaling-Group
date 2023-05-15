import time
import boto3

# Configuración del autoescalado simulado
min_instances = 1
max_instances = 5
cpu_threshold = 70
scale_up_factor = 2
scale_down_factor = 0.5

# Crea una instancia del cliente EC2 de AWS
ec2_client = boto3.client('ec2')

def create_instances(count):
    # Crea nuevas instancias EC2
    response = ec2_client.run_instances(
        ImageId='ami-0f09de67419a5c3c1',
        InstanceType='t2.micro',
        MinCount=count,
        MaxCount=count
    )
    instance_ids = [instance['InstanceId'] for instance in response['Instances']]
    print(f'Se han creado {count} nuevas instancias: {instance_ids}')

def terminate_instances(count):
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    instances = response['Reservations']
    instances_to_terminate = instances[:count]
    instance_ids = []
    for i in range(0, count):
        instance_ids.append(instances_to_terminate[i]['Instances'][0]['InstanceId'])

    # Termina las instancias seleccionadas
    response = ec2_client.terminate_instances(
        InstanceIds=instance_ids
    )
    print(f'Se han terminado {count} instancias: {instance_ids}')

def monitor_cpu_usage():
    return 20

def scale_instances():
    # Obtiene el número actual de instancias activas
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    try:
        instance_count = len(response['Reservations'])
    except:
        instance_count = 0
    cpu_usage = monitor_cpu_usage()

    # Realiza la lógica de escalado
    if cpu_usage > cpu_threshold and instance_count < max_instances:
        new_instance_count = min(max_instances, instance_count * scale_up_factor)
        if new_instance_count == 0:
            new_instance_count = 1
        instances_to_create = new_instance_count - instance_count
        create_instances(instances_to_create)
    elif cpu_usage < cpu_threshold and instance_count > min_instances:
        instances_to_terminate = instance_count - min_instances
        terminate_instances(instances_to_terminate)

if __name__ == '__main__':
    while True:
        # Ejecuta la lógica de escalado cada X segundos
        scale_instances()
        time.sleep(30)  # Espera 60 segundos antes de la siguiente iteración
