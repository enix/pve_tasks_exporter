# Prometheus Proxmox VE Tasks Exporter

This exporter provide Prometheus metrics (Counter) for PVE tasks.  
It's inspired by [Prometheus Proxmox VE Exporter](https://github.com/prometheus-pve/prometheus-pve-exporter), but with results kept in memory between each loop turn to increment tasks counters.

Usage is similar to prometheus-pve-exporter (it use the same configuration).

## Generate self-contained binary

```bash
pip install shiv
shiv -p /usr/bin/python3 -c pve_tasks_exporter -o pve_tasks_exporter .
```
