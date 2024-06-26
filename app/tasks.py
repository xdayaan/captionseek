# app/tasks.py
import os
import subprocess
import boto3
from botocore.exceptions import ClientError
from celery import shared_task
from django.conf import settings
from .models import Video
import time
from uuid import uuid4

@shared_task
def generate_subtitles(video_id, video_title):
    try:
        video = Video.objects.get(id=video_id)
        video_path = video.video_file.path
        media_path = settings.MEDIA_ROOT

        output_folder = os.path.join(media_path, 'subtitles')
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"{os.path.basename(video_path)}.srt")

        # Extract subtitles from video
        subprocess.run(['ccextractor', video_path, '-o', output_path], check=True)

        # Upload video file to S3
        s3_bucket_name = 'captionseek'
        timestamp = int(time.time())  # Unix timestamp
        unique_filename = f"{timestamp}.mp4"
        s3_object_key = f'videos/{unique_filename}'

        s3_client = boto3.client('s3')
        with open(video_path, 'rb') as file:
            s3_client.upload_fileobj(file, s3_bucket_name, s3_object_key)
        s3_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_object_key}"

        # Read subtitles content
        file_content = ""
        with open(output_path, 'r') as file:
            file_content = file.read()

        # Store metadata in DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('captionseek')

        id = str(uuid4())
        table.put_item(
            Item={
                'id': id,
                'title': video_title,
                'url': s3_url,
                'subtitles': file_content
            }
        )

        # Clean up: delete video and subtitle files
        os.remove(video_path)
        os.remove(output_path)
        print("Both video and subtitle files deleted")

        return output_path  # Return the path of the generated subtitles

    except Video.DoesNotExist:
        raise Exception("Video not found")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running ccextractor: {e}")
    except ClientError as e:
        raise Exception(f"Error uploading to S3: {e}")
    except Exception as e:
        raise Exception(f"Error generating subtitles: {e}")
