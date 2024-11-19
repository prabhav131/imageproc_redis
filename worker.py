from rq import Worker, Queue
from redis import Redis
import os
import multiprocessing

# Ensure macOS fork safety
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'


# Your Redis connection string (from Redis Cloud details)
try:

    redis_conn = Redis(
        host='redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com',
        port=12438,
        password='26XC9YvCErtUsaybooUFr4NgeMfDMLqz',
        db=0
    )
except Exception as e:
    print(f"Error connecting to redis- {str(e)}")    

# Create the Queue instance
queue = Queue(connection=redis_conn)

def worker_main():
    # Pass Redis connection directly to the Worker
    worker = Worker([queue], connection=redis_conn)
    worker.work()

if __name__ == '__main__':
    
    multiprocessing.set_start_method('spawn', force=True)
    
    worker_main()