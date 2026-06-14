import re
import pickle
import os

import nltk

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


class QuestionClassifier:
    """
    A text classifier that categorises technical questions into one of four
    topics: OOP, Database, Networking, or Machine Learning.

    It uses TF-IDF vectorisation with bigrams and Logistic Regression.
    Pre-processing includes lowercasing, punctuation removal, stop-word
    filtering and lemmatisation.
    """

    # Confidence threshold below which a result is marked as uncertain.
    CONFIDENCE_THRESHOLD = 0.30

    # Gap between top-1 and top-2 confidence below which a secondary topic
    # is reported (multi-topic support).
    SECONDARY_TOPIC_GAP = 0.15

    def __init__(self, model_dir=None):
        """
        Parameters
         ---
        model_dir : str, optional
            Directory used when saving and loading model files.
            Defaults to the directory that contains this source file so
            that save/load work regardless of the current working directory.
        """
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1
        )
        self.model = LogisticRegression(max_iter=1000)

        # Fix: use an absolute path so save/load are not sensitive to cwd.
        if model_dir is None:
            model_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = model_dir

    #          ---
    # Internal helpers
    #          ---

    def _model_path(self):
        return os.path.join(self.model_dir, "model.pkl")

    def _vectorizer_path(self):
        return os.path.join(self.model_dir, "vectorizer.pkl")

    #          ---
    # Pre-processing
    #          ---

    def preprocess(self, text):
        """
        Clean and normalise a raw question string.

        Steps: lowercase, remove punctuation, remove stop words, lemmatise.
        Returns an empty string if nothing meaningful remains after cleaning.
        """
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)

        words = [
            self.lemmatizer.lemmatize(word)
            for word in text.split()
            if word not in self.stop_words
        ]

        return " ".join(words)

    #          ---
    # Training
    #          ---

    def train(self, dataset):
        """
        Fit the vectoriser and classifier on the provided dataset.

        Parameters
         ---
        dataset : list of (str, str)
            Each element is a (question, topic) pair.
        """
        questions = [self.preprocess(q) for q, _ in dataset]
        labels = [topic for _, topic in dataset]

        X = self.vectorizer.fit_transform(questions)
        self.model.fit(X, labels)

    #          ---
    # Prediction
    #          ---

    def predict(self, question):
        """
        Classify a single question.

        Parameters
         ---
        question : str
            The raw question text.

        Returns
         
        dict with keys:
            topic       - predicted topic (str)
            confidence  - probability of the top prediction, rounded to 4 dp
            secondary_topic - present when top-1 and top-2 are close (str)
            uncertain   - present and True when confidence is below threshold
        """
        # Fix: guard against empty or whitespace-only / punctuation-only input.
        processed = self.preprocess(question)
        if not processed.strip():
            return {
                "topic": "Unknown",
                "confidence": 0.0,
                "uncertain": True
            }

        X = self.vectorizer.transform([processed])
        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        ranked = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        top1_topic, top1_prob = ranked[0]
        top2_topic, top2_prob = ranked[1]

        result = {
            # Fix: cast numpy.str_ to plain Python str so equality checks,
            # JSON serialisation and accuracy_score all work correctly.
            "topic": str(top1_topic),
            "confidence": round(float(top1_prob), 4)
        }

        # Multi-topic support: report secondary when predictions are close.
        if top1_prob - top2_prob < self.SECONDARY_TOPIC_GAP:
            result["secondary_topic"] = str(top2_topic)

        # Flag low-confidence results so callers can handle them gracefully.
        if top1_prob < self.CONFIDENCE_THRESHOLD:
            result["uncertain"] = True

        return result

    #          ---
    # Evaluation
    #          ---

    def evaluate(self, dataset):
        """
        Print accuracy and a per-class classification report.

        Parameters
         ---
        dataset : list of (str, str)
        """
        questions = [self.preprocess(q) for q, _ in dataset]
        actual_labels = [topic for _, topic in dataset]

        X = self.vectorizer.transform(questions)
        predictions = self.model.predict(X)

        # Fix: cast predictions to plain str list so accuracy_score comparison
        # works correctly (numpy.str_ != str in some sklearn/numpy versions).
        predictions = [str(p) for p in predictions]

        accuracy = accuracy_score(actual_labels, predictions)
        print(f"\nAccuracy: {accuracy:.2%}")
        print(classification_report(actual_labels, predictions, zero_division=0))

    #          ---
    # Persistence
    #          ---

    def save(self):
        """
        Persist the trained model and vectoriser to disk.

        Files are written to self.model_dir (defaults to the directory that
        contains classifier.py), so the paths are independent of cwd.
        """
        with open(self._model_path(), "wb") as f:
            pickle.dump(self.model, f)

        with open(self._vectorizer_path(), "wb") as f:
            pickle.dump(self.vectorizer, f)

    def load(self):
        """
        Load a previously saved model and vectoriser from self.model_dir.

        Raises FileNotFoundError if the files do not exist.
        """
        model_path = self._model_path()
        vectorizer_path = self._vectorizer_path()

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                "Run train.py first to generate model.pkl."
            )
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(
                f"Vectoriser file not found: {vectorizer_path}\n"
                "Run train.py first to generate vectorizer.pkl."
            )

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)
