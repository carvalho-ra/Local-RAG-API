#!/usr/bin/env python3

from app.storage import client, MINIO_BUCKET


for obj in client.list_objects(MINIO_BUCKET, recursive=True):
    print(obj.object_name) 
