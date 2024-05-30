#!/bin/bash

pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"
status=$?

if [ $status -eq 0 ]; then
  echo "PostgreSQL is ready"
  exit 0
else
  echo "PostgreSQL is not ready"
  exit 1
fi