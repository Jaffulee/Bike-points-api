"""
Main script to extract and upload bike point data.

This script performs the following actions in sequence:
1. Extracts bike point data from the TfL API and saves it locally as JSON files.
2. Uploads the extracted JSON files from the local directory to an S3 bucket.

Modules:
    - extract_bike_files: Fetches data from the TfL BikePoint API.
    - load_bike_json: Uploads JSON files from the local directory to AWS S3.
"""

from load_bike_json_s3 import load_bike_json
from output_bike_json_files import extract_bike_files

# Extract bike data from the TfL API and save locally
extract_bike_files()

# Upload saved JSON files to the configured S3 bucket
load_bike_json()
