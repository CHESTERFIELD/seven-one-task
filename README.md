# FastAPI & MongoDB app

The simple app to analysis input videos data.

Done as part of a technical challenge of Mykyta Mishchenko interview process 
for @7.1 Tech Hub company.

## Features

- Analysis of video content data
- API to retrieve processed data results

## Requirements
```
Docker
Docker-compose
```

## Run

1. Clone the repository:

    ```bash
    git clone https://github.com/CHESTERFIELD/seven-one-app
    ```

2. Run application with docker-compose:

    ```bash
    docker-compose up
    ```

3. To run processing and analysing test data: 

    ```bash
    docker exec -it fastapi python analysis.py
    ```

4. To check an existent API: 

    ```bash
   # API endpoint for getting videos with similar content according to 
   # the processed feature_vector data
    curl http://0.0.0.0:8000/videos/v40357312/similar_videos
    
    # API endpoint for getting videos with similar context for the video 
    # with {video_id} id and {label} predicted label 
    curl -X POST http://0.0.0.0:8000/videos/predicted_label_similarity_videos \
      -H "Content-Type: application/json" \
      -d '{"video_id":"v40357312", "label":"FoodBev"}'
    ```

## Additional

This application contains a couple of API endpoints to retrieve results of 
processed and analysed video input data.

The application is launched in docker-compose so does not require any major 
actions from the user to start working with it.

The .env file contains set of extra env variables that are being used by 
services for their configuration, and can be adjusted according to the user 
needs.


## Build

The build directory contains scripts, Dockerfiles, etc., for building 
application.

## Tests

TBD, not done yet.

## Known Issues

1. Pagination for API endpoints is not implemented;
2. TVShow analysis API endpoints are not finished.
