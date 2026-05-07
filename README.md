# Fibery ↔ HubSpot CRM Sync

Self-hosted n8n integration that keeps Fibery and HubSpot in sync over their REST APIs. Replaced a paid Zapier setup and several hours per week of manual data entry.

## What it does

- Two-way sync between Fibery records and HubSpot contacts/companies/deals
- 10,000+ contact dataset kept consistent across both systems
- Workflow-triggered email alerts when high-potential customers change state
- Runs on a self-hosted n8n instance (Docker)

## Why self-host

| | Zapier (before) | n8n self-hosted (after) |
|---|---|---|
| Monthly cost | ~$800 | ~$200 (VPS + email) |
| Trigger latency | seconds | seconds |
| Field-level mapping control | limited | full |
| Manual data entry | ~25 hr/wk | ~0 |

The cost savings come from removing per-task pricing — n8n charges for the host, not the operation count, so the marginal cost of an extra workflow is zero.

## Architecture

```
Fibery webhooks ─┐
                 ├─► n8n (self-hosted, Docker)
HubSpot webhooks ┘         │
                           ├─► Field mapping & deduplication
                           ├─► REST API calls (Fibery / HubSpot)
                           └─► SMTP alerts on flagged changes
```

Each integration is a separate n8n workflow with its own trigger, transformation, and write step. Workflows live in JSON exports so they version cleanly in git.

## Stack

- **Orchestration:** n8n (self-hosted, Docker)
- **APIs:** Fibery REST, HubSpot CRM v3
- **Auth:** API tokens stored as n8n credentials
- **Notifications:** SMTP

## Repo contents

- n8n workflow exports (`.json`)
- Field-mapping reference docs
- Sample API request/response payloads

## Note

This repository holds the workflow definitions and integration notes only. Live n8n instance, credentials, and customer data are not committed.
