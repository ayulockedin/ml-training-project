#!/usr/bin/env python3
"""Vertex AI Training Job Submission Script"""

from google.cloud import aiplatform
import argparse
import os

def submit_training_job(
    project_id: str,
    region: str,
    display_name: str,
    container_uri: str,
    model_dir: str,
    training_data: str
):
    """Submit a custom training job to Vertex AI"""
    
    aiplatform.init(project=project_id, location=region)
    
    job = aiplatform.CustomContainerTrainingJob(
        display_name=display_name,
        container_uri=container_uri,
    )
    
    model = job.run(
        model_display_name=f'{display_name}-model',
        args=[
            f'--data-path={training_data}',
            f'--model-dir={model_dir}',
        ],
        replica_count=1,
        machine_type='n1-standard-4',
        accelerator_type='NVIDIA_TESLA_T4',
        accelerator_count=1,
    )
    
    print(f"Training job completed: {job.resource_name}")
    print(f"Model created: {model.resource_name}")
    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', required=True)
    parser.add_argument('--region', default='us-central1')
    parser.add_argument('--display-name', required=True)
    parser.add_argument('--container-uri', required=True)
    parser.add_argument('--model-dir', required=True)
    parser.add_argument('--training-data', required=True)
    args = parser.parse_args()
    
    submit_training_job(
        args.project_id, args.region, args.display_name,
        args.container_uri, args.model_dir, args.training_data
    )
