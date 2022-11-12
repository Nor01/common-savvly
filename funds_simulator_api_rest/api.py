from fastapi import FastAPI
from routes.simulator_route import api_router 
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()
app.include_router(api_router)

origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("api:app",reload=True)