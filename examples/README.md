# CalcBurst Client Examples

This directory contains example client implementations for the CalcBurst API in various programming languages.

## Available Examples

### Python Client (`python_client.py`)

A comprehensive Python client using the `requests` library.

**Requirements**:
```bash
pip install requests
```

**Usage**:
```bash
# Update API_URL in the script first
python python_client.py
```

**Features**:
- Simple method calls for each operation
- Batch calculation support
- Error handling examples
- Performance testing
- Detailed metadata access

### Node.js Client (`nodejs_client.js`)

A modern Node.js client using `axios` and async/await.

**Requirements**:
```bash
npm install
```

**Usage**:
```bash
# Update API_URL in the script first
node nodejs_client.js
```

**Features**:
- Promise-based API
- Parallel batch calculations
- Error handling
- Performance benchmarking

## Quick Start

### 1. Get Your API URL

After deploying CalcBurst, get your API Gateway URL:

```bash
cd infrastructure/terraform
terraform output api_gateway_url
```

### 2. Update Examples

Replace the `API_URL` in each example file with your actual API endpoint.

### 3. Run Examples

**Python**:
```bash
cd examples
python python_client.py
```

**Node.js**:
```bash
cd examples
npm install
node nodejs_client.js
```

## Example Output

```
============================================================
CalcBurst Python Client Examples
============================================================

1. Addition: 10 + 20 + 30
   Result: 60

2. Subtraction: 100 - 30 - 20
   Result: 50

3. Multiplication: 5 × 4 × 3
   Result: 60

4. Division: 100 ÷ 5 ÷ 2
   Result: 10

5. Power: 2^10
   Result: 1024

6. Modulo: 17 % 5
   Result: 2

7. Detailed calculation with metadata
   Calculation ID: calc-1706180400000
   Operation: multiply
   Operands: [12, 13, 14]
   Result: 2184
   Execution Time: 8.45ms
   Timestamp: 2024-01-25T10:00:00.000Z

8. Batch calculations
   Batch 1: add = 6
   Batch 2: multiply = 120
   Batch 3: power = 256

9. Error handling - Division by zero
   Caught expected error: 400 Client Error

10. Performance test - 100 calculations
    Total time: 2456.78ms
    Average per request: 24.57ms
    Throughput: 40.71 req/sec

============================================================
All examples completed successfully!
============================================================
```

## Integration into Your Application

### Python

```python
from calcburst_client import CalcBurstClient

client = CalcBurstClient("https://your-api-url.com/prod/calculate")

# Simple usage
result = client.add(10, 20, 30)
print(f"Sum: {result}")

# With error handling
try:
    result = client.divide(100, 5, 2)
    print(f"Division result: {result}")
except Exception as e:
    print(f"Error: {e}")
```

### Node.js

```javascript
const CalcBurstClient = require('./nodejs_client');

const client = new CalcBurstClient('https://your-api-url.com/prod/calculate');

async function example() {
  try {
    // Simple usage
    const sum = await client.add(10, 20, 30);
    console.log(`Sum: ${sum}`);

    // Batch operations
    const operations = [
      { operation: 'add', operands: [1, 2, 3] },
      { operation: 'multiply', operands: [4, 5, 6] }
    ];
    const results = await client.batchCalculate(operations);
    console.log('Results:', results);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

example();
```

## Advanced Usage

### Custom Calculation IDs

```python
result = client.calculate(
    operation='add',
    operands=[10, 20, 30],
    calc_id='my-custom-id-123'
)
```

### Retry Logic

```python
import time

def calculate_with_retry(client, operation, operands, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.calculate(operation, operands)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Rate Limiting

```python
import time
from threading import Semaphore

rate_limiter = Semaphore(100)  # Max 100 concurrent requests

def rate_limited_calculate(client, operation, operands):
    with rate_limiter:
        result = client.calculate(operation, operands)
        time.sleep(0.01)  # Small delay between requests
        return result
```

## Testing

Both example clients include built-in tests. To run them:

**Python**:
```bash
python python_client.py
```

**Node.js**:
```bash
node nodejs_client.js
```

## Troubleshooting

### Connection Errors

- Verify your API URL is correct
- Check that the API Gateway is deployed
- Ensure you have internet connectivity

### Authentication Errors

- If API keys are enabled, add them to request headers
- Check IAM permissions if using AWS authentication

### Timeout Errors

- Increase timeout in client configuration
- Check Lambda function timeout settings
- Verify DynamoDB is responding

## Contributing

To add examples in other languages:

1. Create a new file: `language_client.ext`
2. Implement the CalcBurstClient class
3. Add examples demonstrating all operations
4. Update this README with usage instructions
5. Submit a pull request

## License

MIT License - see LICENSE file for details

