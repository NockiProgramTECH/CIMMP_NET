import boto3
import json

s3 = boto3.client(
    's3',
    endpoint_url='http://192.168.1.66:3900',
    aws_access_key_id='GK36585bb667d2b9df10a292c8',
    aws_secret_access_key='bd07599fd632c59a047487893473fc56772980fa61f0b79d5eda15c0955193df',
    region_name='garage',
)

policy = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::video/*"
        }
    ]
})

s3.put_bucket_policy(Bucket='video', Policy=policy)
print("✅ Policy publique appliquée sur le bucket 'video'")