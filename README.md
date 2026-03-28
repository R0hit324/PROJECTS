# Application-Data-Security-Assignment-
# README — Keylogger Red Team / Blue Team (Short)

**Status:** Educational lab — attacker actions performed only against an isolated test VM with instructor approval.

## Summary

Small red-team vs blue-team exercise: a harmless, controlled keylogger binary was used on an isolated target VM so defenders could detect, analyze, and respond using tools like `netstat` and static capability scanners.

## Objectives

* Practice safe lab setup and containment.
* Observe endpoint/network artifacts from a simulated compromise.
* Use forensic and static-analysis tools to detect and investigate suspicious activity.
* Produce a short incident timeline and remediation recommendations.

## Ethics & safety

Only run offensive code in isolated labs with written permission. No source code, commands, or reproduction steps are included here.

## Lab setup (high level)

* Two VMs: **Attacker** and **Target** on an isolated network. Use snapshots and no Internet access.
* Logging and monitoring enabled on the target for evidence collection.

## Attacker (what was simulated)

* Non-malicious keylogger that logged simulated keystrokes to local files and attempted benign exfiltration within the lab.
* Goal: create artifacts (files, processes, connections) for detection and analysis.

## Defender approach (high level)

* Monitor processes and network connections (e.g., via connection-listing tools).
* Perform static capability analysis on suspicious binaries (API usage, strings, imports).
* Triage, contain (isolate VM), collect artifacts, and extract IOCs.

## Analysis steps (concise)

1. Detect suspicious activity.
2. Triage: gather PID, parent, open sockets, timestamps.
3. Collect artifacts (hashes, logs) read-only.
4. Static analysis; dynamic sandboxed analysis if necessary.
5. Hunt using IOCs; remediate and document.

## Submission checklist

* Short executive summary
* Environment & isolation details
* Detection timeline and artifacts (sanitized)
* Analysis summary and remediation steps
* Ethics statement
