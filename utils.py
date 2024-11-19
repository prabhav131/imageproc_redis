import requests
import logging
from config import setup_logging

# Set up logging configuration
setup_logging()

# Create a logger instance
logger = logging.getLogger(__name__)

def is_image_url_valid(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Check if the content type is an image
            if 'image' in response.headers.get('Content-Type', ''):
                return True
            else:
                logger.error("The URL does not point to an image.")
                return False
        else:
            logger.error(f"image URL is broken!, status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return False
