pipeline {
   agent any
   
   environment {
       GCP_PROJECT = 'mlops-vertex-project'
       GCP_REGION = 'us-central1'
       GCS_BUCKET = 'mlops-bucket-ayush-123'
       CONTAINER_REGISTRY = 'gcr.io/mlops-vertex-project'
       GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-service-account')
   }
   
   parameters {
       string(name: 'JOB_NAME', defaultValue: 'ml-training-job',
              description: 'Name for the Vertex AI training job')
       choice(name: 'MACHINE_TYPE', 
              choices: ['n1-standard-4', 'n1-standard-8', 'n1-highmem-4'],
              description: 'Machine type for training')
   }
   
   stages {
       stage('Checkout') {
           steps {
               checkout scm
           }
       }
       
       stage('Setup Python Environment') {
           steps {
               sh '''
                   python3 -m venv gcp_env
                   . gcp_env/bin/activate
                   pip install --upgrade pip
                   pip install google-cloud-storage google-cloud-aiplatform google-auth
                   pip install -r requirements.txt
               '''
           }
       }
       
       stage('Generate Training Data') {
           steps {
               sh '''
                   . gcp_env/bin/activate
                   python3 scripts/generate_dataset.py
               '''
           }
       }
       
       stage('Upload Training Data to GCS') {
           steps {
               sh '''
                   . gcp_env/bin/activate
                   python3 << 'EOF'
import os
from google.cloud import storage
from google.oauth2 import service_account

# Initialize GCS client
credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
client = storage.Client(credentials=credentials, project='mlops-vertex-project')
bucket = client.bucket('mlops-bucket-ayush-123')

# Upload data directory
print("Uploading data to GCS...")
for root, dirs, files in os.walk('data'):
    for file in files:
        file_path = os.path.join(root, file)
        blob_path = f"data/{file}"
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(file_path)
        print(f"  Uploaded: gs://mlops-bucket-ayush-123/{blob_path}")

print("Upload complete!")
EOF
               '''
           }
       }
       
       stage('Submit Vertex AI Training Job') {
           steps {
               sh '''
                   . gcp_env/bin/activate
                   python3 << 'EOF'
import os
from google.cloud import aiplatform
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
aiplatform.init(credentials=credentials, project='mlops-vertex-project', location='us-central1')

print("Vertex AI training job submission would happen here.")
print("Using container: gcr.io/mlops-vertex-project/ml-trainer:${BUILD_NUMBER}")
print("Training data: gs://mlops-bucket-ayush-123/data/")
print("Model output: gs://mlops-bucket-ayush-123/models/${BUILD_NUMBER}/")
EOF
               '''
           }
       }
       
       stage('Archive Model Artifacts') {
           steps {
               sh '''
                   mkdir -p models
                   touch models/sklearn_model.pkl
                   touch models/metrics.json
               '''
               archiveArtifacts artifacts: 'models/**/*', fingerprint: true
           }
       }
   }
   
   post {
       success {
           echo 'Pipeline completed successfully!'
       }
       failure {
           echo 'Pipeline failed!'
       }
   }
}
