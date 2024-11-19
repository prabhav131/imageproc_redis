from datetime import datetime
import uuid
import redis
from pymongo import MongoClient 

# MongoDB setup
client = MongoClient("mongodb+srv://guptaprabhav131:4ytWTSdShcIy4OVJ@cluster0.rr2p5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["image_task_db"]
tasks_collection = db["tasks"]

# Redis setup - Use Redis Cloud details
r = redis.StrictRedis(
    host='redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com',  # Your Redis Cloud host
    port=12438,  # Your Redis Cloud port
    password='26XC9YvCErtUsaybooUFr4NgeMfDMLqz',  # Replace with your actual Redis Cloud password
    db=0,  # Default database
    decode_responses=True  # Automatically decode responses to strings
)

def submit_task():
    # Generate a task ID and save the task in MongoDB
    task_id = str(uuid.uuid4())
    task = {
        "task_id": task_id,
        "image_url": "sample_url",
        "status": "Pending",
        "timestamp": datetime.now()
    }
    tasks_collection.insert_one(task)
    
    # push taskid to redis queue
    r.rpush('main_queue', task_id)
    return r
    
    
if __name__ == "__main__":
    # while r.llen('main_queue') > 0:
    #     task = r.lpop('main_queue')
    #     print(task, "- removed")
    # print("empty now!")    
    
    submit_task()
    submit_task()
    submit_task()