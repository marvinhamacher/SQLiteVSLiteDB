import subprocess

import psutil
import platform
class EnvironmentService:
    def get_ram_frequency(self):
        if platform.system() != "Windows":
            return None

        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_PhysicalMemory | "
                    "Measure-Object -Property ConfiguredClockSpeed -Maximum).Maximum"
                ],
                capture_output=True,
                text=True,
                timeout=5
            )

            return int(result.stdout.strip())

        except (ValueError, subprocess.SubprocessError, OSError):
            return None

    def gather_system_information(self):
        cpu_freq = psutil.cpu_freq()

        return {
            "system": {
                "architecture": platform.machine()
            },

            "cpu": {
                "processor": platform.processor(),
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "frequency_mhz": {
                    "max": round(cpu_freq.max, 2) if cpu_freq else None,
                    "min": round(cpu_freq.min, 2) if cpu_freq else None
                }
            },

            "ram": {
                "size_gb": round(
                    psutil.virtual_memory().total / (1024 ** 3),
                    2
                ),
                "frequency_mhz": self.get_ram_frequency()
            }
        }

    def verify_configuration(self):
        sys = platform.platform()
        pyver = platform.python_version()
        if ("Windows-11" not in sys) or ('3.14' not in pyver):
            raise EnvironmentError("System muss auf Windows 11 basieren und Python 3.14 verwenden")