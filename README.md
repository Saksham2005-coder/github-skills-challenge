# AIOps Assessment

## AIOps Scenario
The service being monitored is a simple application platform that exposes operational metrics such as request latency, CPU usage, memory usage, and log events. The goal is to detect when the service behaves abnormally and convert those signals into actionable anomaly events for operations teams.

## Operational Problem
The application may experience slow response times, high resource usage, or error-related log events that indicate degraded service health. Without automated detection, these issues can be missed until users report failures or performance drops become severe.

## Why AIOps is Useful
AIOps helps by automatically analysing telemetry, recognising abnormal behaviour, and turning detected issues into structured events that can be routed to monitoring and operational workflows. In this assessment, AIOps is used to connect operational data, anomaly detection, event publication, and downstream processing in a simplified simulation.

## Operational Data Description
The project provides synthetic service data containing:
- timestamp
- service name
- response_time_ms
- cpu_percent
- memory_percent
- log_level
- message

These fields represent both metrics and operational logs. Metrics are the numeric values such as response time, CPU, and memory. Log information is represented by log_level and message.

## Observations
Normal behaviour includes:
- low response times
- normal CPU and memory values
- INFO-level logs

Unusual behaviour includes:
- unusually high response times
- CPU or memory spikes
- WARNING or ERROR log activity that suggests service degradation

## Anomaly Detection Findings
The anomaly detector evaluates each record against thresholds for response time, CPU usage, and memory usage. Any record exceeding those thresholds is flagged as abnormal. Relevant log events are also considered when assessing the severity of the problem.

## Event Processing Flow
Operational data -> anomaly detection -> event generation -> producer -> topic -> consumer -> AIOps output

## Final Workflow Result
The final pipeline processes service records, identifies anomalous observations, creates anomaly events, publishes those events, consumes them from the topic, and produces a downstream operational result representing the detected issue.

## Issues Identified and Corrected
The workflow originally had issues in the import path and event flow logic. These were corrected so the project could run consistently and the AIOps event chain could complete successfully.

## Limitation
The current detection logic uses fixed thresholds rather than learned baselines, so it may not adapt well to changing service behaviour over time.

## Reproduction Steps
1. Create and activate a virtual environment.
2. Install dependencies from requirements.txt.
3. Run the test suite with coverage.
4. Execute the AIOps pipeline.
5. Confirm that anomaly events are generated and processed correctly.
