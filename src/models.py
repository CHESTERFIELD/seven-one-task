from typing import List

from pydantic import BaseModel


class PredictedLabelVideosRequest(BaseModel):
    video_id: str
    label: str


class Video(BaseModel):
    id: str


class ContentInfo(BaseModel):
    label: str
    percentage: float


class TVShow(BaseModel):
    name: str
    actual_content_percentage: List[ContentInfo]
    predicted_content_percentage: List[ContentInfo]
