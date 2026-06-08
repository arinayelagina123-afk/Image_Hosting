#!/bin/sh
set -eu

pg_dump \
  -h db \
  -U postgres \
  -d images_db \
  -F c \
  -f "/backups/backup_$(date +%Y%m%d_%H%M%S).dump"
