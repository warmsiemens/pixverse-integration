import uvicorn
from fastapi import FastAPI
from app.api.v1 import videos
from app.db.database import engine
from app.models import video

app = FastAPI()
app.include_router(videos.router)


if __name__ == '__main__':
    video.Base.metadata.create_all(bind=engine)
    uvicorn.run('main:app', reload=True)
