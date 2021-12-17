import json
import boto3
import os 

sqs_client = boto3.client("sqs", region_name="us-west-2")

def main(event, context):
	message = {"key": "Hello, SQS!"}
	queue_url = os.environ['QUEUE_URL']
	response = sqs_client.send_message(
	    QueueUrl=queue_url,
	    MessageBody=json.dumps(message)
	)
	print(response)
    return