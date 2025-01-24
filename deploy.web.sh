#!/bin/bash

# deploy.web.sh - Deployment script for Krane web service to Google App Engine
# Usage: ./deploy.web.sh

# Exit on any error
set -e

echo "Starting Krane web service deployment process..."

# 1. Install package in editable mode temporarily
# This makes the package available in development mode and generates necessary egg-info
echo "Installing package in editable mode..."
pip install -e .

# 2. Create a temporary copy of the package for App Engine
# App Engine requires the package to be in the root directory instead of src/
echo "Creating temporary package copy for App Engine..."
cp -r src/krane .

# 3. Deploy to Google App Engine
# Deploy the application using the krane.app.yaml configuration
# The --project flag specifies the GCP project ID
echo "Deploying to Google App Engine..."
gcloud app deploy krane.app.yaml --project barestripe

# 4. Clean up all temporary files and installations
# Remove the temporary copy and uninstall the package
echo "Cleaning up temporary files and installations..."
rm -rf krane
pip uninstall -y krane  # -y flag to skip confirmation prompt

echo "Deployment completed successfully!"