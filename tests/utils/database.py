import boto3

def create_test_table(table_name):
    client = boto3.client('dynamodb')
    client.create_table(
      TableName=table_name,
      AttributeDefinitions=[{
        'AttributeName': 'PK',
        'AttributeType': 'S',
      }, {
        'AttributeName': 'SK',
        'AttributeType': 'S',
      }],
      KeySchema=[{
        'AttributeName': 'PK',
        'KeyType': 'HASH',
      }, {
        'AttributeName': 'SK',
        'KeyType': 'RANGE',
      }],
      BillingMode='PAY_PER_REQUEST'
    )