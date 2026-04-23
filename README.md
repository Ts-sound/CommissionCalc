# CommissionCalc

A Python-based performance commission calculation tool.

**Language**: [English](README.md) | [中文](README.zh.md)

## Features

- Text paste import for performance data (tab-separated format)
- Visual staff configuration management
- Configurable commission rules
- Automatic calculation of multiple commission types
- Detailed commission report export (Excel)
- Automatic repair of historical config data
- Detailed calculation logs for troubleshooting

## Commission Rules

### Personal Performance Commission
- 0-3000: 0%
- Above 3000: 20% (full amount)

### Team Performance Commission (Team Leader/Manager)
- Only accumulates qualified performance (>= threshold, default 3000)
- Includes leader/manager's own performance
- 0-10000: 0%
- 10000-50000: 10%
- Above 50000: 20% (full amount)
- Threshold configurable in rules

### Team Leader Management Commission
- Per member: 100 (member qualification not required)

### High Performance Bonus
- Non-cumulative, takes highest tier
- 20k: 500
- 30k: 1000
- 50k: 2000

## Technical Architecture

- **Language**: Python 3.8+
- **UI Framework**: Tkinter
- **Data Processing**: pandas + openpyxl
- **Config Storage**: JSON files
- **Testing**: pytest

### Layered Architecture

```
src/
├── models/        # Data models
├── services/      # Business logic
├── repositories/  # Data access
└── ui/            # User interface
```

## Installation

### Option 1: Virtual Environment (Recommended)

```powershell
# Auto-create environment and install dependencies
.\scripts\setup-venv.ps1

# Activate environment
.\.venv\Scripts\Activate.ps1

# Run program
python main.py
```

### Option 2: Global Install

```bash
pip install -r requirements.txt
python main.py
```

## Running

```bash
python main.py
```

## Packaging

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Package as single executable
pyinstaller -F -w -n "PerformanceCalc" main.py
```

Output: `dist\PerformanceCalc.exe`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Project Status

All features completed:
- ✅ Data models (Person, Group, CommissionRule, Config)
- ✅ Business logic (commission calculation)
- ✅ Data access (Excel import/export, config persistence)
- ✅ User interface (main window, staff management, rules config)
- ✅ Logging system
- ✅ Independent manager commission config (v0.3.0)
- ✅ Custom export order (v0.3.0)
- ✅ 60 unit tests, all passing

## License

MIT License