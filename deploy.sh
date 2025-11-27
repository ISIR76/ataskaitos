#!/bin/bash
set -e

# Simple deployment script for Google Cloud Run
PROJECT_ID="delves-sandbox"
REGION="europe-west1"
SERVICE_NAME="ataskaitos"

echo "Deploying to project: $PROJECT_ID"

# Build and deploy in one command
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --project $PROJECT_ID \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars ENV=production \
    --update-secrets OPENAI_API_KEY=openai-api-key:latest,API_KEY=ataskaitos-api-key:latest \
    --memory 1Gi \
    --cpu 2 \
    --max-instances 1 \
    --port 8080

echo "Deployment complete!"
echo "Service URL:"
gcloud run services describe $SERVICE_NAME \
    --project $PROJECT_ID \
    --region $REGION \
    --format 'value(status.url)'
