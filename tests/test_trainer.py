import os
import sys
import unittest
import shutil

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.trainer.trainer import Trainer


class TestTrainer(unittest.TestCase):
    """Unit tests for the Trainer class."""

    def setUp(self):
        self.data_path = 'test_data.csv'
        self.version_path = 'test_versions'
        # Create a minimal CSV for pandas to read if available
        try:
            import pandas as pd
            df = pd.DataFrame({'timestamp': ['2023-01-01', '2023-01-02'], 'close': [100, 105]})
            df.to_csv(self.data_path, index=False)
        except Exception:
            # If pandas not available just write a simple CSV-like file
            with open(self.data_path, 'w') as fh:
                fh.write('timestamp,close\n2023-01-01,100\n2023-01-02,105\n')

        os.makedirs(self.version_path, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        if os.path.exists(self.version_path):
            shutil.rmtree(self.version_path)

    def test_train_creates_model_and_metadata(self):
        trainer = Trainer(self.data_path, self.version_path)
        trainer.train()

        versions = [d for d in os.listdir(self.version_path) if os.path.isdir(os.path.join(self.version_path, d))]
        self.assertTrue(len(versions) >= 1)

        # Pick the most recent version directory
        versions.sort()
        version_dir = os.path.join(self.version_path, versions[-1])

        # Accept multiple possible model filenames depending on environment
        candidates = ['model.joblib', 'model.pkl', 'model.json']
        found = any(os.path.exists(os.path.join(version_dir, c)) for c in candidates)
        self.assertTrue(found, f"No model file found in {version_dir}")

        # Ensure version metadata exists
        meta_path = os.path.join(version_dir, 'version_metadata.json')
        self.assertTrue(os.path.exists(meta_path), 'version_metadata.json missing')


if __name__ == '__main__':
    unittest.main()
