import subprocess
import json
import mlflow
import os

mlflow.set_tracking_uri("mlruns")
mlflow.set_experiment("BERTopic Experiment")

run_name = "bertopic_run"

with mlflow.start_run(run_name=run_name):
    mlflow.log_param("run_file", "train_topic_model.py")
    
    result = subprocess.run(["python", "-m", "training.train_topic_model"], capture_output=True, text=True)
    
    print("=== STDOUT ===")
    print(result.stdout)
    print("=== STDERR ===")
    print(result.stderr)

    if os.path.exists("results.json") and os.path.getsize("results.json") > 0:
        with open("results.json") as f:
            results = json.load(f)
        
        mlflow.log_metric("coherence_score", results["coherence_score"])
        mlflow.log_param("docs_size", results["docs_size"])

        with open("topics.json", "w") as f:
            json.dump(results["topics"], f, indent=2)
        mlflow.log_artifact("topics.json")
    else:
        raise Exception("results.json tidak ditemukan atau kosong!")
