# Linux Systems Automation & Monitoring Library

A modular suite of lightweight, production-ready Python utilities designed for automated host-level security auditing, infrastructure resource monitoring, network verification, and full-stack AI-augmented systems operations. This repository documents my engineering transition from hardware reliability operations into infrastructure automation and software development.

---

## 👁️ ARGUS Panoptes Core (Flagship AI Operations Platform)

Located within the `system-health-dashboard/` module, **ARGUS Panoptes Core** is a full-stack, AI-augmented systems administration control center deployed on AWS EC2. It bridges real-time host telemetry with Google's Gemini AI to deliver automated diagnostics, live resource tracking, and an interactive web-based terminal subsystem.

### 🏛️ Architectural Highlights & Capabilities:
- **The Panoptes Oracle (AI Copilot):** Powered by the `google-genai` SDK (`gemini-2.5-flash`) with automated system context injection. It dynamically reads live CPU, memory, and disk telemetry before evaluation, allowing the AI sentinel to provide context-aware troubleshooting insights.
- **Oculi Status (Live Telemetry Engine):** Real-time asynchronous polling of system resource usage, available memory headroom, and root partition archive depth utilizing `psutil`.
- **Command Subsystem (Web Terminal Link):** A secure backend `subprocess` execution layer that translates web UI commands into immediate system operations (e.g., `uptime`, `df -h`) with instant response rendering.
- **Infrastructure & Container Surveillance:** Built-in health check pipelines tracking active Linux `systemd` services (`argus-service`), background processes, and live container metrics.
- **Production Deployment Pattern:** Orchestrated natively via persistent Linux `systemd` services, environment variable isolation (`python-dotenv`), and Flask WSGI execution loops.

---

## 🛡️ Auth Sentinel (Automated Brute-Force Defense & Threat Pipeline)

Located within the `argus-ai/` module, **Auth Sentinel** is a robust automated host protection service that actively monitors system authentication attempts, defends against brute-force attacks, and maintains a zero-trust network perimeter.

### ⚙️ End-to-End Defensive Pipeline:
1. **Journald / Log Parsing:** Ingests and parses system authentication events (via `journalctl` or `/tmp/auth.log`), filtering failed SSH access attempts using robust regular expressions.
2. **SQLite Persistence Layer:** Automatically logs threat telemetry, timestamps, and offending IP addresses into a local SQLite database for historical tracking and repeat-offender validation.
3. **Automated Network Mitigation (`iptables`):** Evaluates failure counts against a pre-configured threat threshold and dynamically executes native kernel-level packet drops (`iptables-nft`) to block malicious IPs instantly on port 22.
4. **Discord Webhook Telemetry:** Fires real-time rich alerts straight to designated Discord channels the moment a threshold breach or firewall action occurs.
5. **Systemd Automation:** Configured as a background `oneshot` service tied to a 5-minute recurring systemd timer for 24/7 autonomous host protection.

---

## 🛠️ Repository Architecture

The toolkit is organized into specialized domain modules to mirror professional production environments:

sysadmin-automation-library/
├── .gitignore                      # Prevents local credentials and caches from being tracked
├── .env.example                    # Template for required environment variables (Gemini API, Webhooks)
├── README.md                       # Project documentation
├── provisioning/                   # User creation, bulk onboarding, and interactive CLI tooling
├── security/                       # Host protection, authentication parsing, and identity whitelisting
├── argus-ai/                       # Auth Sentinel security pipeline, SQLite storage, and core scripts
├── monitoring/                     # System telemetry, storage thresholds, and metric logging
├── networking/                     # Endpoint connectivity checks and data format validation
└── system-health-dashboard/        # Full-stack real-time web monitoring app & ARGUS Panoptes Core

---

## 🚀 Module Deep Dive

### 👤 User Provisioning & Onboarding (`/provisioning`)
- **`interactive_provisioner.py` (CLI Onboarding Wizard):** Guides administrators step-by-step through capturing individual new hire details, automatically generating company emails, setting up user accounts, assigning system groups, configuring default credentials, and handling home directory creation with robust logging fallback.
- **`provision_users.py` (Bulk CSV Ingestion Tool):** Processes structured spreadsheet data to rapidly automate the batch creation of multiple user accounts, system groups, and permissions in a single execution run.

### 🛡️ Security & Identity Auditing (`/security` & `/argus-ai`)
- **`auth_sentinel.py` (Automated SSH Brute-Force Defense):** Production security daemon that parses auth logs, tracks failed logins in SQLite, enforces automatic `iptables` kernel firewall drops, and dispatches real-time Discord webhook alerts.
- **`server_audit.py` (Automated Host Intrusion Alerting):** Streams active identity state changes by parsing `/etc/passwd`. Implements automated system-account filtering logic and hooks into Discord Webhook APIs to instantly trigger real-time host intrusion alerts if an unapproved user bypasses access management profiles.
- **`log_reporter.py` (Secure Authentication Log Pipeline):** Ingests, processes, and structures raw system logs to identify, track, and aggregate brute-force access attempts, outputting parsed results into isolated analytical datasets (`failed_logins.csv`).
- **`ssh_audit.py` & `db_security_filter.py`:** Hardened auditing scripts designed to parse active access endpoints and filter structural configuration inputs using strict security sanitization patterns to block injection attempts.

### 💾 Infrastructure & Resource Telemetry (`/monitoring` & `/system-health-dashboard`)
- **System Health Web Dashboard & ARGUS Core (`/system-health-dashboard`):** A full-stack web application built with Flask, `psutil`, and the Gemini API, featuring a responsive dark-themed cyberpunk UI with real-time dynamic telemetry, AI oracle responses, and terminal command execution. Deployed on AWS EC2 using Gunicorn as a production WSGI application server and Nginx as a reverse proxy.
- **`system_health_report.py` & `disk_space_monitor.py`:** Leverages native OS tracking engines (`shutil`, `psutil`) to calculate partition allocations, memory states, and resource fatigue. Utilizes structured float-formatting to stream clean system warnings directly to communications channels when hardware thresholds cross safety bounds.
- **`disk_sentinel.py` (Resource Health & Automated Cleanup Sentinel):** Monitors root partition utilization and evaluates target log ages using native OS path and time modules. Safely logs and purges stale operational files when storage thresholds cross critical bounds, utilizing robust try-except error handling for low-overhead production maintenance.
- **`uptime_calculator.py` & `bind_serial_rotator.py`:** Tracks host availability profiles and automates the incrementing/updating of BIND DNS zone file serial numbers (`YYYYMMDDnn` format) to streamline domain configuration changes.

### 🌐 Network Utilities (`/networking`)
- **`network_traffic_router.py` & `regional_server_check.py`:** Advanced mock mapping tools designed to evaluate multi-region platform accessibility, simulate simple traffic profiles, and verify global network endpoints.
- **`ping_status_counter.py` & `ip_validator.py`:** Infrastructure utilities to validate system availability across target clusters, handle string validation, and verify structural data formatting for strict IPv4/IPv6 compliance.

---

## ⚙️ Core Technical Highlights

- **Decoupled Secret Management:** Leverages `.env` isolation via `python-dotenv` to entirely abstract structural webhooks, Gemini API keys, and sensitive server data from core execution blocks.
- **Full-Stack Implementation:** Combines robust Python backend telemetry with lightweight asynchronous frontend polling and generative AI integration.
- **Zero-Overhead Parsing Engines:** Written using robust Python native string operations and optimized system calls to maintain lightweight host execution profiles.
- **Production-Grade Infrastructure:** Configured with Linux `systemd` services, Gunicorn multi-worker concurrency, and Nginx reverse proxy security blocks.

---

## 🛠️ Setup & Installation

### 1. Environment Configuration
To run scripts that send Discord alerts or query the Gemini AI oracle, define your environment variables.
- Create a `.env` file in your project root:
  `nano ~/sysadmin-automation-library/.env`
- Add your credentials:
  ```env
  GEMINI_API_KEY="your-gemini-api-key"
  DISCORD_WEBHOOK_URL="[https://discord.com/api/webhooks/your-actual-webhook-id](https://discord.com/api/webhooks/your-actual-webhook-id)"
