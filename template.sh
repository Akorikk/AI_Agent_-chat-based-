#!/bin/bash

echo "Creating project structure..."

mkdir -p payment-agent/{agent,api,utils,tests,docs}

touch payment-agent/agent/__init__.py
touch payment-agent/agent/agent.py

touch payment-agent/api/__init__.py
touch payment-agent/api/client.py

touch payment-agent/utils/__init__.py
touch payment-agent/utils/validators.py
touch payment-agent/utils/state.py

touch payment-agent/tests/test_flows.py

touch payment-agent/run.py
touch payment-agent/requirements.txt
touch payment-agent/README.md
touch payment-agent/docs/design.md

echo "Structure created successfully!"