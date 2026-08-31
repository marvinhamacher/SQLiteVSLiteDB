import json
import os
from datetime import datetime


class ReportService:

    def __init__(self, hardware_config, user, output_dir="results"):
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

        date = datetime.now().strftime("%Y-%m-%d")
        cpu = self._sanitize_filename(
            hardware_config["cpu"]["processor"]
        )


        self.filename = (
            f"result_{date}_{cpu}_{user}.json"
        )

        self.filepath = os.path.join(
            self.output_dir,
            self.filename
        )

        self.report = {
            "hardware": hardware_config,
            "results": []
        }

        self._write()

    def append_results(
        self,
        exec_time,
        results,
        iteration_nr
    ):
        self.report["results"].append({
            "iteration": iteration_nr,
            "exec_time": exec_time,
            "results": results
        })

        self._write()


    def _write(self):
        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.report,
                file,
                indent=4,
                ensure_ascii=False
            )


    @staticmethod
    def _sanitize_filename(value):
        invalid_chars = '<>:"/\\|?*'

        for char in invalid_chars:
            value = value.replace(char, "_")

        return value.strip()
