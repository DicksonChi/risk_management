#!/usr/bin/env bash

# run python static validation
prospector  --profile-path=. --profile=.prospector.yml --path=risk_management

# run bandit - A security linter from OpenStack Security
bandit -r risk_management
