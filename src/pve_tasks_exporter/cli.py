import argparse
import os

import prometheus_client
import yaml

from pve_tasks_exporter.collector import main_loop
from pve_tasks_exporter.config import config_from_env, config_from_yaml


def main():
    """
    Main entry point.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to configuration file (pve.yml)")
    parser.add_argument(
        "--target", default="127.0.0.1", help="PVE target to request API"
    )
    parser.add_argument(
        "--port", type=int, default=9222, help="Port on which the exporter is listening"
    )
    parser.add_argument(
        "--address", default="127.0.0.1", help="Address to which the exporter will bind"
    )
    parser.add_argument(
        "--interval", type=int, default=60, help="Interval to retrieve tasks from API"
    )
    args = parser.parse_args()

    # Load configuration.
    if "PVE_USER" in os.environ:
        config = config_from_env(os.environ)
    else:
        with open(args.config) as handle:
            config = config_from_yaml(yaml.safe_load(handle))

    if config.valid:
        prometheus_client.start_http_server(args.port, args.address)
    else:
        parser.error(str(config))

    metrics = {
        "tasks": prometheus_client.Counter(
            "pve_tasks", "Number of cluster tasks", ["type", "node"]
        ),
        "tasks_error": prometheus_client.Counter(
            "pve_tasks_error", "Number of cluster tasks in error", ["type", "node"]
        ),
    }

    main_loop(metrics, config, args)
