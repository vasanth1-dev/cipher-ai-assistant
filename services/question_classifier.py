import re


class QuestionClassifier:

    SIMPLE_PATTERNS = (
        r"^what is\b",
        r"^who is\b",
        r"^who invented\b",
        r"^when\b",
        r"^where\b",
        r"^define\b",
        r"^meaning of\b",
        r"^full form\b",
    )

    DETAIL_WORDS = (
        "explain",
        "detail",
        "detailed",
        "describe",
        "comparison",
        "compare",
        "advantages",
        "disadvantages",
        "architecture",
        "working",
        "how",
        "why",
        "example",
        "examples",
        "tutorial",
        "guide",
    )

    def is_simple(self, text):

        text = text.lower().strip()

        if any(word in text for word in self.DETAIL_WORDS):
            return False

        for pattern in self.SIMPLE_PATTERNS:

            if re.match(pattern, text):
                return True

        return False


question_classifier = QuestionClassifier()