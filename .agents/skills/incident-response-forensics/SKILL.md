---
name: incident-response-forensics
description: Perform digital forensics during incident response — evidence preservation, volatile data collection, artifact analysis, and timeline construction. Use when investigating a suspected compromise.
---

# Incident Response Forensics

Collect and analyze evidence without destroying it.

## 1. Preserve Before You Poke

- Take memory capture first (before heavy processes): `WinPMem`, `LiME`, or vendor snapshot
- Disk image via write-blocker or verified cloud snapshot; hash everything (SHA-256), record chain of custody
- Collect network evidence: firewall/flow logs, PCAP if available, proxy and DNS logs
- **Never investigate on the live system beyond read-only collection** — attacker tooling notices

## 2. Volatile Data Order

1. Network connections, routing tables
2. Running processes and services, loaded modules
3. Logged-in sessions, clipboard (if interactive)
4. Command histories, scheduled tasks, autostart

## 3. Artifact Analysis

### Windows
- Shimcache/Amcache, Prefetch, SRUM for execution history
- Event logs: 4624/4625 (logons), 4688 (process creation), 7045 (service install), PowerShell 4104
- Registry: Run keys, Services, USN journal for file deletion
- Lateral movement: RDP logs (4776/4624 type 3), scheduled tasks, WMI activity

### Linux
- `/var/log/auth.log`, `journalctl`, `.bash_history`, wtmp/last
- Cron, systemd timers, `LD_PRELOAD` in /etc, immutable-bit anomalies
- Unauthorized SSH keys in authorized_keys, passwd modifications

### Cloud
- CloudTrail/data plane logs, unusual `AssumeRole` chains, new access keys
- Control-plane vs data-plane timeline separation

## 4. Timeline Construction

- Normalize all artifacts into a super-timeline (log2timeline/PlutoScope-style)
- Anchor on the initial access indicator, then walk forward (persistence, spread, exfil) and backward (recon, delivery)
- Separate facts from inference; mark confidence levels

## Output

- IOCs with context (hash, IP, domain, first/last seen)
- Attack narrative mapped to ATT&CK tactics with evidence citations per step
- Root-cause hypothesis with supporting and contradicting evidence
