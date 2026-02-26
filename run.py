import argparse
import pandas as pd
import numpy as np
import yaml
import logging
import json
import time
import sys
import os

# Function to load configuration
def load_config(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    # Make sure required keys exist
    for key in ["seed", "window", "version"]:
        if key not in config:
            raise ValueError(f"Missing '{key}' in config")
    np.random.seed(config["seed"])  # Set random seed
    return config

# Function to load CSV data
def load_data(input_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} not found")
    df = pd.read_csv(input_file)
    if df.empty:
        raise ValueError("CSV is empty")
    if "close" not in df.columns:
        raise ValueError("Missing 'close' column")
    return df

# Function to compute rolling mean and signal
def compute_signal(df, window):
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    # Signal: 1 if close > rolling_mean else 0
    df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)
    return df

# Function to write metrics JSON
def write_metrics(output_file, version, rows, signal_rate, latency, seed, status="success", error=None):
    metrics = {"version": version, "status": status}
    if status == "success":
        metrics.update({
            "rows_processed": rows,
            "metric": "signal_rate",
            "value": float(signal_rate),
            "latency_ms": int(latency),
            "seed": seed
        })
    else:
        metrics["error_message"] = str(error)
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)
    print(json.dumps(metrics, indent=4))  # Print to console

# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    start = time.time()
    try:
        logging.info("Job started")
        config = load_config(args.config)
        logging.info(f"Config loaded: {config}")
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")
        df = compute_signal(df, config["window"])
        logging.info("Rolling mean and signal computed")
        latency = (time.time() - start) * 1000
        signal_rate = df["signal"].mean()
        write_metrics(args.output, config["version"], len(df), signal_rate, latency, config["seed"])
        logging.info("Job completed successfully")
    except Exception as e:
        latency = (time.time() - start) * 1000
        write_metrics(args.output, "v1", 0, 0, latency, 42, status="error", error=e)
        logging.error(f"Job failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()