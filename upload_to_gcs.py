#!/usr/bin/env python3
"""Upload slides and videos to GCS bucket using ADC."""

import sys
import os
from pathlib import Path
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT = os.getenv("PROJECT_NUMBER") or os.getenv("PROJECT_NAME", "videogeneration-484813").split('/')[-1]
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "infinite-context-presentation")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")


def ensure_bucket(client, bucket_name):
    """Create bucket if it doesn't exist."""
    try:
        bucket = client.get_bucket(bucket_name)
        print(f"✓ Bucket exists: gs://{bucket_name}")
        return bucket
    except Exception:
        print(f"  Creating bucket gs://{bucket_name}...")
        bucket = client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        bucket = client.create_bucket(bucket, project=PROJECT, location=LOCATION)
        print(f"✓ Created bucket: gs://{bucket_name}")
        return bucket


def upload_directory(bucket, local_dir, gcs_prefix):
    """Upload all files from a local directory to GCS."""
    local_path = Path(local_dir)
    if not local_path.exists():
        print(f"  ✗ Directory not found: {local_dir}")
        return 0

    files = sorted(local_path.glob("*"))
    files = [f for f in files if f.is_file() and not f.name.startswith('.')]
    count = 0
    for f in files:
        blob_name = f"{gcs_prefix}/{f.name}"
        blob = bucket.blob(blob_name)
        print(f"  Uploading {f.name} ({f.stat().st_size // 1024} KB)...", end=" ")
        blob.upload_from_filename(str(f))
        print("✓")
        count += 1
    return count


def main():
    client = storage.Client(project=PROJECT)
    bucket = ensure_bucket(client, BUCKET_NAME)

    # Upload slides
    print("\n=== Uploading slides ===")
    slide_count = upload_directory(bucket, "slides", "slides")
    print(f"  Uploaded {slide_count} slides")

    # Upload videos (whatever exists so far)
    print("\n=== Uploading videos ===")
    video_count = upload_directory(bucket, "videos", "videos")
    print(f"  Uploaded {video_count} videos")

    # Upload V1 presentation if it exists
    v1 = Path("presentation.mp4")
    if v1.exists():
        print(f"\n  Uploading presentation.mp4 ({v1.stat().st_size // (1024*1024)} MB)...", end=" ")
        blob = bucket.blob("presentation.mp4")
        blob.upload_from_filename(str(v1))
        print("✓")

    print(f"\n=== Done! ===")
    print(f"  Browse: https://console.cloud.google.com/storage/browser/{BUCKET_NAME}")
    print(f"  GCS path: gs://{BUCKET_NAME}/")


if __name__ == "__main__":
    main()
