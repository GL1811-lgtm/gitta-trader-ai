import os
import sys
import argparse

# Make sure project root is importable when running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.trainer.trainer import Trainer


def run_trainer(data_path, version_path):
    """Run the trainer and print created version directory."""
    print("Starting trainer...")
    trainer = Trainer(data_path=data_path, version_path=version_path)
    version_dir = trainer.train()
    print(f"Trainer finished. New version at: {version_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gitta Trader AI Trainer')
    parser.add_argument('--data-path', type=str, default='data/crypto_prices.csv', help='Path to the training data')
    parser.add_argument('--version-path', type=str, default='versions', help='Path to the versioning directory')
    args = parser.parse_args()

    run_trainer(args.data_path, args.version_path)
