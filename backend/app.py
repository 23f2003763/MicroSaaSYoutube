from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI(title="AlgoMirror API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to the Netlify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

def extract_video_id(url: str):
    """Extracts the video ID from various forms of YouTube URLs."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    
    # Check for short form youtu.be
    short_pattern = r'youtu\.be\/([0-9A-Za-z_-]{11})'
    match = re.search(short_pattern, url)
    if match:
        return match.group(1)
        
    return None

@app.post("/analyze")
async def analyze_video(request: AnalyzeRequest):
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        # 1. Extract Transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine text
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # TODO: Replace the mock below with an actual LLM API call
        # e.g., response = openai.ChatCompletion.create(...)
        
        # 2. Mock LLM Response
        free_analysis = {
            "hook_length": "15 seconds",
            "word_count": len(full_transcript.split()),
            "estimated_read_time": f"{max(1, len(full_transcript.split()) // 150)} mins",
            "main_points": [
                "The importance of strong visual hooks in the first 5 seconds.",
                "Pacing changes to maintain audience retention.",
                "A clear payoff structure during the climax."
            ]
        }
        
        premium_template = {
            "title_ideas": [
                "The secret to [Topic] that nobody tells you",
                "How I achieved [Result] in [Timeframe]",
                "Stop doing [Common Mistake] (Do this instead)"
            ],
            "script_structure": {
                "hook": "[0:00 - 0:15] Open with a bold claim about [Topic] and agitate the viewer's pain point regarding [Pain Point].",
                "intro": "[0:15 - 0:45] Introduce the solution: [Core Concept] and show a quick montage of proof.",
                "body_1": "[0:45 - 2:00] Step 1: Explain the biggest misconception about [Topic].",
                "body_2": "[2:00 - 4:00] Step 2: Introduce the unique mechanism. Use the analogy of [Analogy] to explain it.",
                "climax": "[4:00 - 5:30] The 'Aha' moment: Reveal the final crucial step that ties everything together.",
                "cta": "[5:30 - end] Tell the viewer to subscribe for more on [Topic] and click the link in the description for [Offer]."
            }
        }
        
        return {
            "status": "success",
            "free_analysis": free_analysis,
            "premium_template": premium_template
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")

# To run locally: uvicorn app:app --reload
