terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDB Table for calculations
resource "aws_dynamodb_table" "calculations" {
  name           = "calcburst-calculations"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "calculation_id"
  
  attribute {
    name = "calculation_id"
    type = "S"
  }
  
  attribute {
    name = "timestamp"
    type = "S"
  }
  
  global_secondary_index {
    name            = "TimestampIndex"
    hash_key        = "timestamp"
    projection_type = "ALL"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  point_in_time_recovery {
    enabled = true
  }
  
  server_side_encryption {
    enabled = true
  }
  
  tags = {
    Name        = "CalcBurst Calculations"
    Environment = var.environment
    Project     = "CalcBurst"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "calcburst-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name    = "CalcBurst Lambda Role"
    Project = "CalcBurst"
  }
}

# IAM Policy for Lambda
resource "aws_iam_role_policy" "lambda_policy" {
  name = "calcburst-lambda-policy"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:UpdateItem"
        ]
        Resource = [
          aws_dynamodb_table.calculations.arn,
          "${aws_dynamodb_table.calculations.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "calculator" {
  filename         = "../lambda/deployment-package.zip"
  function_name    = "calcburst-calculator"
  role            = aws_iam_role.lambda_role.arn
  handler         = "calculation_handler.lambda_handler"
  source_code_hash = filebase64sha256("../lambda/deployment-package.zip")
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 512
  
  environment {
    variables = {
      DYNAMODB_TABLE     = aws_dynamodb_table.calculations.name
      PROMETHEUS_GATEWAY = var.prometheus_gateway
      LOG_LEVEL         = "INFO"
    }
  }
  
  reserved_concurrent_executions = 1000
  
  tags = {
    Name        = "CalcBurst Calculator"
    Environment = var.environment
    Project     = "CalcBurst"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.calculator.function_name}"
  retention_in_days = 7
  
  tags = {
    Name    = "CalcBurst Lambda Logs"
    Project = "CalcBurst"
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "calcburst_api" {
  name        = "CalcBurstAPI"
  description = "API for CalcBurst calculation engine"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  
  tags = {
    Name    = "CalcBurst API"
    Project = "CalcBurst"
  }
}

# API Gateway Resource
resource "aws_api_gateway_resource" "calculate" {
  rest_api_id = aws_api_gateway_rest_api.calcburst_api.id
  parent_id   = aws_api_gateway_rest_api.calcburst_api.root_resource_id
  path_part   = "calculate"
}

# API Gateway Method
resource "aws_api_gateway_method" "calculate_post" {
  rest_api_id   = aws_api_gateway_rest_api.calcburst_api.id
  resource_id   = aws_api_gateway_resource.calculate.id
  http_method   = "POST"
  authorization = "NONE"
}

# API Gateway Integration
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.calcburst_api.id
  resource_id             = aws_api_gateway_resource.calculate.id
  http_method             = aws_api_gateway_method.calculate_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.calculator.invoke_arn
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.calculator.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.calcburst_api.execution_arn}/*/*"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "calcburst_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
  
  rest_api_id = aws_api_gateway_rest_api.calcburst_api.id
  stage_name  = var.environment
}

# API Gateway Stage
resource "aws_api_gateway_stage" "calcburst_stage" {
  deployment_id = aws_api_gateway_deployment.calcburst_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.calcburst_api.id
  stage_name    = var.environment
  
  xray_tracing_enabled = true
  
  tags = {
    Name        = "CalcBurst API Stage"
    Environment = var.environment
    Project     = "CalcBurst"
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "calcburst-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "This metric monitors lambda errors"
  
  dimensions = {
    FunctionName = aws_lambda_function.calculator.function_name
  }
  
  tags = {
    Name    = "CalcBurst Lambda Errors Alarm"
    Project = "CalcBurst"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "calcburst-lambda-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "This metric monitors lambda throttles"
  
  dimensions = {
    FunctionName = aws_lambda_function.calculator.function_name
  }
  
  tags = {
    Name    = "CalcBurst Lambda Throttles Alarm"
    Project = "CalcBurst"
  }
}

