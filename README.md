# imageproc_redis
image processor to take in image urls and to process them using ai to show results in frontend


1. Go inside the project folder and create virtual env and activate it.
2. pip install -r requirements.txt
3. in one terminal, run python main.py to fire up the frontend.
4. in another terminal run the worker docker image to make it wait to listen to the queue
    4.1 "docker build -t my-rq-worker ."
    4.2 "docker run -d --name worker1 my-rq-worker" followed by "docker logs -f worker1" to see the continuous logs
    4.3 open another terminal and activate another worker to process 2 tasks together using "docker run -d --name worker2     my-rq-worker" followed by "docker logs -f worker2" to see the continuous logs
5. submit image url in the frontend and see the updates
