# Carriere advisor
## Prequistes
1. Ubuntu 22.04 on WSL
2. python3.12
3. git
4. AWS CLI
5. uv

## Config file
In order to be able to run application config file (./config/.ml-env) has to be created.  
Following variables have to set:

CUDA_VISIBLE_DEVICES=""  
LABEL_MODEL_PATH="./data/role_label_encoder.pkl"  
JOB_PREDICT_MODEL_PATH="./data/job_model.keras"  
SENTENCE_TRANSFORMER_MODEL="all-MiniLM-L6-v2"  
GEMINI_KEY=<your api key>  

## Starting application service:
1. uv sync
2. dvc pull
3. uv run uvicorn api.app:app

## 
