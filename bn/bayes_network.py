class MisinformationBN:
    """Simple rule-based Bayesian-style scorer for misinformation.

    Variables:
        - sourcecred: 'Low' | 'Medium' | 'High'
        - ling_uncertainty: 'Low' | 'Medium' | 'High'
        - sensational: 'Present' | 'Absent'
        - fact_contradiction: 'Yes' | 'No'
    """

    def __init__(self):
        pass

    def compute_score(self, sourcecred, ling_uncertainty, sensational, fact_contradiction):
        score = 0

        if sourcecred == "Low":
            score += 2
        elif sourcecred == "Medium":
            score += 1

        if ling_uncertainty == "High":
            score += 2
        elif ling_uncertainty == "Medium":
            score += 1

        if sensational == "Present":
            score += 2

        if fact_contradiction == "Yes":
            score += 3

        return score

    def classify(self, score):
        if score <= 2:
            return "Low"
        elif score <= 5:
            return "Medium"
        return "High"

    def posterior(self, evidence):
        """Return posterior label and score given evidence dict."""
        score = self.compute_score(
            evidence.get("source_cred", "Medium"),
            evidence.get("ling_uncertainty", "Medium"),
            evidence.get("sensational", "Absent"),
            evidence.get("fact_contradiction", "No"),
        )
        label = self.classify(score)
        return label, score
