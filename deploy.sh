#!/bin/bash
set -euo pipefail

# Deployment script for Google Cloud Run (production)
PROJECT_ID="innate-client-508813-e6"
PROJECT_NUMBER="687594214295"
REGION="europe-west1"
SERVICE_NAME="ataskaitos"
SERVICE_ACCOUNT="ataskaitos-run@${PROJECT_ID}.iam.gserviceaccount.com"
SQL_INSTANCE="${PROJECT_ID}:${REGION}:ataskaitos-prod"
GCS_BUCKET="ataskaitos-prod-${PROJECT_NUMBER}"

echo "Deploying to project: $PROJECT_ID"

# Build and deploy in one command
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --platform managed \
    --allow-unauthenticated \
    --service-account "$SERVICE_ACCOUNT" \
    --add-cloudsql-instances "$SQL_INSTANCE" \
    --set-env-vars "ENV=production,USE_GCS=true,GCS_BUCKET_NAME=${GCS_BUCKET},GCS_PROJECT_ID=${PROJECT_ID}" \
    --update-secrets OPENAI_API_KEY=openai-api-key:latest,API_KEY=ataskaitos-api-key:latest,DATABASE_URL=ataskaitos-database-url:latest,JWT_SECRET=ataskaitos-jwt-secret:latest \
    --memory 1Gi \
    --cpu 2 \
    --max-instances 1 \
    --port 8080

echo "Deployment complete!"
echo "Service URL:"
gcloud run services describe "$SERVICE_NAME" \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --format 'value(status.url)'
