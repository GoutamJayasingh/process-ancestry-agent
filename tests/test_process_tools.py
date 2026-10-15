import os
import unittest

from tools.process_info import get_process_info
from tools.process_lookup import find_process
from tools.ancestry import get_process_ancestry
from tools.process_tree import get_process_tree


class TestProcessTools(unittest.TestCase):

    def test_current_process_info(self):
        info = get_process_info(os.getpid())

        self.assertEqual(info["pid"], os.getpid())
        self.assertTrue(info["name"])
        self.assertGreaterEqual(info["ppid"], 0)

    def test_find_existing_process(self):
        # The Python process running this test must exist.
        info = get_process_info(os.getpid())
        matches = find_process(info["name"])

        self.assertTrue(
            any(process["pid"] == os.getpid() for process in matches)
        )

    def test_nonexistent_process_name(self):
        matches = find_process(
            "process_name_that_does_not_exist_12345"
        )
        self.assertEqual(matches, [])

    def test_ancestry_starts_with_target(self):
        pid = os.getpid()
        ancestry = get_process_ancestry(pid)

        self.assertTrue(ancestry)
        self.assertEqual(ancestry[0]["pid"], pid)

    def test_process_tree(self):
        info = get_process_info(os.getpid())
        results = get_process_tree(info["name"])

        self.assertTrue(
            any(
                result["process"]["pid"] == os.getpid()
                for result in results
            )
        )


if __name__ == "__main__":
    unittest.main()
