# ML/MLOps Task 0 - Anything.ai

##    Local Run
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

##     Docker Run
docker build -t mlops-task .
docker run --rm mlops-task

##    Files
- run.py : Main script
- config.yaml : Config file
- data.csv : Dataset
- requirements.txt : Python packages
- Dockerfile : Container instructions
- metrics.json : Output metrics
- run.log : Job logs



##      Sample metrics.json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.499,
    "latency_ms": 120,
    "seed": 42,
    "status": "success"
}