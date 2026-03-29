---
description: "Global security rules — mandatory for all Agents. Covers auth, data handling, file management, logging, and security mindset."
---

# 🛡️ Global Security Rules

> **MANDATORY.** Every Agent must follow these rules in all tasks. No exceptions.

## 1. Authentication & Authorization
- **NEVER** hardcode passwords, API keys, or tokens in source code.
- Use environment variables (`ENV`) or Secret Manager.
- Always check authorization at API endpoints.

## 2. Data Handling
- **Input Validation**: Always validate input (type, length, whitelist patterns).
- **Output Sanitization**: Escape data before rendering in UI (prevent XSS).
- **HTTPS Only**: Use HTTPS for all connections.

## 3. File Management
- Always validate filenames and extensions on upload.
- Block Path Traversal — never use raw user input in file system paths.

## 4. Logging & Error Handling
- Never log sensitive data (credit cards, passwords, full PII).
- Disable debug/verbose errors in production environments.

## 5. Security Mindset
- For every coding task, ask: "Does this code create a security vulnerability?"
- If task involves security → **MUST** activate `security-agent` for review.

## Triggers
Auto-activates on: session start (loaded as global skill for all Agents).
