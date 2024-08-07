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


# @dataclasses.dataclass
# class TVShow:
#     name: str
#     title: str
#     actual_label: str
#     predictable_label: str
#     actual_topic: str
#     predictable_topic: str
