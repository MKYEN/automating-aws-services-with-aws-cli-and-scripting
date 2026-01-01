#!/usr/bin/env python3
import boto3
import datetime

# Connect to CloudWatch
cloudwatch = boto3.client('cloudwatch')

# Generate random number
import random
value = random.randint(1, 100)

# Send the metric
cloudwatch.put_metric_data(
    Namespace='Custom',
    MetricData=[
        {
            'MetricName': 'HighLow',
            'Value': value,
            'Timestamp': datetime.datetime.utcnow()
        }
    ]
)

print(f"Sent metric value: {value}")