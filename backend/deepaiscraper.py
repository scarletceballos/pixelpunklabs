import requests
import time

def generate_image(prompt):
    print("\n--- Starting image generation process ---")
    try:
        api_key = "2a1c8867-bcb9-450e-8b3d-adb9271b18ff"  
        
        # API endpoint
        url = "https://api.deepai.org/api/text2img"
        
        # Headers with API key
        headers = {
            'api-key': api_key
        }
        
        # Data payload
        data = {
            'text': f"steampunk themed: {prompt}",
        }
        
        print("Sending request to DeepAI...")
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if 'output_url' in result:
                image_url = result['output_url']
                print(f"\nSUCCESS - Image URL: {image_url}")
                return image_url
            else:
                print("No image URL in response")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
