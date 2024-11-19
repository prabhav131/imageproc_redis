from datetime import datetime
import time
from pymongo import MongoClient
import utils

# MongoDB setup
client = MongoClient("mongodb+srv://guptaprabhav131:4ytWTSdShcIy4OVJ@cluster0.rr2p5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["image_task_db"]
tasks_collection = db["tasks"]

def process_image_task(task_id):
    try:
        # Print a message when the task is picked up by the worker
        print(f"Task {task_id} picked up by worker for processing.")
        
        # Retrieve task from MongoDB
        task = tasks_collection.find_one({"task_id": task_id})
        if not task or "image_url" not in task:
            raise Exception("Invalid task or missing image URL")

        # Simulate fetching the image URL (assuming image_url is stored in the task document)
        image_url = task["image_url"]

        # Simulate processing the image (introduce a 1-minute delay)
        print(f"Processing task {task_id} with image URL: {image_url}")
        
        task_metadata = {
            "task_id": task_id,
            "status": "Processing",
            "metadata": None,
            "timestamp": datetime.now()
        }
        tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "Processing","timestamp": datetime.now()}})
        
        if not utils.is_image_url_valid(image_url):
            print("URL is invalid or unreachable, can't be processed!")    
            raise Exception("not a valid URL")

        # only process a valid URL
        time.sleep(60)  # Simulate processing time
        
        # TBD: write logic to raise exception if actual AI processing response is a failure

        # Simulate metadata extraction from image
        metadata = {
            "title": "Sample Title",
            "description": "Sample Description",
            "color": "Sample Color",
            "product_type": "Sample Product Type",
            "features": "Sample Features"
        }

        # Update MongoDB with metadata
        task_metadata = {
            "task_id": task_id,
            "status": "Success",
            "metadata": metadata,
            "timestamp": datetime.now()
        }
        tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "Success","metadata" : metadata, "timestamp": datetime.now()}})
        print(f"Task {task_id} processed successfully. Metadata saved to MongoDB.")

    except Exception as e:
        # In case of error, mark task as failed
        task_metadata = {
            "task_id": task_id,
            "status": "Failed",
            "error": str(e),
            "timestamp": datetime.now()
        }
        tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "Failed","timestamp": datetime.now()}})
        print(f"Failure! Error processing task {task_id}: {e}")


if __name__ == "__main__":
    process_image_task(task_id="10d1e972-5782-427b-906f-9d0de7136c1e")