/**
 * CalcBurst Node.js Client Example
 * 
 * This script demonstrates how to interact with the CalcBurst API
 * using Node.js and axios.
 */

const axios = require('axios');

class CalcBurstClient {
  /**
   * Initialize the CalcBurst client
   * @param {string} apiUrl - Base URL of the CalcBurst API
   */
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
    this.client = axios.create({
      baseURL: apiUrl,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Perform a calculation
   * @param {string} operation - Operation type
   * @param {number[]} operands - Array of numbers
   * @param {string} calcId - Optional custom calculation ID
   * @returns {Promise<Object>} Calculation result
   */
  async calculate(operation, operands, calcId = null) {
    try {
      const payload = {
        operation,
        operands
      };

      if (calcId) {
        payload.id = calcId;
      }

      const response = await this.client.post('', payload);
      return response.data;
    } catch (error) {
      console.error('Error:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Add numbers together
   */
  async add(...numbers) {
    const result = await this.calculate('add', numbers);
    return result.result;
  }

  /**
   * Subtract numbers sequentially
   */
  async subtract(...numbers) {
    const result = await this.calculate('subtract', numbers);
    return result.result;
  }

  /**
   * Multiply numbers together
   */
  async multiply(...numbers) {
    const result = await this.calculate('multiply', numbers);
    return result.result;
  }

  /**
   * Divide numbers sequentially
   */
  async divide(...numbers) {
    const result = await this.calculate('divide', numbers);
    return result.result;
  }

  /**
   * Calculate base raised to exponent
   */
  async power(base, exponent) {
    const result = await this.calculate('power', [base, exponent]);
    return result.result;
  }

  /**
   * Calculate remainder of division
   */
  async modulo(dividend, divisor) {
    const result = await this.calculate('modulo', [dividend, divisor]);
    return result.result;
  }

  /**
   * Perform multiple calculations in parallel
   * @param {Array<Object>} operations - Array of operation objects
   * @returns {Promise<Array>} Array of results
   */
  async batchCalculate(operations) {
    const promises = operations.map(op =>
      this.calculate(op.operation, op.operands)
        .catch(error => ({ error: error.message }))
    );
    return await Promise.all(promises);
  }
}

async function main() {
  // Replace with your actual API URL
  const API_URL = 'https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/calculate';
  
  const client = new CalcBurstClient(API_URL);

  console.log('='.repeat(60));
  console.log('CalcBurst Node.js Client Examples');
  console.log('='.repeat(60));

  try {
    // Example 1: Addition
    console.log('\n1. Addition: 10 + 20 + 30');
    let result = await client.add(10, 20, 30);
    console.log(`   Result: ${result}`);

    // Example 2: Subtraction
    console.log('\n2. Subtraction: 100 - 30 - 20');
    result = await client.subtract(100, 30, 20);
    console.log(`   Result: ${result}`);

    // Example 3: Multiplication
    console.log('\n3. Multiplication: 5 × 4 × 3');
    result = await client.multiply(5, 4, 3);
    console.log(`   Result: ${result}`);

    // Example 4: Division
    console.log('\n4. Division: 100 ÷ 5 ÷ 2');
    result = await client.divide(100, 5, 2);
    console.log(`   Result: ${result}`);

    // Example 5: Power
    console.log('\n5. Power: 2^10');
    result = await client.power(2, 10);
    console.log(`   Result: ${result}`);

    // Example 6: Modulo
    console.log('\n6. Modulo: 17 % 5');
    result = await client.modulo(17, 5);
    console.log(`   Result: ${result}`);

    // Example 7: Detailed result with metadata
    console.log('\n7. Detailed calculation with metadata');
    const detailedResult = await client.calculate('multiply', [12, 13, 14]);
    console.log(`   Calculation ID: ${detailedResult.calculation_id}`);
    console.log(`   Operation: ${detailedResult.operation}`);
    console.log(`   Operands: ${detailedResult.operands}`);
    console.log(`   Result: ${detailedResult.result}`);
    console.log(`   Execution Time: ${detailedResult.execution_time_ms}ms`);
    console.log(`   Timestamp: ${detailedResult.timestamp}`);

    // Example 8: Batch calculations
    console.log('\n8. Batch calculations');
    const operations = [
      { operation: 'add', operands: [1, 2, 3] },
      { operation: 'multiply', operands: [4, 5, 6] },
      { operation: 'power', operands: [2, 8] }
    ];
    const results = await client.batchCalculate(operations);
    results.forEach((result, i) => {
      if (!result.error) {
        console.log(`   Batch ${i + 1}: ${result.operation} = ${result.result}`);
      } else {
        console.log(`   Batch ${i + 1}: Error - ${result.error}`);
      }
    });

    // Example 9: Error handling
    console.log('\n9. Error handling - Division by zero');
    try {
      await client.divide(10, 0);
    } catch (error) {
      console.log(`   Caught expected error: ${error.message}`);
    }

    // Example 10: Performance measurement
    console.log('\n10. Performance test - 100 calculations');
    const startTime = Date.now();
    const perfPromises = [];
    for (let i = 0; i < 100; i++) {
      perfPromises.push(client.add(i, i + 1, i + 2));
    }
    await Promise.all(perfPromises);
    const endTime = Date.now();
    const totalTime = endTime - startTime;
    const avgTime = totalTime / 100;
    console.log(`    Total time: ${totalTime}ms`);
    console.log(`    Average per request: ${avgTime.toFixed(2)}ms`);
    console.log(`    Throughput: ${(100 / (totalTime / 1000)).toFixed(2)} req/sec`);

    console.log('\n' + '='.repeat(60));
    console.log('All examples completed successfully!');
    console.log('='.repeat(60));

  } catch (error) {
    console.error('Error running examples:', error.message);
  }
}

// Run examples if this file is executed directly
if (require.main === module) {
  main();
}

module.exports = CalcBurstClient;

