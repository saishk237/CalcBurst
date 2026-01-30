#!/bin/bash

# Load testing script for CalcBurst
# Simulates high throughput to test 1 lakh TPM capacity

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

API_URL=${1:-"https://your-api-gateway-url.amazonaws.com/prod/calculate"}
DURATION=${2:-60}
CONCURRENT=${3:-100}

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}CalcBurst Load Testing${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}API URL: ${API_URL}${NC}"
echo -e "${YELLOW}Duration: ${DURATION} seconds${NC}"
echo -e "${YELLOW}Concurrent requests: ${CONCURRENT}${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if Apache Bench is installed
if ! command -v ab &> /dev/null; then
    echo -e "${RED}Apache Bench (ab) is not installed.${NC}"
    echo -e "${YELLOW}Installing apache2-utils...${NC}"
    sudo apt-get update && sudo apt-get install -y apache2-utils
fi

# Create test payload
cat > /tmp/calcburst-payload.json << EOF
{
  "operation": "add",
  "operands": [123.45, 678.90, 234.56]
}
EOF

# Calculate total requests for target TPM
TOTAL_REQUESTS=$((DURATION * 1667))  # ~100k requests per minute

echo -e "${GREEN}Starting load test...${NC}"
echo -e "${YELLOW}Target: 100,000 TPM${NC}"
echo -e "${YELLOW}Total requests: ${TOTAL_REQUESTS}${NC}"

# Run Apache Bench
ab -n ${TOTAL_REQUESTS} \
   -c ${CONCURRENT} \
   -p /tmp/calcburst-payload.json \
   -T application/json \
   -g /tmp/calcburst-results.tsv \
   ${API_URL}

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Load test completed!${NC}"
echo -e "${GREEN}Results saved to /tmp/calcburst-results.tsv${NC}"
echo -e "${GREEN}========================================${NC}"

# Cleanup
rm /tmp/calcburst-payload.json

