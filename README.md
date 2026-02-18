# Humans vs Machine (Telemetry-Driven Strategy Game)
## Description
A turn-based Human versus Machine strategy game played on a grid, integrating a structured telemetry logging system to capture player behaviour, decision patterns, and performance metrics. The project includes the game prototype, automated unit tests using pytest, and a Tkinter-based analytics dashboard. Telemetry events are written to a CSV file and analysed to generate progression funnel metrics and stage failure counts, enabling refinement of mechanics, improved fairness, and data-driven optimisation of game design decisions.

## Game Features
Turn-based movement system 

Grid-based combat 

Human VS Machine opponent 

Attack and Health system 

Stage progression 

Telemetry Logging of game play 

## REQUIRED MODULES
Pygame  

Pandas

Pytest

Tkinter 	

math

time

## Team Members
Aislin - Project Lead/Scrum Master

Ciara - Requirements and UX Lead

Faatimah - Technical Lead

James - Data and ML Lead

Nur - QA and Testing Lead

Malika - Documentation and Comms Lead

## Project Documentation
Scrum Board- https://docs.google.com/spreadsheets/d/1BoWglaC-3-RQQE-Y0ZF6Q08MyAXAGwlc6wPbj1PWNmk/edit?usp=sharing 

## File Structure
├── _pycache_/
│   ├── classes.cpython-312.pyc
│   └── LevelHandler.cpython-312.pyc
├── .venv/
├── assets/
├── dashboard/
│   └── test/
│   │   ├── _init_.py
│   │   ├── test_analytics.py
│   ├── _init_.py
│   ├── analytics.py
│   ├── cat
│   └── dashboard.py
└── levels/
│   ├── level0.txt
│   └── level1.txt
└── telemetry/
│   ├── _init_.py
│   └── telemetry.csv
└── Telemetry/
│   └── telemetry/
│   │   ├── _init_.py
│   │   ├── event_types.py
│   │   ├── events.py
│   │   ├── logger.py
│   │   ├── storage.py
│   │   └── validation.py
│   └── tests/
│   │   ├── _init_.py
│   │   ├── seed_data.py
│   │   ├── test_events.py
│   │   ├── test_funnel.py
│   │   ├── test_storage.py
│   │   └── test_validation.py
│   └── funnel.py
│   ├── mini_test.py
│   └── telemetry_scheme
├── agent_information.csv
├── classes.py
├── LevelHandler.py
├── logintest.py
├── mainGame.py
├── README.md
├── report.txt
└── UI.py

# Deployment Guide
This guide explains how to set up the environment, run tests, generate telemetry, and launch the dashboard from a fresh clone.

## System Requirements
- Python 3.12
- Conda (recommended)

## Clone the Repository
git clone: https://github.com/AGlomin/The-Code-Crafters.git
cd: The-Code-Crafters

## Environment Setup
Create and activate the environment:
conda create -n codecrafters python=3.12 -y
conda activate codecrafters

Upgrade pip:
python -m pip install --upgrade pip

Install dependencies:
python -m pip install pytest pygame pandas

## How to Run Tests
Run all tests:
pytest

Or in quiet mode:

pytest -q

(All 24 tests should pass. No failures should appear)

## Run the Game (Generate Telemetry)
Start the game:
python mainGame.py

(Gameplay events are automatically written to telemetry/telemetry.csv)

To confirm telemetry is being recorded:
tail -n 5 telemetry/telemetry.csv

(You should see recent event entries (e.g. stage_start, stage_complete, session_end))

## Run the Analytics Dashboard
Launch the dashboard:
python dashboard/dashboard.py

Click “Refresh Dashboard” to display progression funnel metrics and stage failure counts based on the telemetry file.

## Full Demo Workflow
Activate environment
conda activate codecrafters

Run tests
pytest

Run game
python mainGame.py

Confirm telemetry
tail -n 5 telemetry/telemetry.csv

Run dashboard
python dashboard/dashboard.py

Click “Refresh Dashboard”

## Common Issues
If a module is missing:
python -m pip install pytest pygame pandas

If tests fail, ensure the environment is activated before running pytest.
