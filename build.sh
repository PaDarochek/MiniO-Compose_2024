#!/bin/bash

set -m
pwd
mkdir minio
MINIO_SCANNER_SPEED=fastest minio server /minio --console-address :9001 &
sleep 10

mc alias set s3 http://127.0.0.1:9000 minioadmin minioadmin

mc mb s3/bucket
mc quota set s3/bucket --size 16MB

mc admin user add s3 user userkey123
mc admin policy attach s3 readwrite --user=user

fg
