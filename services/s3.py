import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.bucket_name = config("AWS_BUCKET")
        self.region = config("AWS_REGION")

        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )

    def upload_photo(self, file_name, object_name):
        try:
            ext = file_name.split(".")[-1]
            self.s3.upload_file(
                file_name,
                self.bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"},
            )
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_name}"
        except ClientError:
            raise InternalServerError(
                "Provider is not available at the moment. " "Please try again later"
            )

    def delete_photo(self, object_key):
        self.s3.Object(self.bucket_name, object_key).delete()
