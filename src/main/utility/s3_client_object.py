import boto3


class S3ClientProvider:
    #Takes aws_access_key and aws_secret_key and return a s3 object
    def __init__(self, aws_access_key=None, aws_secret_key=None):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key
        )
        self.s3_client = self.session.client('s3')

    def get_client(self):
        return self.s3_client
        