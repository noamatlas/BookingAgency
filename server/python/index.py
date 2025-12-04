from fastapi import FastAPI, HTTPException, Body
from AI_General import (ask_ai)
from AI_Agent_Travel import (ask_ai_agent)
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Booking Agency")

# origins = [
#     "http://localhost:3500",
#     "http://127.0.0.1:3500"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

#routers:
@app.get("/")
def test_api():
	return "Server is online."

   
@app.post("/ask_ai_general")
def ask_ai_general(user_prompt: str = Body(...)):
    try:
        response = ask_ai(user_prompt)
        return response
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/ask_ai_travel")
def ask_ai_travel(user_prompt: str = Body(..., media_type="text/plain")):
    try:
        response = ask_ai_agent(user_prompt)
        return response["output"]
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    

# uvicorn index:app --reload
# http://127.0.0.1:8000/