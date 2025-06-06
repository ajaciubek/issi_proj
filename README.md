# Career Navigator
## Prequistes
1. Ubuntu 22.04 on WSL
2. python3.12
3. git
4. AWS CLI
5. uv

## Project configuration
In order to be able to run application config file (./config/.ml-env) has to be created.  
Following variables have to set:

CUDA_VISIBLE_DEVICES=""  
LABEL_MODEL_PATH="./data/role_label_encoder.pkl"  
JOB_PREDICT_MODEL_PATH="./data/job_model.keras"  
SENTENCE_TRANSFORMER_MODEL="all-MiniLM-L6-v2"  
GEMINI_KEY=<your api key>  

additional install of spacy model may be needed:

uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

## Starting application service:
1. uv sync
2. dvc pull
3. uv run uvicorn api.app:app

## Starting application UI:
1. cd frontend/my-app
2. npm install
3. npm run dev
