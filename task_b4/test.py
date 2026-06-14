"""
Interactive command-line interface for the trained QuestionClassifier.

Usage:
    python test.py

Make sure train.py has been run first to generate model.pkl and vectorizer.pkl.
"""

from classifier import QuestionClassifier

classifier = QuestionClassifier()

try:
    classifier.load()
except FileNotFoundError as e:
    print(f"Error: {e}")
    raise SystemExit(1)

print("Question Topic Classifier")
print("Type a question and press Enter to classify it.")
print("Type 'exit' to quit.\n")

while True:
    question = input("Enter Question (or 'exit'): ").strip()

    if not question:
        print("Please enter a question.\n")
        continue

    if question.lower() == "exit":
        print("Goodbye.")
        break

    result = classifier.predict(question)

    print("\nResult:")
    print(f"  Topic      : {result['topic']}")
    print(f"  Confidence : {result['confidence']:.2%}")

    if result.get("secondary_topic"):
        print(f"  Also relates to: {result['secondary_topic']}")

    if result.get("uncertain"):
        print("  Note: confidence is low. The question may be out of scope.")

    print()
