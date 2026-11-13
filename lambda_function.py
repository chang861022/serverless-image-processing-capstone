import io
import logging
import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image, ImageOps

# Initialize AWS S3 client and logging
s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

THUMBNAIL_SIZE = (256, 256)


def get_image_location(event):
    """Extract the source bucket and image key from the event."""

    # Direct S3 event notification
    if "Records" in event:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

    # EventBridge S3 event
    elif "detail" in event and "bucket" in event["detail"]:
        detail = event["detail"]
        bucket = detail["bucket"]["name"]
        key = detail["object"]["key"]

    # Step Functions or manual test input
    else:
        bucket = event["bucket"]
        key = event["key"]

    return bucket, key


def lambda_handler(event, context):
    """Resize an S3 image and upload its thumbnail."""

    try:
        # Get image location and bucket configuration
        source_bucket, source_key = get_image_location(event)

        expected_source = os.environ["ORIGINAL_BUCKET"]
        destination_bucket = os.environ["THUMBNAIL_BUCKET"]

        if source_bucket != expected_source:
            raise ValueError("Invalid source bucket")

        # Download original image
        response = s3.get_object(
            Bucket=source_bucket,
            Key=source_key
        )
        image_data = response["Body"].read()

        # Resize image while preserving aspect ratio
        with Image.open(io.BytesIO(image_data)) as image:
            image = ImageOps.exif_transpose(image)
            original_size = image.size

            image.thumbnail(
                THUMBNAIL_SIZE,
                Image.Resampling.LANCZOS
            )

            # Replace transparency with a white background
            rgba = image.convert("RGBA")
            thumbnail = Image.new("RGB", rgba.size, "white")
            thumbnail.paste(rgba, mask=rgba.getchannel("A"))

            thumbnail_size = thumbnail.size

            # Save resized image as JPEG in memory
            output = io.BytesIO()
            thumbnail.save(
                output,
                format="JPEG",
                quality=85
            )

        # Upload thumbnail to the destination S3 bucket
        thumbnail_key = f"thumbnails/{source_key}.jpg"

        s3.put_object(
            Bucket=destination_bucket,
            Key=thumbnail_key,
            Body=output.getvalue(),
            ContentType="image/jpeg"
        )

        logger.info(
            "Thumbnail successfully created: %s",
            thumbnail_key
        )

        return {
            "success": True,
            "source_bucket": source_bucket,
            "source_key": source_key,
            "thumbnail_bucket": destination_bucket,
            "thumbnail_key": thumbnail_key,
            "original_size": original_size,
            "thumbnail_size": thumbnail_size
        }

    except Exception as error:
        logger.exception("Image processing failed")

        return {
            "success": False,
            "error": str(error)
        }
