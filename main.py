from fastapi import FastAPI
#lets you send the AI response back to the browser word by word, as it generates, instead of waiting for the full response
from fastapi.responses import StreamingResponse
#a security setting. By default browsers block requests between different origins (e.g. your HTML file talking to your Python server). This middleware allows it
from fastapi.middleware.cors import CORSMiddleware
#define exactly what data shape you expect from the frontend. If required fields are missing, FastAPI automatically rejects the request with an error
from pydantic import BaseModel, validator
#reads .env file and loads
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime
import os

from prompts import build_itinerary_prompt

load_dotenv() # read .env file

#Productionizing with API check at startup
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Check your .env file.")

#creates one reusable Groq client for the whole app
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#creates web application instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItineraryRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    travel_style: str
    dietary_prefs: str
    budget: str

    #Productionizing with input validation
    @validator("destination", "dietary_prefs")
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("This field cannot be empty")
        return v
    
    @validator("end_date")
    def end_must_be_after_start(cls, end_date, values):
        if "start_date" in values:
            start = datetime.strptime(values["start_date"], "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if end <= start:
                raise ValueError("End date must be after start date")
            if (end - start).days > 14:
                raise ValueError("Trip length cannot exceed 14 days")
        return end_date

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
def generate_itinerary(request: ItineraryRequest):
    prompt = build_itinerary_prompt(
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        travel_style=request.travel_style,
        dietary_prefs=request.dietary_prefs,
        budget=request.budget,
    )

    def stream():
        #Productionizing with error handling
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in response:
                text = chunk.choices[0].delta.content
                if text:
                    yield text
        except Exception as e:
            yield f"\n\n Something went wrong while generating your itinerary: {str(e)}"

    return StreamingResponse(stream(), media_type="text/plain")