# Linux Systems Automation & Monitoring Library

A modular suite of lightweight, production-ready Python utilities designed for automated host-level security auditing, infrastructure resource monitoring, and network verification.

*This repository documents my engineering transition from hardware reliability operations into infrastructure automation and software development.*

---

## 🛠️ Repository Architecture

The toolkit is organized into specialized domain modules to mirror professional production environments:

```text
sysadmin-automation-library/
├── .gitignore         # Prevents local credentials and caches from being tracked
├── .env.example       # Template for required environment variables
├── README.md          # Project documentation
├── provisioning/      # User creation, bulk onboarding, and interactive CLI tooling
├── security/          # Host protection, authentication parsing, and identity whitelisting
├── monitoring/        # System telemetry, storage thresholds, and metric logging
└── networking/        # Endpoint connectivity checks and data format validation

🚀 Module Deep Dive

👤 User Provisioning & Onboarding (/provisioning)

interactive_provisioner.py (CLI Onboarding Wizard): Guides administrators step-by-step through capturing individual new hire details (first name, last name, department), automatically generates company emails, sets up user accounts, assigns system groups, configures default credentials, and handles home directory creation with robust logging fallback.

provision_users.py (Bulk CSV Ingestion Tool): Processes structured spreadsheet data to rapidly automate the batch creation of multiple user accounts, system groups, and permissions in a single execution run.

🛡️ Security & Identity Auditing (/security)
server_audit.py (Automated Host Intrusion Alerting): Streams active identity state changes by parsing /etc/passwd. Implements automated system-account filtering logic and hooks into Discord Webhook APIs to instantly trigger real-time host intrusion alerts if an unapproved user bypasses access management profiles.

auth_log_summarizer.py (Authentication Event Aggregator): Parses system authentication logs to extract, categorize, and count event frequencies by process and message type, turning raw log data into clean, structured summaries for fast security auditing.

log_reporter.py (Secure Authentication Log Pipeline): Ingests, processes, and structures raw system logs (/var/log/auth.log) to identify, track, and aggregate brute-force access attempts, outputting parsed results into isolated analytical datasets (failed_logins.csv).

ssh_audit.py & db_security_filter.py: Hardened auditing scripts designed to parse active access endpoints and filter structural configuration inputs using strict security sanitization patterns to block injection attempts.

💾 Infrastructure & Resource Telemetry (/monitoring)
system_health_report.py & disk_space_monitor.py: Leverages native OS tracking engines (shutil, psutil) to calculate partition allocations, memory states, and resource fatigue. Utilizes structured float-formatting to stream clean system warnings directly to communications channels when hardware thresholds cross safety bounds.

disk_sentinel.py (Resource Health & Automated Cleanup Sentinel): Monitors root partition utilization and evaluates target log ages using native OS path and time modules. Safely logs and purges stale operational files when storage thresholds cross critical bounds, utilizing robust try-except error handling for low-overhead production maintenance.

uptime_calculator.py: Tracks and exposes host availability profiles, aggregating runtime data into clean administrative metrics.

disk_sentinel.py: Monitors root partition capacity and safely queues inactive logs for cleanup when free space drops below 20%.

bind_serial_rotator.py: Automates the incrementing and updating of BIND DNS zone file serial numbers (`YYYYMMDDnn format`) to streamline domain configuration changes and ensure proper version propagation.

🌐 Network Utilities (/networking)
network_traffic_router.py & regional_server_check.py: Advanced mock mapping tools designed to evaluate multi-region platform accessibility, simulate simple traffic profiles, and verify global network endpoints.

ping_status_counter.py & ip_validator.py: Infrastructure utilities to validate system availability across target clusters, handle string validation, and verify structural data formatting for strict IPv4/IPv6 compliance.

⚙️ Core Technical Highlights
Decoupled Secret Management: Leverages .env isolation via python-dotenv to entirely abstract structural webhooks and sensitive server data from core execution blocks.

Zero-Overhead Parsing Engines: Written using robust Python native string operations, skipping bloated libraries to maintain lightweight host execution profiles.

Clean Stream Parsing: Built to intelligently account for empty trailing strings and system data edge cases to avoid runtime indexing failures.

🛠️ Setup & Installation
1. Environment Configuration
To run scripts that send Discord alerts (like server_audit.py), you must define your webhook URL locally.

Create a .env file in the root directory:

Bash
nano ~/sysadmin-automation-library/.env
Add your credentials:

Ini, TOML
DISCORD_WEBHOOK_URL="[https://discord.com/api/webhooks/your-actual-webhook-id](https://discord.com/api/webhooks/your-actual-webhook-id)"
(Note: Your local .gitignore is already configured to keep this file out of your public commits).

2. Install Dependencies
While the toolkit relies heavily on the Python Standard Library, resource telemetry utilizes psutil for host hardware state parsing:

Bash
pip install psutil python-dotenv
⏰ Deployment & Production Automation
These utilities are optimized for low-overhead execution and designed to run natively via system schedulers (cron) without heavy third-party dependencies.

Production Cron Profile Example:
To configure these scripts to run automatically, run crontab -e and add your schedule entries:

Plaintext
# Execute the resource and identity audit script every hour on the hour
0 * * * * /usr/bin/python3 /home/atlas-01/sysadmin-automation-library/security/server_audit.py

# Run the authentication intrusion log pipeline daily at midnight
0 0 * * * /usr/bin/python3 /home/atlas-01/sysadmin-automation-library/security/log_reporter.py

---

### Part 2: Terminal Commands to Deploy It

Once you have copied the Markdown block above, run these commands step-by-step in your terminal to save and publish your new profile:

1. **Open the readme in nano:**
   ```bash
   nano ~/sysadmin-automation-library/README.md
