import os
from collections import defaultdict

import pandas as pd
import numpy as np

from db import DBClient
from schemas import VideoSchema, PredictedVideoSchema, TVShow, ContentInfo


SIMILARITY_THRESHOLD = 0.9
DATA_PATH = os.environ.get("DATA_FILEPATH")
DATA_SHEET_NAME = os.environ.get("DATA_SHEET_NAME", "in")

db = DBClient()


def read_input_data(file_path: str, sheet_name: str):
    # read the Excel file
    return pd.read_excel(file_path, sheet_name=sheet_name)


def analyse_and_insert_data():
    input_data = read_input_data(DATA_PATH, DATA_SHEET_NAME)

    true_grouped_data = input_data.groupby([
        'tvshow', 'actual_label']).size().reset_index(name='count')
    total_counts = true_grouped_data.groupby('tvshow')[
        'count'].transform('sum')
    true_grouped_data['percentage'
        ] = (true_grouped_data['count'] / total_counts) * 100

    grouped_data = input_data.groupby([
        'tvshow', 'actual_label', 'predicted_label']).size(
    ).reset_index(name='count')
    total_counts = grouped_data.groupby('tvshow')['count'].transform('sum')
    grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

    # transform data to the document schema
    tvshows_actual_data = defaultdict(list)
    for _, row in true_grouped_data.iterrows():
        tvshows_actual_data[row.tvshow].append(ContentInfo(
            label=row.actual_label,
            percentage=round(float(row.percentage), 2)))

    # transform data to the document schema
    tvshows_predicted_data = defaultdict(list)
    for _, row in grouped_data.iterrows():
        tvshows_predicted_data[row.tvshow].append(ContentInfo(
            label=row.predicted_label,
            percentage=round(float(row.percentage), 2)))

    tvshow_names = set()
    tvshow_names.update(tvshows_actual_data.keys())
    tvshow_names.update(tvshows_predicted_data.keys())

    # insert documents into collection
    db.tvshows_collection.insert_many([
        TVShow(name=name,
               actual_content_percentage=tvshows_actual_data[name],
               predicted_content_percentage=tvshows_predicted_data[name]
               ).to_dict()
        for name in tvshow_names
    ])

    # transform string vector to the float numpy array
    vectors = np.array([list(map(float, vector.split(', ')))
                        for vector in input_data.feature_vector])

    # normalize the vectors to have one unit length
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized_vectors = vectors / norms

    # compute the cosine similarity matrix
    cosine_similarity_matrix = np.dot(normalized_vectors, normalized_vectors.T)

    # set the diagonal to 0 to ignore self-similarity
    np.fill_diagonal(cosine_similarity_matrix, 0)

    # extract the upper diagonal part of the matrix
    upper_cosine_similarity_matrix = np.triu(cosine_similarity_matrix)

    # use similarity indices to find similar videos
    similarity_indices = np.argwhere(
        upper_cosine_similarity_matrix > SIMILARITY_THRESHOLD)

    videos_predict_map = defaultdict(list)
    videos_actual_map = defaultdict(list)
    for first, second in similarity_indices:
        if (input_data.predicted_label[first]
                == input_data.predicted_label[second]):

            videos_predict_map[input_data.content_id[first]].append(
                PredictedVideoSchema(id=input_data.content_id[second],
                                     label=input_data.predicted_label[second]))

            videos_predict_map[input_data.content_id[second]].append(
                PredictedVideoSchema(id=input_data.content_id[first],
                                     label=input_data.predicted_label[first]))

        if (input_data.actual_label[first]
                == input_data.actual_label[second]):
            videos_actual_map[input_data.content_id[first]].append(
                input_data.content_id[second])
            videos_actual_map[input_data.content_id[second]].append(
                input_data.content_id[first])

    # transform data to the document schema
    videos_data = []
    for _, video in input_data.iterrows():
        videos_data.append(VideoSchema(
            id=video.content_id,
            actual_label=video.actual_label,
            predicted_label=video.predicted_label,
            actual_label_similarity_videos_ids=videos_actual_map[
                video.content_id],
            predicted_label_similarity_videos=videos_predict_map[
                video.content_id]
        ).to_dict())

    # insert documents into collection
    db.videos_collection.insert_many(videos_data)


if __name__ == '__main__':
    analyse_and_insert_data()
