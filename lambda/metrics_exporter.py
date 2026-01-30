import json
import boto3
import os
from datetime import datetime, timedelta
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CloudWatch client
cloudwatch = boto3.client('cloudwatch')
dynamodb = boto3.resource('dynamodb')

# Prometheus gateway
PROMETHEUS_GATEWAY = os.environ.get('PROMETHEUS_GATEWAY', 'localhost:9091')
registry = CollectorRegistry()

# Metrics
lambda_invocations = Gauge('calcburst_lambda_invocations', 'Lambda invocations', registry=registry)
lambda_errors = Gauge('calcburst_lambda_errors', 'Lambda errors', registry=registry)
lambda_duration = Gauge('calcburst_lambda_duration_ms', 'Lambda duration', registry=registry)
dynamodb_consumed_capacity = Gauge('calcburst_dynamodb_consumed_capacity', 'DynamoDB consumed capacity', registry=registry)
api_gateway_requests = Gauge('calcburst_api_requests', 'API Gateway requests', registry=registry)

def get_cloudwatch_metrics():
    """
    Fetch metrics from CloudWatch
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    
    metrics = {}
    
    try:
        # Lambda invocations
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Invocations',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'calcburst-calculator'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum']
        )
        if response['Datapoints']:
            metrics['invocations'] = response['Datapoints'][0]['Sum']
        
        # Lambda errors
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Errors',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'calcburst-calculator'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum']
        )
        if response['Datapoints']:
            metrics['errors'] = response['Datapoints'][0]['Sum']
        
        # Lambda duration
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Duration',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': 'calcburst-calculator'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        if response['Datapoints']:
            metrics['duration'] = response['Datapoints'][0]['Average']
        
        # API Gateway requests
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/ApiGateway',
            MetricName='Count',
            Dimensions=[
                {'Name': 'ApiName', 'Value': 'CalcBurstAPI'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum']
        )
        if response['Datapoints']:
            metrics['api_requests'] = response['Datapoints'][0]['Sum']
            
    except Exception as e:
        logger.error(f"Error fetching CloudWatch metrics: {str(e)}")
    
    return metrics

def lambda_handler(event, context):
    """
    Export metrics to Prometheus Push Gateway
    """
    try:
        metrics = get_cloudwatch_metrics()
        
        # Update Prometheus metrics
        if 'invocations' in metrics:
            lambda_invocations.set(metrics['invocations'])
        if 'errors' in metrics:
            lambda_errors.set(metrics['errors'])
        if 'duration' in metrics:
            lambda_duration.set(metrics['duration'])
        if 'api_requests' in metrics:
            api_gateway_requests.set(metrics['api_requests'])
        
        # Push to Prometheus Gateway
        push_to_gateway(PROMETHEUS_GATEWAY, job='calcburst-metrics', registry=registry)
        
        logger.info("Metrics exported successfully")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Metrics exported successfully',
                'metrics': metrics
            })
        }
        
    except Exception as e:
        logger.error(f"Error exporting metrics: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

