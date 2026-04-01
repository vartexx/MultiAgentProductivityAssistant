# Cloud Run Deployment Guide

This guide explains how to deploy the Multi-Agent Productivity Assistant to Google Cloud Run.

## Prerequisites

1. Google Cloud SDK installed: https://cloud.google.com/sdk/docs/install
2. Docker installed locally
3. GCP Project: `Multi-Agent-Vartexx`
4. Authenticated gcloud CLI: `gcloud auth login`

## Step-by-Step Deployment

### 1. Set up GCP environment variables
```bash
export PROJECT_ID=Multi-Agent-Vartexx
export SERVICE_NAME=multi-agent-productivity-assistant
export REGION=us-central1
export IMAGE=gcr.io/$PROJECT_ID/$SERVICE_NAME
```

### 2. Configure gcloud
```bash
gcloud config set project $PROJECT_ID
gcloud auth configure-docker gcr.io
```

### 3. Build Docker image locally (optional for testing)
```bash
docker build -t $SERVICE_NAME:latest .
docker run -p 8000:8000 $SERVICE_NAME:latest
# Test: curl http://localhost:8000/health
```

### 4. Push image to Google Container Registry
```bash
docker build -t $IMAGE:latest .
docker push $IMAGE:latest
```

### 5. Deploy to Cloud Run
```bash
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --timeout=300 \
  --set-env-vars="APP_NAME=Multi-Agent Productivity Assistant"
```

### 6. Retrieve service URL
```bash
gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)'
```

### 7. Test deployed service
```bash
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
curl $SERVICE_URL/health
curl $SERVICE_URL/docs
```

## Optional: Connect External MCP Services

If you have external MCP services running, deploy them similarly and then update environment variables:

```bash
gcloud run deploy $SERVICE_NAME \
  --update-env-vars="CALENDAR_MCP_URL=https://calendar-service-url/,TASK_MCP_URL=https://task-service-url/" \
  --region=$REGION
```

## Monitoring and Logs

### View logs
```bash
gcloud run logs read $SERVICE_NAME --region=$REGION --limit 50
```

### View metrics
```bash
gcloud run services describe $SERVICE_NAME --region=$REGION
```

## Cleanup

To delete the Cloud Run service:
```bash
gcloud run services delete $SERVICE_NAME --region=$REGION
```

To delete the image from Container Registry:
```bash
gcloud container images delete $IMAGE:latest
```
