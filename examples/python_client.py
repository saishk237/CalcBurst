"""
CalcBurst Python Client Example

This script demonstrates how to interact with the CalcBurst API
using Python's requests library.
"""

import requests
import json
import time
from typing import List, Dict, Any

class CalcBurstClient:
    """Client for interacting with CalcBurst API"""
    
    def __init__(self, api_url: str):
        """
        Initialize the CalcBurst client
        
        Args:
            api_url: Base URL of the CalcBurst API
        """
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def calculate(self, operation: str, operands: List[float], 
                 calc_id: str = None) -> Dict[str, Any]:
        """
        Perform a calculation
        
        Args:
            operation: Operation type (add, subtract, multiply, divide, power, modulo)
            operands: List of numbers to operate on
            calc_id: Optional custom calculation ID
        
        Returns:
            Dictionary containing calculation result and metadata
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        payload = {
            'operation': operation,
            'operands': operands
        }
        
        if calc_id:
            payload['id'] = calc_id
        
        try:
            response = self.session.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    def add(self, *numbers: float) -> float:
        """Add numbers together"""
        result = self.calculate('add', list(numbers))
        return result['result']
    
    def subtract(self, *numbers: float) -> float:
        """Subtract numbers sequentially"""
        result = self.calculate('subtract', list(numbers))
        return result['result']
    
    def multiply(self, *numbers: float) -> float:
        """Multiply numbers together"""
        result = self.calculate('multiply', list(numbers))
        return result['result']
    
    def divide(self, *numbers: float) -> float:
        """Divide numbers sequentially"""
        result = self.calculate('divide', list(numbers))
        return result['result']
    
    def power(self, base: float, exponent: float) -> float:
        """Calculate base raised to exponent"""
        result = self.calculate('power', [base, exponent])
        return result['result']
    
    def modulo(self, dividend: float, divisor: float) -> float:
        """Calculate remainder of division"""
        result = self.calculate('modulo', [dividend, divisor])
        return result['result']
    
    def batch_calculate(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform multiple calculations in parallel
        
        Args:
            operations: List of operation dictionaries
        
        Returns:
            List of results
        """
        results = []
        for op in operations:
            try:
                result = self.calculate(op['operation'], op['operands'])
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        return results


def main():
    """Example usage of CalcBurst client"""
    
    # Replace with your actual API URL
    API_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/calculate"
    
    client = CalcBurstClient(API_URL)
    
    print("=" * 60)
    print("CalcBurst Python Client Examples")
    print("=" * 60)
    
    # Example 1: Addition
    print("\n1. Addition: 10 + 20 + 30")
    result = client.add(10, 20, 30)
    print(f"   Result: {result}")
    
    # Example 2: Subtraction
    print("\n2. Subtraction: 100 - 30 - 20")
    result = client.subtract(100, 30, 20)
    print(f"   Result: {result}")
    
    # Example 3: Multiplication
    print("\n3. Multiplication: 5 × 4 × 3")
    result = client.multiply(5, 4, 3)
    print(f"   Result: {result}")
    
    # Example 4: Division
    print("\n4. Division: 100 ÷ 5 ÷ 2")
    result = client.divide(100, 5, 2)
    print(f"   Result: {result}")
    
    # Example 5: Power
    print("\n5. Power: 2^10")
    result = client.power(2, 10)
    print(f"   Result: {result}")
    
    # Example 6: Modulo
    print("\n6. Modulo: 17 % 5")
    result = client.modulo(17, 5)
    print(f"   Result: {result}")
    
    # Example 7: Detailed result with metadata
    print("\n7. Detailed calculation with metadata")
    result = client.calculate('multiply', [12, 13, 14])
    print(f"   Calculation ID: {result['calculation_id']}")
    print(f"   Operation: {result['operation']}")
    print(f"   Operands: {result['operands']}")
    print(f"   Result: {result['result']}")
    print(f"   Execution Time: {result['execution_time_ms']}ms")
    print(f"   Timestamp: {result['timestamp']}")
    
    # Example 8: Batch calculations
    print("\n8. Batch calculations")
    operations = [
        {'operation': 'add', 'operands': [1, 2, 3]},
        {'operation': 'multiply', 'operands': [4, 5, 6]},
        {'operation': 'power', 'operands': [2, 8]},
    ]
    results = client.batch_calculate(operations)
    for i, result in enumerate(results, 1):
        if 'error' not in result:
            print(f"   Batch {i}: {result['operation']} = {result['result']}")
        else:
            print(f"   Batch {i}: Error - {result['error']}")
    
    # Example 9: Error handling
    print("\n9. Error handling - Division by zero")
    try:
        result = client.divide(10, 0)
    except requests.exceptions.HTTPError as e:
        print(f"   Caught expected error: {e}")
    
    # Example 10: Performance measurement
    print("\n10. Performance test - 100 calculations")
    start_time = time.time()
    for i in range(100):
        client.add(i, i+1, i+2)
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    avg_time = total_time / 100
    print(f"    Total time: {total_time:.2f}ms")
    print(f"    Average per request: {avg_time:.2f}ms")
    print(f"    Throughput: {100 / (total_time/1000):.2f} req/sec")
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

