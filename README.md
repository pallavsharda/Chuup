# Chuup

TL;DR: A speech timer application that tracks speaking time using real-time audio detection.

Background: 

WHY: I wanted a personal tool that would help me practice the mantra of listening more and talking less. The aim of this app is to help me monitor my speaking time in online meetings- if I'm speaking continuously (based on a threshold), I'll know to pause and listen more. That's the basic idea.

HOW: The app uses the system microphone to detect audio (not as speech per se, just the sound waves above a certain threshold) in real-time. It then starts a cumulative timer. Once the timer reaches a pre-set threshold, the app will inform the user.

## Features
- Real-time audio detection (as a proxy for speech)
- Configurable time threshold
- Visual feedback
- Microphone calibration utility

## Setup
1. Install requirements
2. Run the app: `python main/gui.py`

## Version History
- v0.1: First working version with speech detection and GUI. Known issues:
    - The GUI is not very user-friendly.
    - The audio detection is not very accurate.
    - The app does not reset the time if user threshold is not crossed (i.e. the ideal use case is not implemented - where if the user has spoken for less than the threshold, then there is no issue, and the timer should reset).
