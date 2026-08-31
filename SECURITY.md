# Security Policy

## Supported Versions

Security fixes are applied to the latest commit on the default branch. Older
research snapshots and tags are not maintained as production software.

## Reporting a Vulnerability

Do not disclose credentials, command-injection paths, unsafe file-processing
cases, or other exploitable details in a public issue.

Use GitHub's private vulnerability reporting feature from the repository's
Security tab. Include the affected commit, reproduction steps, impact, and any
proposed mitigation.

If private vulnerability reporting is unavailable, contact the repository owner
through their GitHub profile without including exploit details in the first
message.

## Research-Software Scope

This repository processes CSV, XLSX, Draw.io, BibTeX, and LaTeX files. Only run
the analysis pipeline on trusted inputs, and review externally supplied files
before opening or compiling them.
