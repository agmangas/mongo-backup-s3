#!/bin/bash

set -e

: ${MONGO_HOST:?}
: ${MONGO_DB:?}
: ${S3_BUCKET:?}
: ${AWS_ACCESS_KEY_ID:?}
: ${AWS_SECRET_ACCESS_KEY:?}

FOLDER=/backup
DUMPOUT=dump

DATEFORMAT=${DATEFORMAT-"%Y%m%d-%H%M%S"}
FILEPREFIX=${FILEPREFIX-"backup-"}

FILENAME=${FILEPREFIX}$(date -u +${DATEFORMAT}).tar.gz

echo "Creating backup folder..."

mkdir -p ${FOLDER} && cd ${FOLDER}

echo "Starting backup..."

mongodump --host=${MONGO_HOST} --db=${MONGO_DB} --out=${DUMPOUT}

echo "Compressing backup..."

tar -zcvf ${FILENAME} ${DUMPOUT} && rm -fr ${DUMPOUT}

echo "Uploading to S3..."

aws s3api put-object --bucket ${S3_BUCKET} --key ${FILENAME} --body ${FILENAME}

echo "Done!"
