#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Defines the rest API for the recommender.

Copyright © 2018 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
from fastapi import FastAPI

from recommendation_engine.predictor.online_recommendation import PMFRecommendation
from rudra.data_store.aws import AmazonS3
import recommendation_engine.config.cloud_constants as cloud_constants
from recommendation_engine.config.cloud_constants import USE_CLOUD_SERVICES, LOCAL_ACCESS
from recommendation_engine.config.params_scoring import ScoringParams
from recommendation_engine.api_models import Package
from typing import List

app = FastAPI()

if USE_CLOUD_SERVICES:
    s3 = AmazonS3(bucket_name=cloud_constants.S3_BUCKET_NAME,  # pragma: no cover
                  aws_access_key_id=cloud_constants.AWS_S3_ACCESS_KEY_ID,
                  aws_secret_access_key=cloud_constants.AWS_S3_SECRET_KEY_ID)
    s3.connect()
elif LOCAL_ACCESS:
    print("INSIDE LOCAL ACCESS")
    s3 = AmazonS3(bucket_name=cloud_constants.S3_BUCKET_NAME,
                  aws_access_key_id=cloud_constants.AWS_S3_ACCESS_KEY_ID,
                  aws_secret_access_key=cloud_constants.AWS_S3_SECRET_KEY_ID,
                  endpoint_url=cloud_constants.AWS_S3_ENDPOINT_URL,
                  local_dev=True)
    s3.connect()
else:
    from rudra.data_store.local_data_store import LocalDataStore
    # Change the source directory here for local file system testing.
    s3 = LocalDataStore('tests/test_data/')
    ScoringParams.num_latent_factors = 5

# This needs to be global as ~200MB of data is loaded from S3 every time an object of this class
# is instantiated.
recommender = PMFRecommendation(ScoringParams.recommendation_threshold,
                                s3,
                                ScoringParams.num_latent_factors)


@app.get('/api/v1/liveness', status_code=200)
def liveness():
    """Define the linveness probe."""
    return {}


@app.get('/api/v1/readiness', status_code=200)
def readiness():
    """Define the readiness probe."""
    return {}


@app.post('/api/v1/companion_recommendation', status_code=200)
def recommendation(payload: List[Package]):
    """Endpoint to serve recommendations."""
    global recommender
    response_json = []
    for recommendation_request in payload:
        missing, recommendations, ip_package_to_topic_dict = recommender.predict(
            recommendation_request.package_list,
            companion_threshold=recommendation_request.comp_package_count_threshold
        )
        response_json.append({
            "missing_packages": missing,
            "companion_packages": recommendations,
            "ecosystem": os.environ.get("CHESTER_SCORING_REGION", "npm"),
            "package_to_topic_dict": ip_package_to_topic_dict
        })
    return response_json


if __name__ == "__main__":
    app.run(debug=True, port=6006)  # pragma: no cover
