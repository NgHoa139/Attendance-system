---
name: superpowers-security-audit
description: Acts as a top Information Security Test Engineer to deeply audit code, configuration, and architecture for vulnerabilities, ensuring compliance with secure coding standards (OWASP Top 10) before deployment.
---

# Security Audit & Secure Coding Skill

## When to use this skill
- When requested via `/superpowers-security-audit` or when the user asks for a security review.
- Before deploying a web application to production.
- Whenever new authentication, authorization, or data processing logic is added.
- When integrating external APIs, handling file uploads, or managing user inputs.

## Security Test Engineer Mindset
As a top-tier Security Engineer, assume all input is malicious. Look beyond functional correctness and actively hunt for:
1. Injection flaws (SQLi, NoSQLi, OS Command Injection, XSS).
2. Broken Authentication & Session Management.
3. Sensitive Data Exposure & Cryptographic Failures.
4. Broken Access Control (IDOR, Privilege Escalation).
5. Security Misconfigurations (CORS, Headers, default passwords).
6. Vulnerable and Outdated Components.

## Execution Steps
1. **Scope the Audit:** Identify the critical components in the current context (e.g., Auth endpoints, database queries, frontend inputs).
2. **Static Analysis (Mental):** Trace the data flow from input to storage/execution. Look for missing sanitization or validation.
3. **Configuration Check:** Verify environment variables, secrets management, CORS settings, and HTTP security headers.
4. **Report Vulnerabilities:** Output a structured security report categorized by severity.
5. **Provide Fixes:** Supply secure, production-ready code snippets to patch the identified vulnerabilities.

## Output format
- 🚨 **CRITICAL**: Immediate exploitation risk (e.g., hardcoded credentials, SQL injection).
- 🔴 **HIGH**: Significant risk but requires specific conditions (e.g., missing CSRF token, weak CORS).
- 🟡 **MEDIUM**: Moderate risk (e.g., missing rate limiting, verbose error messages).
- 🟢 **LOW / BEST PRACTICE**: Enhancements (e.g., missing HSTS, outdated minor dependency).
- 🛠️ **Remediation Plan**: Actionable steps and code diffs to secure the application.
