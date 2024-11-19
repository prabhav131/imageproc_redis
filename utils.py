import requests

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
                print("The URL does not point to an image.")
                return False
        else:
            print(f"image URL is broken!, status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
        
    url = "https://example.com/path/to/image.jpg"
    if is_image_url_valid(url):
        print("The image URL is valid and reachable.")
    else:
        print("The image URL is invalid or unreachable.")
