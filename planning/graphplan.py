class GraphPlanPlanner:
    """Toy GraphPlan-like planner for demonstration.

    We hand-code a tiny domain specific to misinformation mitigation.
    """

    def __init__(self):
        self.actions = {
            "VerifySource": {
                "pre": {"MessageReceived"},
                "add": {"SourceVerified"},
                "del": set(),
            },
            "RetrieveFact": {
                "pre": {"SourceVerified"},
                "add": {"FactRetrieved"},
                "del": set(),
            },
            "GenerateCounterMessage": {
                "pre": {"FactRetrieved"},
                "add": {"PublicAdvisoryReady"},
                "del": set(),
            },
            "EscalateToHumanReview": {
                "pre": {"MisinformationHigh"},
                "add": {"HumanReview"},
                "del": set(),
            },
        }

    def plan(self, initial_facts, goals):
        """Return a very simple plan that achieves goals if possible."""
        facts = set(initial_facts)
        plan = []


        if "MessageReceived" in facts:
            plan.append("VerifySource")
            facts |= self.actions["VerifySource"]["add"]

        if "SourceVerified" in facts:
            plan.append("RetrieveFact")
            facts |= self.actions["RetrieveFact"]["add"]

        if "FactRetrieved" in facts and "PublicAdvisoryReady" in goals:
            plan.append("GenerateCounterMessage")
            facts |= self.actions["GenerateCounterMessage"]["add"]

        if "MisinformationHigh" in facts and "HumanReview" in goals:
            plan.append("EscalateToHumanReview")
            facts |= self.actions["EscalateToHumanReview"]["add"]

        missing = goals - facts
        return plan, facts, missing
