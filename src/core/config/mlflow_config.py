import os
import mlflow

def setup_mlflow():
    mlflow.set_tracking_uri(
        "https://dagshub.com/Nikhil-MLOPs/Rag-System.mlflow"
    )
    mlflow.set_experiment("phase_3_chunking_experiments")