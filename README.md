# imageproc_redis
AI-powered image processing system that ingests image URLs, processes them using machine learning models, and delivers results to the frontend. Implemented Redis for distributed task queue management, enabling parallel processing with multiple workers. Designed real-time status updates in the frontend using SSE, ensuring a seamless user experience.
DB used: MongoDB

1. Go inside the project folder and create virtual env and activate it.
2. pip install -r requirements.txt
3. in one terminal, run python main.py to fire up the frontend.
4. in another terminal run the worker docker image to make it wait to listen to the queue. Ensure you have docker installed on your system.
    4.1 "docker build -t my-rq-worker ."
    4.2 "docker run -d --name worker1 my-rq-worker" followed by "docker logs -f worker1" to see the continuous logs
    4.3 open another terminal and activate another worker to process 2 tasks together using "docker run -d --name worker2     my-rq-worker" followed by "docker logs -f worker2" to see the continuous logs
5. submit image url in the frontend and see the updates
