from fastapi import FastAPI, HTTPException
from typing import List

from db import DBClient
from models import Video, PredictedLabelVideosRequest, TVShow

app = FastAPI()
db = DBClient()


@app.get("/videos/{video_id}/similar_videos", response_model=List[Video])
def get_similar_content_for_video(video_id: str):
    video = list(db.videos_collection.find({"id": video_id}))
    if not video:
        raise HTTPException(status_code=404,
                            detail="Requested video is not found")
    return [{"id": sim_video_id} for sim_video_id
            in video[0]["actual_label_similarity_videos_ids"]]


@app.post("/videos/predicted_label_similarity_videos",
          response_model=List[Video])
def get_similar_content_for_video_by_predicted_label(
        request: PredictedLabelVideosRequest):
    video = list(db.videos_collection.find({"id": request.video_id}))
    if not video:
        raise HTTPException(status_code=400,
                            detail="Invalid request data")

    # TODO: add pagination
    result = []
    for similar_video in video[0]["predicted_label_similarity_videos"]:
        if similar_video["label"] == request.label:
            result.append({"id": similar_video["id"]})
    return result


@app.get("/tvshows", response_model=List[TVShow])
def get_tv_show_detailed_info_by_id():
    return list(db.tvshows_collection.find())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
