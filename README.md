
# Serverless Image Processing Pipeline

## 1. Project Overview

This capstone project uses AWS serverless services to resize images into thumbnails.

Amazon S3 stores original and resized images, AWS Lambda performs image processing using Python and Pillow, and AWS Step Functions manages the workflow. Amazon API Gateway will provide an endpoint to trigger the state machine.

**Current Status:** The Lambda function and Step Functions success workflow have been successfully tested. The automatic S3 trigger and API Gateway integration are not yet completed.

## 2. System Architecture

The system uses the following AWS services:

- **Amazon S3:** Stores original images and generated thumbnails in separate buckets.
- **AWS Lambda:** Resizes images using Python and Pillow.
- **AWS Step Functions:** Orchestrates image processing using Task, Choice, Succeed, and Fail states.
- **Amazon API Gateway:** Provides an endpoint to start the workflow (pending).
- **Amazon CloudWatch:** Records Lambda execution logs.

### Workflow

1. An image is uploaded to the original S3 bucket.
2. AWS Lambda processes the image and creates a thumbnail.
3. The thumbnail is saved to the destination S3 bucket.
4. Step Functions checks whether image processing was successful.
5. The workflow enters the Success or Fail state.

Automatic upload triggering and API Gateway integration are still being configured.

## 3. AWS Resources and Prerequisites

The project requires an AWS account with access to S3, Lambda, Step Functions, API Gateway, IAM, and CloudWatch.

| Resource | Configuration |
|---|---|
| AWS Region | Canada (Central) - ca-central-1 |
| Original S3 Bucket | `chang-chih-shiuan-capstone-originals` |
| Thumbnail S3 Bucket | `chang-chih-shiuan-capstone-thumbnails` |
| Lambda Function | `CapstoneResizeImage` |
| Runtime | Python 3.14 |
| Image Processing Library | Pillow 13.0.0 |
| Lambda Layer | `CapstonePillow` Version 2 |
| Lambda Memory | 512 MB |
| Lambda Timeout | 30 seconds |
| Step Functions | `CapstoneImageProcessingWorkflow` |
| State Machine Type | Standard |
| API Gateway | Pending configuration |

The Step Functions ARN and API Gateway URL will be documented after the remaining integrations are completed.

## 4. Deployment Instructions

### Step 1: Create S3 Buckets

Create two S3 buckets in the Canada (Central) region:

- `chang-chih-shiuan-capstone-originals`
- `chang-chih-shiuan-capstone-thumbnails`

Keep public access blocked for both buckets.

### Step 2: Create the Lambda Function

1. Create a Lambda function named `CapstoneResizeImage`.
2. Select Python 3.14 and x86_64 architecture.
3. Add the Python image processing code from `lambda_function.py`.
4. Create and attach a compatible Pillow Lambda Layer.
5. Set memory to 512 MB and timeout to 30 seconds.

Configure these environment variables:

- `ORIGINAL_BUCKET=chang-chih-shiuan-capstone-originals`
- `THUMBNAIL_BUCKET=chang-chih-shiuan-capstone-thumbnails`

Configure IAM permissions to allow:

- `s3:GetObject` on the original bucket.
- `s3:PutObject` on the thumbnail bucket.
- CloudWatch logging.

### Step 3: Create Step Functions

Create a Standard state machine named `CapstoneImageProcessingWorkflow`.

Use the definition in `state_machine.json`.

The workflow includes:

1. **ResizeImage:** Invokes the Lambda function.
2. **CheckResizeResult:** Checks whether `$.success` equals `true`.
3. **Success:** Ends the workflow successfully.
4. **Fail:** Ends the workflow when image processing fails.

The execution role must have permission to invoke the Lambda function.

### Step 4: Configure API Gateway and S3 Trigger

Configure an API Gateway endpoint to start the Step Functions state machine.

Configure automatic processing when a new image is uploaded to the original S3 bucket.

**Status:** These integrations are not yet completed.

## 5. How to Run and Test

The following manual Step Functions test has been completed successfully.

1. Upload an image named `test picture.png` to the original S3 bucket.
2. Open `CapstoneImageProcessingWorkflow` in AWS Step Functions.
3. Click **Start execution**.
4. Enter the following JSON input:

```json
{
  "bucket": "chang-chih-shiuan-capstone-originals",
  "key": "test picture.png"
}
```

5. Start the execution.
6. Verify that the workflow reaches the Success state.
7. Open the thumbnail S3 bucket.
8. Verify that `thumbnails/test picture.png.jpg` has been created.

## 6. Testing Results

### Successful Execution

The Step Functions workflow was tested successfully on November 12, 2026.

| Test Item | Result |
|---|---|
| Execution Status | Succeeded |
| Execution Duration | 5.222 seconds |
| Lambda Invocation | Successful |
| Choice State | Successful |
| Final State | Success |
| Thumbnail Created | Yes |

The Lambda function resized the original image and saved the thumbnail to the destination S3 bucket.

### Execution Status Screenshot

![Step Functions Execution Success](StepFunctions_Execution_Success.jpeg)

### Workflow Execution Screenshot

The following screenshot shows the successful execution path:

**ResizeImage → CheckResizeResult → Success**

![Step Functions Workflow Success](StepFunctions_Workflow_Success.jpeg)

