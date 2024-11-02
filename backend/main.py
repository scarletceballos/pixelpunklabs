
import os
from dotenv import load_dotenv
import httpx
from typing import List, Optional
from user_manager import UserManager
from database import DatabaseManager
from schemas import UserCreate, UserInDB, ImageCreate, ImageInDB
import json
from pydantic import BaseModel


# Load environment variables
load_dotenv()
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")
WORKER_URL = os.getenv("CLOUDFLARE_WORKER_URL")

'''oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")'''

user_manager = UserManager()
db_manager = DatabaseManager()

SECRET_NAME = os.getenv("SECRET_NAME")
'''do this command for authentication then use SECRET_NAME in the header of the deepai or blender api": wrangler secret put SECRET_NAME'''


class GenerationRequest(BaseModel):
    prompt: str
    type: str = "image"  # "image" or "3d"
    style_preferences: Optional[dict] = None

class GenerationResponse(BaseModel):
    asset_url: str
    type: str
    prompt: str
    metadata: Optional[dict] = None

class AssetGenerator:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.worker_url = WORKER_URL

    async def enhance_prompt(self, prompt: str, asset_type: str) -> str:
        """Enhance prompt with steampunk elements"""
        steampunk_elements = {
            "image": [
                "Victorian era aesthetics",
                "brass and copper materials",
                "mechanical gears",
                "steam-powered machinery",
                "ornate metalwork",
                "vintage industrial style"
            ],
            "3d": [
                "detailed mechanical parts",
                "brass fixtures",
                "copper piping",
                "intricate gears",
                "steam valves",
                "Victorian-era engineering"
            ]
        }
        
        elements = steampunk_elements.get(asset_type, steampunk_elements["image"])
        return f"steampunk-themed {prompt} featuring {', '.join(elements)}"

    async def generate_image(self, prompt: str) -> dict:
        """Generate image using DeepAI through Cloudflare Worker"""
        enhanced_prompt = await self.enhance_prompt(prompt, "image")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.worker_url}/generate/image",
                    headers=self.headers,
                    json={
                        "prompt": enhanced_prompt,
                        "api_key": DEEPAI_API_KEY,
                        "settings": {
                            "style": "steampunk",
                            "quality": "high",
                            "negative_prompt": "modern, futuristic, minimal"
                        }
                    }
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Worker error: {response.text}"
                    )
                
                return response.json()
                
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="Image generation timed out"
                )

    async def generate_3d_model(self, prompt: str) -> dict:
        """Generate 3D model using Blender through Cloudflare Worker"""
        enhanced_prompt = await self.enhance_prompt(prompt, "3d")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.worker_url}/generate/3d",
                    headers=self.headers,
                    json={
                        "prompt": enhanced_prompt,
                        "settings": {
                            "format": "glb",
                            "style": "steampunk",
                            "detail_level": "high",
                            "blender_settings": {
                                "render_engine": "cycles",
                                "samples": 128,
                                "resolution": [1920, 1080]
                            }
                        }
                    }
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Worker error: {response.text}"
                    )
                
                return response.json()
                
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="3D model generation timed out"
                )

generator = AssetGenerator()

# Authentication endpoints
@app.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    return await user_manager.create_user(user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_manager.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Image endpoints
@app.post("/generate", response_model=GenerationResponse)
async def generate_asset(request: GenerationRequest):
    """Generate either a steampunk image or 3D model"""
    try:
        if request.type == "image":
            result = await generator.generate_image(request.prompt)
            return GenerationResponse(
                asset_url=result["output_url"],
                type="image",
                prompt=request.prompt,
                metadata=result.get("metadata")
            )
            
        elif request.type == "3d":
            result = await generator.generate_3d_model(request.prompt)
            return GenerationResponse(
                asset_url=result["model_url"],
                type="3d",
                prompt=request.prompt,
                metadata={
                    "format": "glb",
                    "vertices": result.get("vertex_count"),
                    "file_size": result.get("file_size")
                }
            )
            
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid asset type. Use 'image' or '3d'"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Check service health and API connections"""
    try:
        async with httpx.AsyncClient() as client:
            worker_health = await client.get(f"{WORKER_URL}/health")
            
            return {
                "status": "healthy",
                "worker_status": worker_health.status_code == 200,
                "api_version": "1.0.0"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

