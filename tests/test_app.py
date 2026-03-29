import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import menu
from cennik import get_membership_table_text
from funkcje import show_workout_schedule


class MembershipTableTests(unittest.TestCase):
    def test_membership_table_contains_expected_values(self):
        table_text = get_membership_table_text()

        self.assertIn("karnet", table_text)
        self.assertIn("Multisport", table_text)


class WorkoutScheduleTests(unittest.TestCase):
    def test_show_workout_schedule_handles_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_schedule = Path(temp_dir) / "grafik.csv"

            with patch("funkcje.SCHEDULE_FILE", missing_schedule):
                with patch("sys.stdout", new_callable=io.StringIO) as output:
                    show_workout_schedule()

        self.assertIn("Grafik nie jest jeszcze dostępny.", output.getvalue())


class MenuTests(unittest.TestCase):
    def test_menu_allows_exit(self):
        with patch("builtins.input", side_effect=["7"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                menu.main()

        self.assertIn("SIŁOWNIA ZASPANI", output.getvalue())
        self.assertIn("Kończymy na dziś", output.getvalue())

    def test_membership_option_displays_price_table(self):
        with patch("builtins.input", side_effect=["2", "1", "4", "7"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                menu.main()

        self.assertIn("rodzaj wejścia", output.getvalue())
        self.assertIn("Kończymy na dziś", output.getvalue())


if __name__ == "__main__":
    unittest.main()
