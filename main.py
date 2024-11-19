from datetime import datetime
import uuid
from flask import Flask, jsonify, request, render_template
import redis
from pymongo import MongoClient 
from que import q, process_task
import utils

app = Flask(__name__)

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

@app.route("/")
def hello_world():
    tasks = list(db["tasks"].find())
    return render_template('index.html', tasks=tasks)
    # return "<p>Hello, World!</p>"

@app.route('/api/submit-task', methods=['POST'])
def submit_task():
    data = request.form.get('imageUrl')
    image_url = data
    
    if not image_url or not utils.is_image_url_valid(image_url):
        return jsonify({"error": "a valid/reachable Image URL is required"}), 400
    
    # Generate a task ID and save the task in MongoDB
    task_id = str(uuid.uuid4())
    task = {
        "task_id": task_id,
        "image_url": image_url,
        "status": "Pending",
        "metadata": None,
        "timestamp": datetime.now()
    }
    tasks_collection.insert_one(task)
    
    # push taskid to redis queue
    # r.lpush('main_queue', task_id)
    
    # Enqueue the task with a specific task_number
    task = q.enqueue(process_task, task_id) 
    print(f"Task {task.id} enqueued.")


    return jsonify({"taskId": task_id, "status": "Pending"}), 200

if __name__ == "__main__":
    app.run(debug=True)
    