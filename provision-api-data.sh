#!/bin/bash

BASE_DOMAIN=https://tnnze9frd0.execute-api.us-east-1.amazonaws.com/dev


curl -H "Content-Type: application/json" -X DELETE ${BASE_DOMAIN}/routes


for file in data/routes/*.json
do
  curl -H "Content-Type: application/json" -X POST ${BASE_DOMAIN}/routes -d @"$file"
done



curl -H "Content-Type: application/json" -X DELETE ${BASE_DOMAIN}/pointsOfInterest


for file in data/points-of-interest/*.json
do
  curl -H "Content-Type: application/json" -X POST ${BASE_DOMAIN}/pointsOfInterest -d @"$file"
done
