"""
Application configuration management.

This module centralizes environment configuration such as API keys,
model settings, and external service parameters. Configuration values
are loaded from environment variables to support local development,
Docker deployment, and CI environments.

Responsibilities:
- Load environment variables
- Provide typed configuration objects
- Prevent configuration logic from spreading across the codebase
"""

# Load configurations, env vaiables
# Dependency wiring