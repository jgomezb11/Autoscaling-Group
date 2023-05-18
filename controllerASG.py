import boto3
from pymongo import (
    MongoClient,
)
import time

ec2_client = boto3.client("ec2")


def create_instances(count):
    response = ec2_client.run_instances(
        ImageId="ami-057fdd985f1bcf237",
        InstanceType="t2.micro",
        MinCount=count,
        MaxCount=count,
        SecurityGroupIds=["sg-025b36a67c4532340"],
    )
    instance_ids = []
    configuration = collection.find_one()
    time.sleep(5)
    for instance in response["Instances"]:
        instance_ids.append(instance["InstanceId"])
        newHost = {
            "id_instance": instance["InstanceId"],
            "ip": get_public_ip(instance["InstanceId"]),
        }
        newStatus = {
            "id_instance": instance["InstanceId"],
            "state": False,
            "isReady": False,
            "memory_usage": [],
            "time_stap": [],
        }
        configuration["hosts"].append(newHost)
        configuration["status"].append(newStatus)
    changes = {
        "hosts": configuration["hosts"],
        "status": configuration["status"],
    }
    response = collection.update_one(
        {"_id": configuration["_id"]}, {"$set": changes}
    )
    while not response.acknowledged:
        response = collection.update_one(
            {"_id": configuration["_id"]}, {"$set": changes}
        )
    print(f"Se han creado {count} nuevas instancias: {instance_ids}")


def get_public_ip(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = response["Reservations"][0]["Instances"][0].get(
        "PublicIpAddress"
    )
    while not public_ip:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = response["Reservations"][0]["Instances"][0].get(
            "PublicIpAddress"
        )
    return public_ip


def terminate_instances(count):
    instance_ids = []
    configuration = collection.find_one()
    for host in configuration["hosts"]:
        instance_ids.append(host["id_instance"])
    instances_to_terminate = instance_ids[:count]
    response = ec2_client.terminate_instances(
        InstanceIds=instances_to_terminate
    )
    print(f"Se han terminado {count} instancias: {instances_to_terminate}")


def monitor_cpu_usage():
    return collection.find_one()["average_memory"]


def count_running_instances():
    response = ec2_client.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running", "pending"]}
        ]
    )
    instance_count = 0
    instances_ids = []
    for group in response["Reservations"]:
        instance_count += len(group["Instances"])
        for instance in group["Instances"]:
            instances_ids.append(instance["InstanceId"])
    return instance_count, instances_ids


def scale_instances():
    instance_count, _ = count_running_instances()
    cpu_usage = monitor_cpu_usage()
    if instance_count == 0:
        configuration = collection.find_one()
        changes = {"hosts": [], "status": []}
        response = collection.update_one(
            {"_id": configuration["_id"]}, {"$set": changes}
        )
        while not response.acknowledged:
            response = collection.update_one(
                {"_id": configuration["_id"]}, {"$set": changes}
            )

    if (
        cpu_usage > cpu_up_threshold and instance_count < max_instances
    ) or instance_count < min_instances:
        new_instance_count = min(
            max_instances, instance_count * scale_up_factor
        )
        if new_instance_count == 0:
            new_instance_count = 1
        instances_to_create = new_instance_count - instance_count
        create_instances(instances_to_create)
    elif cpu_usage < cpu_down_threshold and instance_count > min_instances:
        instances_to_terminate = int(
            min(instance_count * scale_down_factor, instance_count - min_instances)
        )
        terminate_instances(instances_to_terminate)


def delete_unavailable_instances():
    configuration = collection.find_one()
    instances_to_terminate = []
    for host in configuration["status"]:
        status = host["state"]
        is_ready = host["isReady"]
        if not status and is_ready:
            instances_to_terminate.append(host["id_instance"])
    if len(instances_to_terminate) > 0:
        response = ec2_client.terminate_instances(
            InstanceIds=instances_to_terminate
        )
        print(
            "Instances ", instances_to_terminate, "deleted due to unavailability!"
        )


def initialize_db():
    configuration = collection.find_one()
    changes = {"hosts": [], "status": []}
    response = collection.update_one(
        {"_id": configuration["_id"]}, {"$set": changes}
    )
    while not response.acknowledged:
        response = collection.update_one(
            {"_id": configuration["_id"]}, {"$set": changes}
        )
    response = ec2_client.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running", "pending"]}
        ]
    )
    configuration = collection.find_one()
    instances_ids = []
    for group in response["Reservations"]:
        for instance in group["Instances"]:
            instances_ids.append(instance["InstanceId"])
            newHost = {
                "id_instance": instance["InstanceId"],
                "ip": get_public_ip(instance["InstanceId"]),
            }
            newStatus = {
                "id_instance": instance["InstanceId"],
                "state": False,
                "isReady": False,
                "memory_usage": [],
                "time_stap": [],
            }
            configuration["hosts"].append(newHost)
            configuration["status"].append(newStatus)

    changes = {
        "hosts": configuration["hosts"],
        "status": configuration["status"],
    }
    response = collection.update_one(
        {"_id": configuration["_id"]}, {"$set": changes}
    )
    while not response.acknowledged:
        response = collection.update_one(
            {"_id": configuration["_id"]}, {"$set": changes}
        )
    print(
        "Database initialized successfully! There are ",
        len(configuration["hosts"]),  " hosts up!"
    )


def update_from_database():
    index = 0
    while index < 30:
        count, instances_ids = count_running_instances()
        configuration = collection.find_one()
        hosts = configuration["hosts"]
        status = configuration["status"]
        if count < len(hosts) or count < len(status):
            instances_to_terminate = list(
                set([host["id_instance"] for host in hosts])
                - set(instances_ids)
            )
            hosts_filtrados = [
                host
                for host in hosts
                if host["id_instance"] not in instances_to_terminate
            ]
            status_filtrados = [
                host
                for host in configuration["status"]
                if host["id_instance"] not in instances_to_terminate
            ]
            configuration["hosts"] = hosts_filtrados
            configuration["status"] = status_filtrados
            response = collection.update_one(
                {"_id": configuration["_id"]},
                {
                    "$set": {
                        "hosts": configuration["hosts"],
                        "status": configuration["status"],
                    }
                },
            )
            while not response.acknowledged:
                collection.update_one(
                    {"_id": configuration["_id"]},
                    {
                        "$set": {
                            "hosts": configuration["hosts"],
                            "status": configuration["status"],
                        }
                    },
                )
        index += 1
        if index != 30:
            delete_unavailable_instances()
        time.sleep(2)


if __name__ == "__main__":
    global client, database, collection, min_instances, max_instances, cpu_up_threshold, cpu_down_threshold, scale_up_factor, scale_down_factor
    client = MongoClient("mongodb://localhost:27017")
    database = client["ASG"]
    collection = database["config"]
    initialize_db()
    while True:
        config = collection.find_one()
        min_instances = config["min_instances"]
        max_instances = config["max_instances"]
        cpu_up_threshold = config["cpu_up_threshold"]
        cpu_down_threshold = config["cpu_down_threshold"]
        scale_up_factor = config["scale_up_factor"]
        scale_down_factor = config["scale_down_factor"]
        scale_instances()
        update_from_database()
