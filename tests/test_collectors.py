# tests/test_collectors.py
import unittest
import tempfile
import os
import json
import shutil
import sys

# Adjust path to import the runner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents.collectors import run_all

class TestCollectorPipeline(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory to act as the supervisor inbox."""
        self.temp_dir = tempfile.mkdtemp()
        # Monkey-patch the path in the runner script to use the temp directory
        run_all.supervisor_inbox = self.temp_dir

    def tearDown(self):
        """Remove the temporary directory after the test."""
        shutil.rmtree(self.temp_dir)

    def test_run_all_collectors(self):
        """
        Tests that running all collectors creates the correct number of files
        and that the files have the correct message schema.
        """
        # Run the main function from the collector runner script
        total_saved = run_all.main()

        # 1. Assert that the function reports saving 30 strategies
        self.assertEqual(total_saved, 30, "The main runner should report 30 saved strategies.")

        # 2. Assert that 30 files were created (10 agents * 3 strategies each)
        files_in_inbox = os.listdir(self.temp_dir)
        self.assertEqual(len(files_in_inbox), 30, "Should have created 30 strategy files in the inbox.")

        # 3. Assert that a sample file has the correct schema
        sample_file_path = os.path.join(self.temp_dir, files_in_inbox[0])
        with open(sample_file_path, 'r') as f:
            data = json.load(f)

        # Check for the existence of top-level keys from AgentMessage
        self.assertIn("message_type", data)
        self.assertIn("source_agent", data)
        self.assertIn("timestamp", data)
        self.assertIn("payload", data)

        # Check that the message type is correct
        self.assertEqual(data["message_type"], "strategy")

        # Check that the payload has the expected keys from the simulation
        self.assertIn("title", data["payload"])
        self.assertIn("source", data["payload"])
        self.assertIn("summary", data["payload"])

if __name__ == '__main__':
    unittest.main()
