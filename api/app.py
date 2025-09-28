from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GEMINI_API_KEY or not TAVILY_API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY and TAVILY_API_KEY in .env file")

# Initialize Tavily
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  # ✅ correct model name
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


# FastAPI app
app = FastAPI(
    title="LinkedIn Post Generator API",
    version="1.0",
    description="Generates LinkedIn-style posts based on recent news using Gemini + Tavily"
)

# Request/Response Schemas
class GenerateRequest(BaseModel):
    topic: str

class GenerateResponse(BaseModel):
    topic: str
    news_sources: List[str]
    linkedin_post: str
    image_suggestion: Optional[str] = None


def fetch_news(topic: str, max_results: int = 3) -> List[str]:
    """Fetch recent news URLs using Tavily API"""
    try:
        results = tavily_client.search(topic, max_results=max_results)
        return [res["url"] for res in results.get("results", [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tavily error: {str(e)}")


def generate_linkedin_post(topic: str, news_summary: str) -> str:
    """Use Gemini to generate LinkedIn style post"""
    prompt = ChatPromptTemplate.from_template(
        "You are a professional LinkedIn content creator. "
        "Write a LinkedIn-style post (engaging, professional tone, 3–5 short paragraphs) "
        "based on the topic: {topic} and recent news: {news_summary}. "
        "End with a call-to-action."
    )
    chain = prompt | llm
    response = chain.invoke({"topic": topic, "news_summary": news_summary})
    return response.content


@app.post("/generate-post", response_model=GenerateResponse)
async def generate_post(req: GenerateRequest):
    try:
        # Step 1: Get news URLs
        news_sources = fetch_news(req.topic, max_results=3)
        if not news_sources:
            raise HTTPException(status_code=404, detail="No recent news found")

        # Step 2: Summarize sources into a post
        news_summary = "; ".join(news_sources)
        linkedin_post = generate_linkedin_post(req.topic, news_summary)

        # Step 3: Response
        return GenerateResponse(
            topic=req.topic,
            news_sources=news_sources,
            linkedin_post=linkedin_post,
            image_suggestion=None  # You can extend prompt to include image suggestion
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
