#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}CalcBurst Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Terraform is not installed. Please install it first.${NC}"
    exit 1
fi

# Set environment
ENVIRONMENT=${1:-prod}
AWS_REGION=${2:-us-east-1}

echo -e "${YELLOW}Environment: ${ENVIRONMENT}${NC}"
echo -e "${YELLOW}AWS Region: ${AWS_REGION}${NC}"

# Create deployment package
echo -e "${GREEN}Creating Lambda deployment package...${NC}"
cd lambda
pip install -r requirements.txt -t package/
cp calculation_handler.py package/
cp metrics_exporter.py package/
cd package
zip -r ../deployment-package.zip .
cd ..
rm -rf package
cd ..

echo -e "${GREEN}Lambda package created successfully${NC}"

# Initialize Terraform
echo -e "${GREEN}Initializing Terraform...${NC}"
cd infrastructure/terraform
terraform init

# Plan deployment
echo -e "${GREEN}Planning Terraform deployment...${NC}"
terraform plan \
  -var="aws_region=${AWS_REGION}" \
  -var="environment=${ENVIRONMENT}" \
  -out=tfplan

# Apply deployment
echo -e "${YELLOW}Applying Terraform configuration...${NC}"
terraform apply tfplan

# Get outputs
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Outputs:${NC}"
terraform output

# Save outputs to file
terraform output -json > ../../outputs.json

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}API Gateway URL saved to outputs.json${NC}"
echo -e "${GREEN}========================================${NC}"

cd ../..

# Test the endpoint
echo -e "${YELLOW}Testing API endpoint...${NC}"
API_URL=$(terraform -chdir=infrastructure/terraform output -raw api_gateway_url)

curl -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "operands": [10, 20, 30]}' \
  | jq '.'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment and testing complete!${NC}"
echo -e "${GREEN}========================================${NC}"

