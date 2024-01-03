#!/usr/bin/env python3

import json
import os
from typing import Any

import boto3
import structlog
from aws_lambda_typing import context as context_
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.responses import APIGatewayProxyResponseV2
from pydantic import BaseModel

# Configure structlog to use the standard library's logging module
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,  # Filter logs by level
        structlog.stdlib.add_logger_name,  # Add logger name to log entries
        structlog.stdlib.add_log_level,  # Add log level to log entries
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),  # Add timestamps to log entries
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,  # Include exception info in log entries
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,  # Render log entries to keyword arguments
    ],
    context_class=dict,  # Use a dict to store the context
    logger_factory=structlog.stdlib.LoggerFactory(),  # Use the standard library's logging module
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Create a logger
logger = structlog.get_logger()


# Bind the aws_request_id to the logger
def setup_logger(context):
    return logger.bind(aws_request_id=context.aws_request_id)


# Initialize the S3 client
s3_client = boto3.client("s3", region_name=os.environ["AWS_REGION"])


class Response(BaseModel):
    buckets: list[str]


def success_response(buckets: list[str]) -> APIGatewayProxyResponseV2:
    return APIGatewayProxyResponseV2(
        statusCode=200,
        body=Response(buckets=buckets).model_dump_json(),
        headers={"Content-Type": "application/json"},
    )


def error_response(message: str, status_code: int = 500) -> APIGatewayProxyResponseV2:
    return APIGatewayProxyResponseV2(
        statusCode=status_code,
        body=json.dumps({"message": message}),
        headers={"Content-Type": "application/json"}
    )


def lambda_handler(event: APIGatewayProxyEventV2,
                   context: context_.Context) -> APIGatewayProxyResponseV2:
    logger = setup_logger(context)

    # Parse the incoming event body
    print(event)
    logger.info("Parsing event body", lambda_event=event)
    data: dict[str, Any] = json.loads(event['body'])
    logger.info("Received event", data=data)

    try:
        response = s3_client.list_buckets()
        logger.info("S3 buckets", buckets=response["Buckets"])
        return success_response(buckets=[bucket["Name"] for bucket in response["Buckets"]])
    except Exception as error:
        logger.exception("Error listing S3 buckets")
        return error_response(f"Error listing S3 buckets: {error}", status_code=500)
