import json
import re

def tokenize(text):
    """Extract clean lowercase words removing punctuation."""
    return set(re.findall(r"[a-zA-Z]+", text.lower()))

class KnowledgeGraphSearcher:
    """
    Fully corrected evidence retrieval.

    - Does NOT rely on links.
    - Does NOT require start node.
    - Checks ALL news articles.
    - Picks the news article with highest keyword match.
    """

    def __init__(self, kb_path):
        with open(kb_path, "r") as f:
            self.kb = json.load(f)

    
    def compute_match_score(self, node, query):
        query_words = tokenize(query)

        text_words  = tokenize(node["text"])
        title_words = tokenize(node["title"])
        tag_words   = tokenize(" ".join(node.get("tags", [])))
        auto_words  = tokenize(" ".join(node.get("auto_tags", []))) if node.get("auto_tags") else set()

        all_words = text_words | title_words | tag_words | auto_words

        return len(all_words & query_words)



    