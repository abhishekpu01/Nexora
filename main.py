from fastapi import FastAPI, UploadFile, File, Form
from google import genai
from dotenv import load_dotenv
import os
import json
from prompts import IMAGE_ASSISTANT_SYSTEM
from utils.utils import createSuccessResponse, createFailedResponse
from nexoramcp_service.mcp_server import fetch_analysed_products

load_dotenv()

app = FastAPI()
geminiclient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/analyse")
async def analyse(height: str = Form(...), weight: str = Form(...), face_tone: str = Form(...), image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        response = geminiclient.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                genai.types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image.content_type
                ),
                f"""
                Height: {height} cm
                Weight: {weight} kg
                Face Tone: {face_tone}
                """
            ],
            config=genai.types.GenerateContentConfig(
                system_instruction=IMAGE_ASSISTANT_SYSTEM
            )
        )

        agent_response = json.loads(response.candidates[0].content.parts[0].text)
        result = fetch_analysed_products(agent_response['outfit_types'], agent_response['color_combinations'])
        agent_response['recommended_outfits'] = result
        return createSuccessResponse(agent_response)

    except Exception as e:
        return createFailedResponse(str(e))