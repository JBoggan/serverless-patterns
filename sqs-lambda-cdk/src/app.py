from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as eventsources,
    aws_logs as logs,
    aws_sqs as sqs,
    core as cdk,
)


class SQSLambdaStack(cdk.Stack):
    def __init__(self, app: cdk.App, id: str) -> None:
        super().__init__(app, id)

        # SQS queue
        queue = sqs.Queue(self, 'sqs-to-lambda-test')

        dlq = sqs.Queue(self, "DLQ")

        # Lambda Function
        lambdaFn = _lambda.Function(self, "SQSEventHandler",
                                    runtime=_lambda.Runtime.PYTHON_3_9,
                                    code=_lambda.Code.from_asset("lambda"),
                                    handler="handler.main",
                                    timeout=cdk.Duration.seconds(10),
                                    dead_letter_queue = dlq)

        # subscribe Lambda to SQS queue
        lambdaFn.add_event_source(eventsources.SqsEventSource(queue))   

        # Set Lambda Logs Retention and Removal Policy
        logs.LogGroup(
            self,
            'logs',
            log_group_name=f"/aws/lambda/{lambdaFn.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.ONE_DAY
        )

        
        # Output information about the created resources
        cdk.CfnOutput(self, 'sqsQueueArn',
                      value=queue.queue_arn,
                      description='The arn of the SQS queue')

        cdk.CfnOutput(self, 'sqsQueueUrl',
                     value=queue.queue_url,
                    description='The URL of the SQS queue')

        cdk.CfnOutput(self, 'sqsDLQueueArn',
                      value=dlq.queue_arn,
                      description='The arn of the SQS dead letter queue')
        cdk.CfnOutput(self, 'functionName',
                      value=lambdaFn.function_name,
                      description='The name of the handler function')


app = cdk.App()
SQSLambdaStack(app, "SQSLambdaStackExample")
app.synth()
