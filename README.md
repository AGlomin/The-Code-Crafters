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
<pre>
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
├── LevelEditor.py
├── LevelSelector.py
├── LICENSE
├── logintest.py
├── mainGame.py
├── README.md
├── report.txt
├── auth.py
├── users.csv
├── test_level_h.py
└── UI.py
</pre>
# Deployment Guide
This guide explains how to set up the environment, run tests, generate telemetry, and launch the dashboard from a fresh clone.

## System Requirements
- Python 3.12
- Conda (recommended)

## Clone the Repository
1. git clone https://github.com/AGlomin/The-Code-Crafters.git

2. cd The-Code-Crafters

## Environment Setup
Create and activate the environment:

1. conda create -n codecrafters python=3.12 -y

2. conda activate codecrafters

Upgrade pip:
python -m pip install --upgrade pip

Install dependencies:
python -m pip install pytest pygame pandas matplotlib

## How to Run Tests
Run all tests:
pytest

Or in quiet mode:

pytest -q

(All 33 tests should pass. No failures should appear)


## User Interface Launching and User Capabilities

The user interface is launched through the main login screen, which controls access to features based on the type of user. After logging in, users are directed to a menu showing only the functions available to their role.

### Launching the User Interface
Run the interface with:

python UI.py

After login, selecting **Play Game** takes the user to the **Level Selector** screen.

### User Types and Capabilities

The system has four users in total:
- 2 Players
- 1 Designer
- 1 Maintainer

### Login Credentials

| User Type  |   Username  |   Password  |
|------------|-------------|-------------|
| Player 1   | player1     | pass123     |
| Player 2   | player2     | pass234     |
| Designer   | designer1   | design123   |
| Maintainer | maintainer1 | maintain123 |

#### Player Accounts
Player users are restricted to gameplay only. They can:
- Log in
- Access Play Game
- Open the Level Selector
- Play unlocked levels only

Players cannot access:
- Analytics dashboard
- Balancing toolkit

#### Designer Account
The Designer has access to all major system tools. They can:
- Play the game
- Access the analytics dashboard
- Access the balancing toolkit

#### Maintainer Account
The Maintainer also has full system access. They can:
- Play the game
- Access the analytics dashboard
- Access the balancing toolkit

### Level Progression and Unlocking
When a user selects Play Game, they are taken to the Level Selector.

The Level Selector uses a progression-based unlock system:
- The first level is available from the start
- Later levels remain locked until earlier levels are completed
- A player must complete Level 1 before Level 2 becomes available
- This continues for subsequent levels

This progression system ensures structured gameplay and allows telemetry to track how players progress through stages over time.

### Summary of Access Rights

| User Type  | Play Game | Dashboard | Balancing Toolkit |
|------------|-----------|-----------|-------------------|
| Player 1   | Yes       | No        | No                |
| Player 2   | Yes       | No        | No                |
| Designer   | Yes       | Yes       | Yes               |
| Maintainer | Yes       | Yes       | Yes               |

### To confirm Telemetery capture
Gameplay events are automatically written to telemetry/telemetry.csv

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
python -m pip install pytest pygame pandas matplotlib

If tests fail, ensure the environment is activated before running pytest.
