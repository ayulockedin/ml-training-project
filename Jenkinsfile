pipeline {
   agent any
   
   environment {
       GCP_PROJECT = 'REPLACE_WITH_YOUR_GCP_PROJECT_ID'
       GCP_REGION = 'us-central1'
       GCS_BUCKET = 'gs://REPLACE_WITH_YOUR_BUCKET_NAME'
       CONTAINER_REGISTRY = 'gcr.io/${GCP_PROJECT}'
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
       
       stage('Build Training Container') {
           steps {
               sh '''
                   gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                   gcloud config set project ${GCP_PROJECT}
                   gcloud auth configure-docker
                   
                   docker build -t ${CONTAINER_REGISTRY}/ml-trainer:${BUILD_NUMBER} .
                   docker push ${CONTAINER_REGISTRY}/ml-trainer:${BUILD_NUMBER}
               '''
           }
       }
       
       stage('Upload Training Data') {
           steps {
               sh '''
                   gsutil cp -r data/ ${GCS_BUCKET}/data/
               '''
           }
       }
       
       stage('Submit Vertex AI Training Job') {
           steps {
               sh '''
                   pip install google-cloud-aiplatform
                   
                   python vertex_training.py \
                       --project-id ${GCP_PROJECT} \
                       --region ${GCP_REGION} \
                       --display-name ${JOB_NAME}-${BUILD_NUMBER} \
                       --container-uri ${CONTAINER_REGISTRY}/ml-trainer:${BUILD_NUMBER} \
                       --model-dir ${GCS_BUCKET}/models/${BUILD_NUMBER}/ \
                       --training-data ${GCS_BUCKET}/data/
               '''
           }
       }
       
       stage('Download Model Artifacts') {
           steps {
               sh '''
                   gsutil cp -r ${GCS_BUCKET}/models/${BUILD_NUMBER}/ ./models/
               '''
               archiveArtifacts artifacts: 'models/**/*', fingerprint: true
           }
       }
   }
   
   post {
       success {
           echo 'Vertex AI training completed successfully!'
       }
       failure {
           echo 'Training job failed!'
       }
   }
}
