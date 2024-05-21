#!/bin/bash

redis-cli ping
status=$?

if [ $status -eq 0 ]; then
  echo "redis is ready"
  exit 0
else
  echo "redis is not ready"
  exit 1
fi