# TradeHub MT5 Sync Agent

This folder contains the local Windows sync agent for TradeHub.

The Streamlit Cloud app cannot directly read your MT5 terminal, so this agent must run on the same Windows computer where MT5 is installed and logged in.

## Setup

1. Install Python on Windows.
2. Open Command Prompt inside the TradeHub project.
3. Install sync requirements:

```bash
pip install -r sync/requirements.txt
