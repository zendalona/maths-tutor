
# math-tutor

this is the qt6Test branch


## Basic Components

- Cross platform gui
- 2 Themes, High contrast and Low contrast (currently look like light mode and dark mode)
- Add new lessons from file system
- Shift key to read question out loud
- Uses 'espeak' for windows and linux and 'say' for mac
- Basic gif changes for start, right answer, wrong answer and congratulations
- Default lesson is Addition (Easy)




## Installation
1. Clone project and navigate to project directory.

2. Create a python env and activate it

For Mac and Debian:-
```bash
  python3 -m venv qttutor
  cd qttutor
  source bin/activate

```
For Windows:-
```bash
  python3 -m venv qttutor
  cd qttutor
  qttutor\Scripts\activate

```
3. Install dependencies
```bash
  pip3 install PyQt6
```
4. Navigate to root directory of project and run
```bash
  python3 qt6main.py
```