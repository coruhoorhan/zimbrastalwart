#!/bin/bash
# PostgreSQL dump
docker exec stalwart-postgres pg_dump -U stalwart stalwart > /opt/stalwart-stack/backup/stalwart_$(date +%F).sql

echo "Backup finished."
