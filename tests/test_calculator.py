import unittest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lambda'))

from calculation_handler import perform_calculation, lambda_handler

class TestCalculationEngine(unittest.TestCase):
    
    def test_addition(self):
        result = perform_calculation('add', [10, 20, 30])
        self.assertEqual(result, 60)
    
    def test_subtraction(self):
        result = perform_calculation('subtract', [100, 30, 20])
        self.assertEqual(result, 50)
    
    def test_multiplication(self):
        result = perform_calculation('multiply', [5, 4, 2])
        self.assertEqual(result, 40)
    
    def test_division(self):
        result = perform_calculation('divide', [100, 5, 2])
        self.assertEqual(result, 10)
    
    def test_power(self):
        result = perform_calculation('power', [2, 8])
        self.assertEqual(result, 256)
    
    def test_modulo(self):
        result = perform_calculation('modulo', [17, 5])
        self.assertEqual(result, 2)
    
    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            perform_calculation('divide', [10, 0])
    
    def test_invalid_operation(self):
        with self.assertRaises(ValueError):
            perform_calculation('invalid', [10, 20])
    
    def test_insufficient_operands(self):
        with self.assertRaises(ValueError):
            perform_calculation('add', [10])

class TestLambdaHandler(unittest.TestCase):
    
    def test_valid_request(self):
        event = {
            'body': json.dumps({
                'operation': 'add',
                'operands': [10, 20, 30]
            })
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        
        body = json.loads(response['body'])
        self.assertEqual(body['result'], 60)
    
    def test_missing_operation(self):
        event = {
            'body': json.dumps({
                'operands': [10, 20]
            })
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
    
    def test_missing_operands(self):
        event = {
            'body': json.dumps({
                'operation': 'add'
            })
        }
        
        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()

