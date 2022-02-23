import collections
import time

import proxmoxer


def get_node_tasks(pve):
    """
    Retrieve the lisr of tasks for each node
    """
    return {
        node["node"]: pve.nodes(node["node"]).tasks.get(source="archive", limit=200)
        for node in pve.nodes.get()
    }


def get_new_tasks(tasks, last_run_timestamp):
    """
    Return the list of new tasks per node since the last run
    """
    return {
        node: [task for task in tasks[node] if task["starttime"] > last_run_timestamp]
        for node in tasks
    }


def update_tasks_counters(tasks):
    counters = {node: {} for node in tasks}
    for node in tasks:
        counters[node] = {
            "tasks": collections.Counter(task["type"] for task in tasks[node]),
            "tasks_error": collections.Counter(
                [task["type"] for task in tasks[node] if task.get("status") != "OK"]
            ),
        }
    return counters


def update_metrics(counters, metrics):
    for key in metrics:
        for node in counters:
            for task_type, value in counters[node].get(key).items():
                metrics[key].labels(type=task_type, node=node).inc(value)


def main_loop(metrics, config, args):
    last_run_timestamp = int(time.time())
    # FIXME? May need to move in the loop for token renew
    pve = proxmoxer.ProxmoxAPI(args.target, **config["default"])

    while True:
        tmp_last_run_timestamp = int(time.time())
        tasks = get_new_tasks(get_node_tasks(pve), last_run_timestamp)
        last_run_timestamp = tmp_last_run_timestamp
        counters = update_tasks_counters(tasks)
        update_metrics(counters, metrics)
        time.sleep(args.interval)
