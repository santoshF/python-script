"""
Load the rotten_tomatoes dataset and split it into train/validation/test.

Usage:
    python3 load_rotten_tomatoes.py
    python3 load_rotten_tomatoes.py --train-size 0.8 --val-size 0.1 --test-size 0.1

Requires: pip install datasets
"""

import argparse

from datasets import load_dataset, concatenate_datasets, DatasetDict


def split_dataset(train_size, val_size, test_size, seed):
    dataset = load_dataset("rotten_tomatoes")
    full = concatenate_datasets([dataset["train"], dataset["validation"], dataset["test"]])

    # First split off the test set.
    split = full.train_test_split(test_size=test_size, seed=seed)

    # Then split the remainder into train/validation.
    val_fraction = val_size / (train_size + val_size)
    train_val_split = split["train"].train_test_split(test_size=val_fraction, seed=seed)

    return DatasetDict(
        {
            "train": train_val_split["train"],
            "validation": train_val_split["test"],
            "test": split["test"],
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-size", type=float, default=0.8)
    parser.add_argument("--val-size", type=float, default=0.1)
    parser.add_argument("--test-size", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if abs(args.train_size + args.val_size + args.test_size - 1.0) > 1e-9:
        raise ValueError("train-size + val-size + test-size must sum to 1.0")

    dataset = split_dataset(args.train_size, args.val_size, args.test_size, args.seed)

    for split_name, split in dataset.items():
        print(f"{split_name}: {len(split)} examples")

    print("\nFirst and last sample from original train split:")
    print(load_dataset("rotten_tomatoes")["train"][0, -1])


if __name__ == "__main__":
    main()
