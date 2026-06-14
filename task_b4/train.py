"""
Train the QuestionClassifier on the full dataset and save the model to disk.

Usage:
    python train.py
"""

from dataset import DATASET
from classifier import QuestionClassifier

classifier = QuestionClassifier()

classifier.train(DATASET)

# Evaluate on the full training set to confirm the model fits the data.
# For a held-out accuracy figure, run evaluation.py.
classifier.evaluate(DATASET)

classifier.save()

print("\nModel saved successfully.")
