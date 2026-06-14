"""
Training dataset for the QuestionClassifier.

"""

import random

TOPICS = {
    "OOP": {
        "terms": [
            "class",
            "object",
            "inheritance",
            "polymorphism",
            "encapsulation",
            "abstraction",
            "interface",
            "constructor",
            "method overriding",
            "composition"
        ]
    },

    "Database": {
        "terms": [
            "SQL",
            "primary key",
            "foreign key",
            "normalization",
            "index",
            "join",
            "transaction",
            "schema",
            "table",
            "stored procedure"
        ]
    },

    "Networking": {
        "terms": [
            "TCP",
            "UDP",
            "DNS",
            "router",
            "switch",
            "firewall",
            "subnetting",
            "HTTP",
            "IP address",
            "VPN"
        ]
    },

    "Machine Learning": {
        "terms": [
            "regression",
            "classification",
            "clustering",
            "neural network",
            "overfitting",
            "dataset",
            "feature engineering",
            "gradient descent",
            "random forest",
            "cross validation"
        ]
    }
}

TEMPLATES = [
    "What is {}?",
    "Explain {}.",
    "How does {} work?",
    "Why is {} important?",
    "What are the advantages of {}?",
    "What are the disadvantages of {}?",
    "Compare {} with other approaches.",
    "When should {} be used?",
    "Give a real-world example of {}.",
    "What problems does {} solve?",

    # Scenario based
    "A developer is using {}. What should they know?",
    "How would you implement {} in a project?",
    "What happens if {} is used incorrectly?",
    "What are best practices for {}?",
    "How can {} improve system performance?",

    # Interview style
    "Explain {} as if you were in a technical interview.",
    "What are common mistakes related to {}?",
    "How would you explain {} to a beginner?",
    "What are advanced concepts related to {}?",
    "How is {} used in industry?"
]

def generate_dataset(samples_per_topic=100):

    dataset = []

    for topic, data in TOPICS.items():

        terms = data["terms"]

        while len(
            [x for x in dataset if x[1] == topic]
        ) < samples_per_topic:

            term = random.choice(terms)

            template = random.choice(TEMPLATES)

            question = template.format(term)

            dataset.append(
                (
                    question,
                    topic
                )
            )

    random.shuffle(dataset)

    return dataset

generate_dataset()

DATASET = generate_dataset(
    samples_per_topic=100
)

if __name__ == "__main__":

    print(
        f"Dataset Size: {len(DATASET)}"
    )

    for row in DATASET[:10]:
        print(row)
