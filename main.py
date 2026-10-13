import subprocess
import time
import re
from typing import Optional

class MacBatteryController:
    """
    A controller to manage MacBook battery charging via the 'batt' CLI tool.
    Requires 'batt' to be installed via Homebrew.
    """
    def __init__(self, batt_path: str = "/opt/homebrew/bin/batt"):
        # Default path for Homebrew installations on Apple Silicon
        self.batt_cmd = batt_path

    def get_battery_level(self) -> Optional[int]:
        """Retrieve the current battery percentage using the 'pmset' system command."""
        try:
            # Capture standard output and error
            output = subprocess.check_output(
                ["pmset", "-g", "batt"], 
                stderr=subprocess.STDOUT
            ).decode("utf-8")
            
            match = re.search(r'(\d+)%', output)
            if match:
                return int(match.group(1))
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute pmset: {e.output.decode('utf-8').strip()}")
        except Exception as e:
            print(f"Failed to read battery level: {e}")
        return None

    def force_discharge(self) -> None:
        """Disable external AC power and force the system to use battery power."""
        print("\n🔌 Triggered: Disconnecting external power, switching to battery...")
        subprocess.run(["sudo", self.batt_cmd, "adapter", "disable"], check=False)

    def restore_adapter(self) -> None:
        """Enable external AC power."""
        print("\n🔌 Triggered: Restoring external AC power...")
        subprocess.run(["sudo", self.batt_cmd, "adapter", "enable"], check=False)

    def prevent_sleep_clamshell(self) -> None:
        """Prevent the Mac from sleeping when external power is cut in clamshell mode."""
        print("\n🛡️ Enabling sleep prevention for clamshell mode...")
        subprocess.run(["sudo", self.batt_cmd, "prevent-sleep-on-adapter-disable", "enable"], check=False)

def main():
    controller = MacBatteryController()
    
    # ⚠️ Uncomment the line below if you are using your Mac in Clamshell mode 
    # (lid closed with an external monitor). Cutting power normally forces sleep.
    # controller.prevent_sleep_clamshell()

    # Set your target charging limits
    UPPER_LIMIT = 99
    LOWER_LIMIT = 5
    CHECK_INTERVAL_SECONDS = 60

    print(f"🚀 Starting custom battery monitoring (Target range: {LOWER_LIMIT}% - {UPPER_LIMIT}%)")
    print("💡 Tip: Press Ctrl+C to stop monitoring and restore default power settings.\n")

    try:
        while True:
            level = controller.get_battery_level()
            if level is not None:
                # The \r keeps the output on the same line to prevent terminal spam
                print(f"🔋 Current battery level: {level}%", end="\r", flush=True)
                
                # Execute charging logic
                if level >= UPPER_LIMIT:
                    controller.force_discharge()
                elif level <= LOWER_LIMIT:
                    controller.restore_adapter()
            
            # Pause before checking again
            time.sleep(CHECK_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped manually. Restoring default power settings...")
        controller.restore_adapter()
        print("✅ Power settings restored.")

if __name__ == "__main__":
    main()
