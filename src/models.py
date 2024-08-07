from pydantic import BaseModel


class PredictedLabelVideosRequest(BaseModel):
    video_id: str
    label: str


class Video(BaseModel):
    id: str
