from rq import Worker, Queue
from redis import Redis
from concurrent.futures import ProcessPoolExecutor

# Your Redis connection string (from your Redis Cloud details)
redis_conn = Redis(host='redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com', 
                   port=12438, 
                   password='26XC9YvCErtUsaybooUFr4NgeMfDMLqz', 
                   db=0)

# Create the Queue instance
queue = Queue(connection=redis_conn)

def worker_main():
    # Create the worker instance
    worker = Worker([queue], connection=redis_conn)
    
    # Set the executor for the worker
    worker.executor = ProcessPoolExecutor()

    # Start the worker to process the queue jobs
    worker.work()

if __name__ == '__main__':
    worker_main()
