#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setting up Monitoring Stack${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose not found. Installing...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create Grafana datasource configuration
mkdir -p monitoring/grafana/datasources
cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

# Create Grafana dashboard provisioning
mkdir -p monitoring/grafana/dashboards
cat > monitoring/grafana/dashboards/dashboard.yml << EOF
apiVersion: 1

providers:
  - name: 'CalcBurst'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF

# Create CloudWatch Exporter config
mkdir -p monitoring/cloudwatch-exporter
cat > monitoring/cloudwatch-exporter/config.yml << EOF
region: us-east-1
metrics:
  - aws_namespace: AWS/Lambda
    aws_metric_name: Invocations
    aws_dimensions: [FunctionName]
    aws_statistics: [Sum]
    
  - aws_namespace: AWS/Lambda
    aws_metric_name: Errors
    aws_dimensions: [FunctionName]
    aws_statistics: [Sum]
    
  - aws_namespace: AWS/Lambda
    aws_metric_name: Duration
    aws_dimensions: [FunctionName]
    aws_statistics: [Average]
    
  - aws_namespace: AWS/Lambda
    aws_metric_name: Throttles
    aws_dimensions: [FunctionName]
    aws_statistics: [Sum]
    
  - aws_namespace: AWS/DynamoDB
    aws_metric_name: SuccessfulRequestLatency
    aws_dimensions: [TableName]
    aws_statistics: [Average]
    
  - aws_namespace: AWS/ApiGateway
    aws_metric_name: Count
    aws_dimensions: [ApiName]
    aws_statistics: [Sum]
    
  - aws_namespace: AWS/ApiGateway
    aws_metric_name: 5XXError
    aws_dimensions: [ApiName]
    aws_statistics: [Sum]
EOF

# Create Alertmanager config
mkdir -p monitoring/alertmanager
cat > monitoring/alertmanager/config.yml << EOF
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:5001/alerts'
EOF

# Start monitoring stack
echo -e "${GREEN}Starting monitoring containers...${NC}"
cd monitoring
docker-compose up -d

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Monitoring stack is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Prometheus: http://localhost:9090${NC}"
echo -e "${YELLOW}Grafana: http://localhost:3000${NC}"
echo -e "${YELLOW}  Username: admin${NC}"
echo -e "${YELLOW}  Password: calcburst2024${NC}"
echo -e "${YELLOW}Pushgateway: http://localhost:9091${NC}"
echo -e "${GREEN}========================================${NC}"

cd ..

