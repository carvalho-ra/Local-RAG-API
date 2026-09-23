#!/usr/bin/env python3

from app.storage import client, MINIO_BUCKET


for obj in client.list_objects(MINIO_BUCKET, recursive=True):
    client.remove_object(MINIO_BUCKET, obj.object_name)
    print(f"Removed: {obj.object_name}")