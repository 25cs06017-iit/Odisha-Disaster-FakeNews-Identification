class POPPlanner:
    """Minimal Partial-Order Planner representation.

    For this project we don't implement full POP search; we just build
    a partial order around the same hard-coded actions.
    """

    def build_partial_order(self):
        steps = [
            "Start",
            "VerifySource",
            "RetrieveFact",
            "GenerateCounterMessage",
            "Finish",
        ]

        ordering = [
            ("Start", "VerifySource"),
            ("VerifySource", "RetrieveFact"),
            ("RetrieveFact", "GenerateCounterMessage"),
            ("GenerateCounterMessage", "Finish"),
        ]

        causal_links = [
            ("VerifySource", "SourceVerified", "RetrieveFact"),
            ("RetrieveFact", "FactRetrieved", "GenerateCounterMessage"),
        ]

        return {
            "steps": steps,
            "ordering": ordering,
            "causal_links": causal_links,
        }
