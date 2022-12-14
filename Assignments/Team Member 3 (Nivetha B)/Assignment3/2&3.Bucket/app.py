from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.ap.cloud-object-storage.appdomain.cloud/"

COS_API_KEY_ID = "3Z5-MbwAgH5Lb20qDSxmGG43euCd2vxFFIiSjQcWFRcK"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/3e321662c56f487f9700184fa54559d3:9cbbd38e-0af9-47af-b4dd-b3b02cf77a43::"

# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud
cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)

def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()

        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))

@app.route('/')
def index():
    file1 = get_bucket_contents('first02')
    return render_template('index.html', files=file1)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089, debug=True)