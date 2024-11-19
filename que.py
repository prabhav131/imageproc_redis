import time
from rq import Queue
from redis import Redis
import redis
from task import process_image_task

# Connect to Redis server
redis_conn = Redis(host='localhost', port=6379, db=0)

# Redis setup - Use Redis Cloud details
r = redis.StrictRedis(
    host='redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com',  # Your Redis Cloud host
    port=12438,  # Your Redis Cloud port
    password='26XC9YvCErtUsaybooUFr4NgeMfDMLqz',  # Replace with your actual Redis Cloud password
    db=0,  # Default database
    decode_responses=True  # Automatically decode responses to strings
)


# Create a Queue object that will manage the tasks
q = Queue(connection=r)

def process_task(task_number):
    """Task to process in the background"""
    
    print(f"Processing task number: {task_number}")
    process_image_task(task_id=task_number)
    print(f"Finished task number: {task_number}")
