import json
import boto3
import time
import os
from decimal import Decimal
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'calcburst-calculations')
table = dynamodb.Table(table_name)

# Prometheus metrics
REQUEST_COUNT = Counter('calcburst_requests_total', 'Total calculation requests')
REQUEST_LATENCY = Histogram('calcburst_request_latency_seconds', 'Request latency')
CALCULATION_ERRORS = Counter('calcburst_errors_total', 'Total calculation errors')
ACTIVE_REQUESTS = Gauge('calcburst_active_requests', 'Currently active requests')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def perform_calculation(operation, operands):
    """
    Perform mathematical calculations based on operation type
    Supports: add, subtract, multiply, divide, power, modulo
    """
    if len(operands) < 2:
        raise ValueError("At least two operands required")
    
    result = operands[0]
    
    if operation == 'add':
        for num in operands[1:]:
            result += num
    elif operation == 'subtract':
        for num in operands[1:]:
            result -= num
    elif operation == 'multiply':
        for num in operands[1:]:
            result *= num
    elif operation == 'divide':
        for num in operands[1:]:
            if num == 0:
                raise ValueError("Division by zero")
            result /= num
    elif operation == 'power':
        result = operands[0] ** operands[1]
    elif operation == 'modulo':
        result = operands[0] % operands[1]
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return result

def store_calculation(calc_id, operation, operands, result, execution_time):
    """
    Store calculation result in DynamoDB with metadata
    """
    try:
        item = {
            'calculation_id': calc_id,
            'operation': operation,
            'operands': [Decimal(str(op)) for op in operands],
            'result': Decimal(str(result)),
            'timestamp': datetime.utcnow().isoformat(),
            'execution_time_ms': Decimal(str(execution_time)),
            'ttl': int(time.time()) + 2592000  # 30 days TTL
        }
        
        table.put_item(Item=item)
        logger.info(f"Stored calculation {calc_id} successfully")
        return True
    except Exception as e:
        logger.error(f"DynamoDB error: {str(e)}")
        CALCULATION_ERRORS.inc()
        return False

def lambda_handler(event, context):
    """
    Main Lambda handler for calculation requests
    """
    start_time = time.time()
    REQUEST_COUNT.inc()
    ACTIVE_REQUESTS.inc()
    
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        operation = body.get('operation')
        operands = body.get('operands', [])
        calc_id = body.get('id', f"calc-{int(time.time() * 1000)}")
        
        # Validate input
        if not operation or not operands:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing operation or operands'
                })
            }
        
        # Perform calculation
        result = perform_calculation(operation, operands)
        
        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000
        
        # Store in DynamoDB
        store_calculation(calc_id, operation, operands, result, execution_time)
        
        # Record latency
        REQUEST_LATENCY.observe(time.time() - start_time)
        
        # Return response
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'calculation_id': calc_id,
                'operation': operation,
                'operands': operands,
                'result': result,
                'execution_time_ms': round(execution_time, 2),
                'timestamp': datetime.utcnow().isoformat()
            }, cls=DecimalEncoder)
        }
        
        logger.info(f"Calculation {calc_id} completed in {execution_time:.2f}ms")
        return response
        
    except ValueError as e:
        CALCULATION_ERRORS.inc()
        logger.error(f"Validation error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
    except Exception as e:
        CALCULATION_ERRORS.inc()
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }
    finally:
        ACTIVE_REQUESTS.dec()

