# sysadmin-automation-library

A modular Python toolkit for Linux systems administration, automating host intrusion detection, system metric logging, and real-time webhook alerting pipelines.

# Linux Systems Automation & Monitoring Library

A modular suite of lightweight, production-ready Python utilities designed for automated host-level security auditing, infrastructure resource monitoring, and network verification. 

This repository documents my engineering transition from hardware reliability operations into infrastructure automation and software development.

---

## 🛠️ Repository Architecture

The toolkit is organized into specialized domain modules to mirror professional production environments:

```text
sysadmin-automation-library/
├── security/         # Host protection, authentication parsing, and identity whitelisting
├── monitoring/       # System telemetry, storage thresholds, and metric logging
└── networking/       # Endpoint connectivity checks and data format validation

🚀 Module Deep Dive
🛡️ Security & Identity Auditing (/security)
server_audit.py (Automated Host Intrusion Alerting): Streams active identity state changes by parsing /etc/passwd. Implements automated system-account filtering logic and hooks into Discord Webhook APIs to instantly trigger real-time host intrusion alerts if an unapproved user bypasses access management profiles.

log_reporter.py (Secure Authentication Log Pipeline): Ingests, processes, and structures raw system logs (/var/log/auth.log) to identify, track, and aggregate brute-force access attempts, outputting parsed results into isolated analytical datasets (failed_logins.csv).

ssh_audit.py & db_security_filter.py: Hardened auditing scripts designed to parse active access endpoints and filter structural configuration inputs using strict security sanitization patterns to block injection attempts.

💾 Infrastructure & Resource Telemetry (/monitoring)
system_health_report.py & disk_space_monitor.py: Leverages native OS tracking engines (shutil, psutil) to calculate partition allocations, memory states, and resource fatigue. Utilizes structured float-formatting to stream clean system warnings directly to communications channels when hardware thresholds cross safety bounds.

uptime_calculator.py: Tracks and exposes host availability profiles, aggregating runtime data into clean administrative metrics.

🌐 Network Utilities (/networking)
network_traffic_router.py & regional_server_check.py: Advanced mock mapping tools designed to evaluate multi-region platform accessibility, simulate simple traffic profiles, and verify global network endpoints.

ping_status_counter.py & ip_validator.py: Infrastructure utilities to validate system availability across target clusters, handle string validation, and verify structural data formatting for strict IPv4/IPv6 compliance.

⏰ Deployment & Production Automation
These utilities are optimized for low-overhead execution and designed to run natively via system schedulers (cron) without heavy third-party dependencies.

Production Cron Profile Example:

# Execute the resource and identity audit script every hour on the hour
0 * * * * /usr/bin/python3 /home/atlas-01/sysadmin-automation-library/security/server_audit.py

# Run the authentication intrusion log pipeline daily at midnight
0 0 * * * /usr/bin/python3 /home/atlas-01/sysadmin-automation-library/security/log_reporter.py

⚙️ Core Technical Highlights
Decoupled Secret Management: Leverages .env isolation to entirely abstract structural webhooks and sensitive server data from core execution blocks.

Zero-Overhead Parsing Engines: Written using robust Python native string operations, skipping bloated libraries to maintain lightweight host execution profiles.

Clean Stream Parsing: Built to intelligently account for empty trailing strings and system data edge cases to avoid runtime indexing failures.
