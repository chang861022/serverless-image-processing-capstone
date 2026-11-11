# Serverless Image Processing Pipeline

## Project Overview
The goal of this project is to automatically create a thumbnail when an image is uploaded to an Amazon S3 bucket. AWS Lambda resizes the image and saves the thumbnail in a second bucket. An API Gateway endpoint lets users start the resizing workflow through AWS Step Functions.

## Deployment Instructions
### 1. Create the S3 buckets
Create two general purpose S3 buckets in Canada (Central), `ca-central-1`. Keep **Block all public access** enabled for both buckets.

| Purpose | Bucket name used in this project |
| --- | --- |
| Store original images | `chang-chih-shiuan-capstone-originals-20261110` |
| Store thumbnails | `chang-chih-shiuan-capstone-thumbnails-20261110` |

When deploying in another AWS account, choose two unique bucket names.