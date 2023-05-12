import time
import boto3

# Configuración del autoescalado simulado
min_instances = 1
max_instances = 5
cpu_threshold = 70  # Umbral de uso de CPU para activar el escalado
scale_up_factor = 2  # Factor de escalado para crear nuevas instancias
scale_down_factor = 0.5  # Factor de escalado para terminar instancias

# Crea una instancia del cliente EC2 de AWS
ec2_client = boto3.client('ec2')

def create_instances(count):
    # Crea nuevas instancias EC2
    response = ec2_client.run_instances(
        ImageId='ami-12345678',  # ID de la imagen AMI
        InstanceType='t2.micro',  # Tipo de instancia
        MinCount=count,
        MaxCount=count
    )
    instance_ids = [instance['InstanceId'] for instance in response['Instances']]
    print(f'Se han creado {count} nuevas instancias: {instance_ids}')

def terminate_instances(count):
    # Obtiene las instancias activas
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    instances = response['Reservations'][0]['Instances']
    instances_to_terminate = instances[:count]
    instance_ids = [instance['InstanceId'] for instance in instances_to_terminate]

    # Termina las instancias seleccionadas
    response = ec2_client.terminate_instances(
        InstanceIds=instance_ids
    )
    print(f'Se han terminado {count} instancias: {instance_ids}')

def monitor_cpu_usage(instance_id):
    return 1

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
    instance_count = len(response['Reservations'][0]['Instances'])

    # Obtiene el uso de CPU de una instancia (puede ser el promedio de todas las instancias)
    instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
    cpu_usage = monitor_cpu_usage(instance_id)

    # Realiza la lógica de escalado
    if cpu_usage > cpu_threshold and instance_count < max_instances:
        new_instance_count = min(max_instances, instance_count * scale_up_factor)
        instances_to_create = new_instance_count - instance_count
        create_instances(instances_to_create)
    elif cpu_usage < cpu_threshold and instance_count > min_instances:
        instances_to_terminate = instance_count - min_instances
        terminate_instances(instances_to_terminate)

if __name__ == '__main__':
    while True:
        # Ejecuta la lógica de escalado cada X segundos
        scale_instances()

        # Espera un tiempo antes de volver a ejecutar la lógica
        time.sleep(60)  # Espera 60 segundos antes de la siguiente iteración
