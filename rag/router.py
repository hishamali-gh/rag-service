""" from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from rag.database import search_manuals


# 1. Initialize an isolated API router group (like Django's path include blocks)

router = APIRouter(prefix="/api/chat", tags=["AI Copilot Portal"])


# 2. Define the Incoming Data Contract (What React must send us)

class ChatRequestSchema(BaseModel):
    message: str


# 3. Define the Outgoing Data Contract (What we promise to return to React)

class ChatResponseSchema(BaseModel):
    user_query: str
    retrieved_context: str
    ai_synthesis: str


# 4. Create an asynchronous HTTP POST path endpoint

@router.post("/", response_model=ChatResponseSchema)
async def process_copilot_query(payload: ChatRequestSchema):


    # Enforce basic validation constraints manually if string is blank spaces

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")
    

    # Execution Step A: Run your verified Retrieval function

    matched_documentation = search_manuals(payload.message)

    
    # Execution Step B: Simulate the Augmentation & Generation layer.

    # In a later phase, this string will be replaced by a live API call to an LLM.

    if "OVN-404" in matched_documentation or "OVEN" in payload.message.upper():
        simulated_ai_response = (
            "Warning OVN-404 fetched. Please isolate the automated fluid pump line "
            "immediately and execute a manual power cycle on the secondary radiator core."
        )

    elif "CNV-BELT" in matched_documentation or "BELT" in payload.message.upper():
        simulated_ai_response = (
            "Conveyor misalignment verified. Proceed to the lower intake assembly "
            "and turn both tension bolts clockwise exactly 2 rotations."
        )

    else:
        simulated_ai_response = f"Context cleared. Recommending technical index parameter lookup: {matched_documentation}"


    # 5. Pack the results into your response schema format

    return ChatResponseSchema(
        user_query=payload.message,
        retrieved_context=matched_documentation,
        ai_synthesis=simulated_ai_response
    ) """


import os

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from openai import OpenAI

from dotenv import load_dotenv

from rag.database import search_manuals


load_dotenv()


router = APIRouter(prefix="/api/chat", tags=["AI Copilot Portal"])

# Determine mode from environment variable

USE_LIVE_AI = os.getenv("USE_LIVE_AI", "False").lower() == "true"


# If true, it hooks up to your local Ollama port!

if USE_LIVE_AI:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        base_url=os.getenv("OPENAI_API_BASE_URL", "http://localhost:11434/v1")
    )


class ChatRequestSchema(BaseModel):
    message: str


class ChatResponseSchema(BaseModel):
    user_query: str
    retrieved_context: str
    ai_synthesis: str


@router.post("/", response_model=ChatResponseSchema)
async def process_copilot_query(payload: ChatRequestSchema):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")
    
    
    # 1. RETRIEVAL ("R"): Grab the exact technical instruction paragraph from your manuals
    
    matched_documentation = search_manuals(payload.message)
    
    
    # 2 & 3. AUGMENTATION & GENERATION ("AG")
    
    if USE_LIVE_AI:
        try:
            
            # Storing the manual context inside the system prompt contract
            
            system_instructions = (
                "You are an expert operations assistant for the Pizzeria VDCS platform.\n"
                "Answer the operator's question using ONLY this documentation context:\n\n"
                f"{matched_documentation}\n\n"
                "Keep your response concise, professional, and formatted for an industrial monitor screen."
            )
            
            
            # Send the request to your local Llama3 brain
            
            response = client.chat.completions.create(
                model="llama3",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": payload.message}
                ],
                temperature=0.2
            )
            
            generated_ai_text = response.choices[0].message.content
            
        except Exception as e:
            print(f"Ollama Link Fault: {e}")
            
            raise HTTPException(status_code=502, detail="Local Ollama instance unreachable. Is the service active?")
    else:
        
        # Fallback local mock mode if USE_LIVE_AI is False
        
        if "OVN-404" in matched_documentation or "OVEN" in payload.message.upper():
            generated_ai_text = "[Dev Mock]: Isolate fluid pump lines and power cycle radiator core."
        
        else:
            generated_ai_text = f"[Dev Mock]: Context located: {matched_documentation}"

    return ChatResponseSchema(
        user_query=payload.message,
        retrieved_context=matched_documentation,
        ai_synthesis=generated_ai_text
    )
