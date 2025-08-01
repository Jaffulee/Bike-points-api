# Bike Points API

This project automates the process of collecting and storing bike point data from the Transport for London (TfL) BikePoint API.

It performs two main actions:

1. **Extraction**: Downloads the latest bike point data from the TfL API and saves it as a local `.json` file.
2. **Loading**: Uploads the extracted `.json` files to an AWS S3 bucket and deletes the local copies after a successful upload.

---

## 🔧 Requirements

- Python 3.7+
- An `.env` file containing the following variables:
  ```env
  Access_key_ID="your_aws_access_key"
  Secret_access_key="your_aws_secret_key"
  AWS_BUCKET_NAME="your_target_bucket_name"
  ```
