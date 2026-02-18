# Humans vs Machine (Telemetry-Driven Strategy Game)
## Description
A turn-based Human versus Machine strategy game played on a gird. The game integrates telemetry to capture player behaviour, decision patterns and performance metrics. The collected data can be used to refine mechanics, improve fairness and optimise game design decisions

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
