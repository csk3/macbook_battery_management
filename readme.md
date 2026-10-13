# MacBatteryController 🔋

A lightweight Python automation script that takes full control of your MacBook's charging and discharging behavior without requiring you to manually plug or unplug the power cable.

## 📖 The Story Behind This Project

I originally created this script because I needed to run automated battery cycle tests on my MacBook. I wanted to observe how the system and battery behaved during deep drain and recharge cycles, but constantly sitting by the laptop to manually plug and unplug the power cable was tedious and completely impractical. 

I needed a way to programmatically tell the MacBook to "stop taking power from the wall and use the battery" even while physically plugged in. By combining Python with the `batt` CLI tool, this script was born. It automates the entire process, monitoring the battery percentage and toggling the power supply based on your customized limits.

## ✨ Features

- **Automated Cycle Testing**: Run hands-free charge/discharge cycles (e.g., charge to 99%, drop to 5%, repeat).
- **Battery Health Preservation**: Keep your Mac plugged in all the time? Set the limits to 70%-80% to prevent battery degradation from overcharging (similar to tools like AlDente).
- **Clamshell Mode Support**: Built-in option to prevent the Mac from going to sleep when external power is cut while the lid is closed and an external monitor is connected.

## 🛠 Prerequisites

Before using this script, ensure you have the following installed on your macOS:
1. **Python 3.x**
2. **Homebrew** (macOS package manager)
3. **The `batt` CLI tool**: This script relies on the `batt` command-line utility to control the SMC (System Management Controller).

## 🚀 Installation

1. **Install the `batt` utility via Homebrew:**
```bash
# Note: Ensure you have the correct tap for the 'batt' tool you are using
brew tap charlie0129/batt
brew install batt
```

2. **Clone this repository:**
```bash
git clone https://github.com/YOUR_USERNAME/MacBatteryController.git
cd MacBatteryController
```

## ⚙️ Configuration & Usage

Open `mac_battery_controller.py` in your favorite text editor and customize the following variables in the `main()` function to fit your needs:

```python
# Set your target charging limits
UPPER_LIMIT = 99  # When to stop charging and switch to battery
LOWER_LIMIT = 5   # When to restore AC power and start charging
```

**Clamshell Mode:** 
If you are running this test while your MacBook lid is closed and connected to an external monitor, uncomment the following line in the script so your Mac doesn't go to sleep when the power is virtually disconnected:
```python
controller.prevent_sleep_clamshell()
```

### Running the Script

Because modifying power states requires administrator privileges, you must run the script with `sudo`:

```bash
sudo python3 mac_battery_controller.py
```

### Stopping the Script

To stop monitoring, simply press `Ctrl + C` in your terminal. 
The script will safely catch the keyboard interrupt, automatically restore your default external power settings, and exit gracefully.

## ⚠️ Disclaimer

This script manipulates hardware-level power states via the System Management Controller (SMC). While it uses established CLI tools to do so, use it at your own risk. The author is not responsible for any hardware damage or battery degradation.
