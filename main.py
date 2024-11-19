from datetime import datetime
import time
import uuid
from flask import Flask, json, jsonify, request, render_template, Response
import redis
from pymongo import MongoClient 
from que import q, process_task
import utils
import constants

app = Flask(__name__)

# MongoDB setup
try:
    client = MongoClient(constants.MONGO_URI)
    db = client[constants.MONGO_DB]
    tasks_collection = db[constants.MONGO_COLLECTION]
except Exception as e:
    print(f"Error in connecting to mongodb- {str(e)}")

# Redis setup - Use Redis Cloud details
try:
    r = redis.StrictRedis(
        host=constants.REDIS_HOST,  #  Redis Cloud host
        port=constants.REDIS_PORT,  #  Redis Cloud port
        password=constants.REDIS_PASSWORD,  # Replace with your actual Redis Cloud password
        db=0,  # Default database
        decode_responses=True  # Automatically decode responses to strings
    )
except Exception as e:
    print(f"Error in connecting to mongodb- {str(e)}")

@app.route("/")
def hello_world():
    tasks = list(db["tasks"].find())
    return render_template('index.html', tasks=tasks)
    # return "<p>Hello, World!</p>"

# SSE Stream Route to push task updates to client
@app.route('/api/task-status')
def task_status():
    def generate():
        # Simulate a task monitoring loop
        while True:
            # Fetch the latest task statuses and metadata from MongoDB
            # client = MongoClient("mongodb+srv://guptaprabhav131:4ytWTSdShcIy4OVJ@cluster0.rr2p5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            # db = client["image_task_db"]
            tasks = list(db["tasks"].find())
            
            # Send each task status update with metadata as an SSE message
            for task in tasks:
                # Prepare the task data
                task_data = {
                    "task_id": task['task_id'],
                    "status": task['status'],
                    "metadata": task['metadata']
                }
                # Convert the task data to JSON
                message = f"data: {json.dumps(task_data)}\n\n"
                yield message  # Send updated task status
            
            time.sleep(3)  # Simulate delay between updates

    return Response(generate(), content_type='text/event-stream')

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
    