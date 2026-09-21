Migration steps to Masonite 4
================================

This repository was originally implemented with FastAPI. Masonite 5 is not available on PyPI, so this project targets Masonite 4.20.4 as the supported framework for migration.

Prerequisites
- Python 3.11 or 3.12 (Python 3.13 has build issues with some Masonite dependencies)
- A virtual environment created using that Python version

Quick start (recommended)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

Generate Masonite project skeleton

Once Masonite is installed, you can scaffold a new Masonite project and then run the included converter to copy business logic from the original `app/` package into Masonite controllers.

```powershell
# create a new Masonite project (example name: masonite_project)
craft new masonite_project
cd masonite_project
# run converter from the repository root
..\scripts\convert_to_masonite.py
```

What the converter does
- Creates controller files mapping the existing insight endpoints to Masonite controller actions.
- Creates `routes/web.py` entries corresponding to the current FastAPI endpoints.

After scaffolding

```powershell
# run Masonite development server
craft serve
```

Notes
- If you prefer, I can perform the conversion inside this repo directly and move files into a `masonite_project/` folder — say the word and I'll proceed.
