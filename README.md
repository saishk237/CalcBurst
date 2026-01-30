# CalcBurst - Serverless Real-time Calculation Engine

A high-performance, serverless calculation engine built on AWS infrastructure, designed to handle 100,000 transactions per minute with single-digit millisecond latency.

## Architecture Overview

CalcBurst leverages AWS serverless technologies to provide a scalable, highly available calculation service with comprehensive monitoring and observability.

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   API Gateway       │
│  (REST API)         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐         ┌──────────────────┐
│   Lambda Function   │────────▶│    DynamoDB      │
│  (Python 3.11)      │         │  (PAY_PER_REQ)   │
│  - Calculation      │         │  - Calculations  │
│  - Validation       │         │  - TTL: 30 days  │
│  - Metrics Export   │         │  - PITR Enabled  │
└──────┬──────────────┘         └──────────────────┘
       │
       │ Metrics
       ▼
┌─────────────────────┐
│  Prometheus         │
│  Push Gateway       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐         ┌──────────────────┐
│   Prometheus        │────────▶│    Grafana       │
│   (Time Series DB)  │         │  (Visualization) │
└─────────────────────┘         └──────────────────┘
```

## Key Features

### High Performance
- **100,000 TPM**: Handles 100,000 transactions per minute with automated scaling
- **Low Latency**: Single-digit millisecond response times
- **Concurrent Execution**: Supports 1,000 concurrent Lambda executions

### Scalability
- **Auto-scaling**: Lambda automatically scales based on demand
- **DynamoDB On-Demand**: Pay-per-request billing with automatic capacity management
- **No Infrastructure Management**: Fully serverless architecture

### Reliability
- **High Availability**: Multi-AZ deployment across AWS regions
- **Disaster Recovery**: Point-in-time recovery enabled for DynamoDB
- **Error Handling**: Comprehensive error handling and retry logic

### Observability
- **Real-time Monitoring**: Prometheus metrics collection every 15 seconds
- **Visual Dashboards**: Grafana dashboards for system health tracking
- **Alerting**: Automated alerts for errors, latency, and throttling
- **CloudWatch Integration**: Native AWS metrics and logging

## Supported Operations

CalcBurst supports the following mathematical operations:

- **Addition** (`add`): Sum of multiple numbers
- **Subtraction** (`subtract`): Sequential subtraction
- **Multiplication** (`multiply`): Product of multiple numbers
- **Division** (`divide`): Sequential division with zero-check
- **Power** (`power`): Exponentiation
- **Modulo** (`modulo`): Remainder operation

## Technology Stack

### AWS Services
- **AWS Lambda**: Serverless compute (Python 3.11)
- **API Gateway**: RESTful API endpoint
- **DynamoDB**: NoSQL database with on-demand capacity
- **CloudWatch**: Logging and native AWS metrics
- **IAM**: Security and access management

### Monitoring Stack
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Push Gateway**: Metrics aggregation for Lambda
- **CloudWatch Exporter**: AWS metrics to Prometheus bridge
- **Alertmanager**: Alert routing and management

### Infrastructure as Code
- **Terraform**: Infrastructure provisioning and management
- **Docker Compose**: Local monitoring stack deployment

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Python 3.11
- Docker and Docker Compose (for monitoring)

### Quick Deployment

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/calcburst.git
cd calcburst
```

2. **Deploy infrastructure**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh prod us-east-1
```

3. **Setup monitoring**
```bash
chmod +x scripts/setup-monitoring.sh
./scripts/setup-monitoring.sh
```

4. **Test the API**
```bash
curl -X POST https://your-api-url.amazonaws.com/prod/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add",
    "operands": [10, 20, 30]
  }'
```

## API Usage

### Request Format

```json
{
  "operation": "add|subtract|multiply|divide|power|modulo",
  "operands": [number1, number2, ...],
  "id": "optional-calculation-id"
}
```

### Response Format

```json
{
  "calculation_id": "calc-1234567890",
  "operation": "add",
  "operands": [10, 20, 30],
  "result": 60,
  "execution_time_ms": 8.45,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Example Requests

**Addition**
```bash
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "operands": [100, 200, 300]}'
```

**Multiplication**
```bash
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "operands": [5, 10, 2]}'
```

**Power**
```bash
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "operands": [2, 10]}'
```

## Performance Testing

Run load tests to verify 100k TPM capacity:

```bash
chmod +x scripts/load-test.sh
./scripts/load-test.sh https://your-api-url.amazonaws.com/prod/calculate 60 100
```

This simulates high-throughput scenarios and generates performance reports.

## Monitoring and Observability

### Accessing Dashboards

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `calcburst2024`
  
- **Prometheus**: http://localhost:9090

- **Push Gateway**: http://localhost:9091

### Key Metrics

- **Request Rate**: Transactions per minute (TPM)
- **Latency**: P50, P95, P99 response times
- **Error Rate**: Failed requests per second
- **Active Requests**: Concurrent executions
- **Lambda Duration**: Function execution time
- **DynamoDB Latency**: Database operation latency

### Alerts

Automated alerts are configured for:
- High error rate (> 5% for 5 minutes)
- High latency (P95 > 500ms for 5 minutes)
- Lambda throttling
- DynamoDB high latency (> 100ms)
- API Gateway 5xx errors

## Project Structure

```
calcburst/
├── lambda/
│   ├── calculation_handler.py      # Main Lambda function
│   ├── metrics_exporter.py         # Metrics export to Prometheus
│   └── requirements.txt            # Python dependencies
├── infrastructure/
│   └── terraform/
│       ├── main.tf                 # Main infrastructure config
│       ├── variables.tf            # Input variables
│       └── outputs.tf              # Output values
├── monitoring/
│   ├── docker-compose.yml          # Monitoring stack
│   ├── prometheus/
│   │   ├── prometheus.yml          # Prometheus config
│   │   └── alerts.yml              # Alert rules
│   └── grafana/
│       └── dashboards/
│           └── calcburst-dashboard.json
├── scripts/
│   ├── deploy.sh                   # Deployment automation
│   ├── load-test.sh                # Performance testing
│   └── setup-monitoring.sh         # Monitoring setup
├── tests/
│   └── test_calculator.py          # Unit tests
└── README.md
```

## Development

### Running Tests

```bash
cd tests
python -m pytest test_calculator.py -v
```

### Local Development

1. Install dependencies:
```bash
pip install -r lambda/requirements.txt
```

2. Run unit tests:
```bash
python -m unittest discover tests
```

3. Test Lambda function locally:
```bash
python lambda/calculation_handler.py
```

## Infrastructure Details

### DynamoDB Schema

**Table Name**: `calcburst-calculations`

| Attribute | Type | Description |
|-----------|------|-------------|
| calculation_id | String (PK) | Unique calculation identifier |
| operation | String | Operation type |
| operands | List | Input numbers |
| result | Number | Calculation result |
| timestamp | String | ISO 8601 timestamp |
| execution_time_ms | Number | Processing time |
| ttl | Number | Time-to-live (30 days) |

**Indexes**:
- TimestampIndex (GSI): Query by timestamp

### Lambda Configuration

- **Runtime**: Python 3.11
- **Memory**: 512 MB
- **Timeout**: 30 seconds
- **Concurrent Executions**: 1,000 reserved
- **Environment Variables**:
  - `DYNAMODB_TABLE`: Table name
  - `PROMETHEUS_GATEWAY`: Metrics endpoint
  - `LOG_LEVEL`: Logging level

### Cost Optimization

- **DynamoDB**: On-demand billing (pay per request)
- **Lambda**: Pay per invocation and compute time
- **API Gateway**: Pay per API call
- **CloudWatch**: Free tier covers basic logging
- **Data Transfer**: Minimal with regional deployment

**Estimated Monthly Cost** (100k TPM):
- Lambda: ~$50
- DynamoDB: ~$30
- API Gateway: ~$35
- CloudWatch: ~$10
- **Total**: ~$125/month

## Security

- **IAM Roles**: Least privilege access for Lambda
- **Encryption**: DynamoDB server-side encryption enabled
- **API Gateway**: CORS configured, rate limiting available
- **VPC**: Can be deployed in VPC for enhanced security
- **Secrets**: No hardcoded credentials

## Troubleshooting

### High Latency
- Check CloudWatch Logs for Lambda errors
- Verify DynamoDB capacity metrics
- Review Grafana latency dashboard

### Throttling
- Increase Lambda reserved concurrency
- Check API Gateway throttle limits
- Review CloudWatch metrics

### Failed Deployments
- Verify AWS credentials
- Check Terraform state
- Review IAM permissions

## Contributing

This project was developed as a demonstration of serverless architecture best practices. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Contact

For questions or support, please open an issue in the GitHub repository.

---

**Built with** ❤️ **by Saish Kothawade**

