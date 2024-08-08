import dataclasses
from typing import List


@dataclasses.dataclass
class PredictedVideoSchema:
    id: str
    label: str


@dataclasses.dataclass
class VideoSchema:
    id: str
    actual_label: str
    predicted_label: str
    actual_label_similarity_videos_ids: List[str]
    predicted_label_similarity_videos: List['PredictedVideoSchema']

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class ContentInfo:
    label: str
    percentage: float


@dataclasses.dataclass
class TVShow:
    name: str
    actual_content_percentage: List[ContentInfo]
    predicted_content_percentage: List[ContentInfo]

    def to_dict(self):
        return dataclasses.asdict(self)
