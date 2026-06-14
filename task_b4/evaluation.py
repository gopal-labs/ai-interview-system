"""
Evaluate the QuestionClassifier on a held-out test split.

Usage:
    python evaluation.py

The script trains a fresh classifier on 80 % of the dataset and tests it
on the remaining 20 %, then prints accuracy and a per-class report.
"""

from dataset import DATASET
from classifier import QuestionClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

questions = [q for q, t in DATASET]
labels = [t for q, t in DATASET]

X_train, X_test, y_train, y_test = train_test_split(
    questions,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

train_data = list(zip(X_train, y_train))

classifier = QuestionClassifier()
classifier.train(train_data)

predictions = []
for q in X_test:
    result = classifier.predict(q)
    predictions.append(result["topic"])

# Fix: predict() now returns plain str, so accuracy_score works correctly.
accuracy = accuracy_score(y_test, predictions)

print(f"Hold-out test accuracy: {accuracy:.2%}")
print(f"Test set size: {len(y_test)} samples")
print()

for actual, predicted, question in zip(y_test, predictions, X_test):
    status = "CORRECT" if actual == predicted else "WRONG  "
    print(f"  [{status}]  actual={actual:<20}  predicted={predicted:<20}  question={question}")
