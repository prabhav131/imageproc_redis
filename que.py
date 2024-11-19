from rq import Queue
import redis
from task import process_image_task
from redis.exceptions import ConnectionError

# Redis setup - Use Redis Cloud details
try:
    r = redis.StrictRedis(
        host='redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com',  # Your Redis Cloud host
        port=12438,  # Your Redis Cloud port
        password='26XC9YvCErtUsaybooUFr4NgeMfDMLqz',  # Replace with your actual Redis Cloud password
        db=0,  # Default database
        decode_responses=True  # Automatically decode responses to strings
    )
except ConnectionError as e:
    print(f"error- Redis connection failed: {str(e)}")

# Create a Queue object that will manage the tasks
q = Queue(connection=r)

def process_task(task_number):
    """Task to process in the background"""
    try:
        print(f"Processing task number: {task_number}")
        process_image_task(task_id=task_number)
        print(f"Finished task number: {task_number}")
    except Exception as e:
        print(f"encountered some error while processing task {task_number} - str(e)")    
