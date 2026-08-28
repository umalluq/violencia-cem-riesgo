"""Contratos mínimos del orquestador de notebooks."""
import unittest

from run_all import selected_notebooks


class RunAllTests(unittest.TestCase):
    def test_notebooks_are_complete_and_ordered(self) -> None:
        notebooks = selected_notebooks(1)
        self.assertEqual([path.name[:2] for path in notebooks], [f"{number:02d}" for number in range(1, 11)])

    def test_resume_uses_the_requested_notebook(self) -> None:
        self.assertEqual([path.name[:2] for path in selected_notebooks(6)], ["06", "07", "08", "09", "10"])
