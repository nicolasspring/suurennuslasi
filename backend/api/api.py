from fastapi import FastAPI

app = FastAPI()


@app.get("/posts")
def get_posts():
    return [
        {
            "id": "1",
            "caption": "Weekend in Zurich",
            "latitude": 47.3769,
            "longitude": 8.5417,
            "image_url": "...",
        }
    ]
