from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from datetime import datetime, timedelta
import base64
import httpx
import os
from typing import Optional

from database import db_manager
from schemas import ImageGenerationRequest, ImageGenerationResponse
from deepaiscraper import generate_image

app = Flask(__name__)
CORS(app)

# Load environment variables
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
WORKER_URL = os.getenv("CLOUDFLARE_WORKER_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Change in production

app.config['SECRET_KEY'] = SECRET_KEY

class AssetGenerator:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.worker_url = WORKER_URL

    async def enhance_prompt(self, prompt: str) -> str:
        steampunk_elements = [
            "Victorian era aesthetics",
            "brass and copper materials",
            "mechanical gears",
            "steam-powered machinery",
            "ornate metalwork",
            "vintage industrial style"
        ]
        return f"steampunk-themed {prompt} featuring {', '.join(steampunk_elements)}"

    async def generate_image(self, prompt: str) -> dict:
        enhanced_prompt = await self.enhance_prompt(prompt)
        return await generate_image(enhanced_prompt)

generator = AssetGenerator()

# Authentication decorator
def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = await db_manager.get_user_by_username(data['username'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return await f(current_user, *args, **kwargs)
    
    return decorated

# Routes
@app.route('/register', methods=['POST'])
async def register():
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if await db_manager.get_user_by_email(data['email']):
        return jsonify({'message': 'Email already registered'}), 400
    
    if await db_manager.get_user_by_username(data['username']):
        return jsonify({'message': 'Username already taken'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    
    user_data = {
        'username': data['username'],
        'email': data['email'],
        'password': hashed_password
    }
    
    user = await db_manager.create_user(user_data)
    return jsonify({'message': 'User created successfully', 'user_id': user['id']}), 201

@app.route('/login', methods=['POST'])
async def login():
    auth = request.get_json()
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Missing credentials'}), 401
    
    user = await db_manager.get_user_by_username(auth.get('username'))
    
    if not user or not check_password_hash(user['password'], auth.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'username': user['username'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    })

@app.route('/generate', methods=['POST'])
@token_required
async def generate_image_endpoint(current_user):
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        result = await generator.generate_image(data['prompt'])
        
        if result and 'output_url' in result:
            image_data = {
                'user_id': str(current_user['_id']),
                'prompt': data['prompt'],
                'image_url': result['output_url'],
                'created_at': datetime.utcnow()
            }
            
            saved_image = await db_manager.save_generated_image(image_data)
            
            return jsonify({
                'success': True,
                'image_data': result['output_url'],
                'image_id': str(saved_image['id'])
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate image'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/my-images', methods=['GET'])
@token_required
async def get_user_images(current_user):
    images = await db_manager.get_user_images(str(current_user['_id']))
    return jsonify({
        'images': [{
            'id': str(img['_id']),
            'prompt': img['prompt'],
            'image_url': img['image_url'],
            'created_at': img['created_at'].isoformat()
        } for img in images]
    })

@app.route('/health', methods=['GET'])
async def health_check():
    try:
        # Test database connection
        await db_manager.db.command('ping')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'api_version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)