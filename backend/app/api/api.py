from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/posts")
async def get_posts():
    return [
        {
            "id": "1",
            "caption": "A sunny day in Zurich.",
            "latitude": 47.3769,
            "longitude": 8.5417,
        }
    ]
