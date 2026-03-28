---
name: 'Development Environment Standards'
description: 'Project environment, build, dependency, and deployment conventions'
applyTo: "package.json,requirements.txt,Dockerfile,docker-compose.yml,Makefile,*.toml"
---

# Development Environment Standards

- Use lockfiles for reproducible builds (package-lock.json, poetry.lock, etc.)
- Never commit actual .env files — use .env.example as template
- Document all required environment variables in README
- Use migrations for all database schema changes
- Use structured logging with appropriate log levels
- Include health checks in containerized applications
- Ensure builds are reproducible across environments
