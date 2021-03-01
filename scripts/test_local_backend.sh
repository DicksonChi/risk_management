#!/usr/bin/env bash
# Note: when first run this script or migrations are updated, please remove the options --nomigrations and --reuse-db

py.test -n 2  --cov=risk_management --cov-report=html tests/
