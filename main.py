import json
from bn import MisinformationBN
from retrieval import KnowledgeGraphSearcher
from planning import GraphPlanPlanner, POPPlanner
from rl import q_learning_train, greedy_policy
from advisory import generate_advisory


def analyze_user_message(text):
    text_l = text.lower()

    
    low_sources = ["forwarded", "i heard", "someone said", "viral", "rumor", "unverified"]
    med_sources = ["people say", "reports say", "some news"]
    high_sources = ["official", "government", "imd", "osdma"]

    if any(word in text_l for word in low_sources):
        source_cred = "Low"
    elif any(word in text_l for word in high_sources):
        source_cred = "High"
    else:
        source_cred = "Medium"

    
    uncertainty_words = ["maybe", "possibly", "might", "not sure", "unknown"]
    if any(w in text_l for w in uncertainty_words):
        ling = "High"
    else:
        ling = "Medium"


    sensational_words = ["poison", "collapse", "deadly", "destroyed", "permanent", "danger", "catastrophic"]
    sensational = "Present" if any(w in text_l for w in sensational_words) else "Absent"

    
    return {
        "text": text,
        "source_cred": source_cred,
        "ling_uncertainty": ling,
        "sensational": sensational,
        "fact_contradiction": "No"
    }


def run_demo():

    print("\n=== AI-Driven Misinformation Detection and Response Demo ===\n")

    
    user_news = input("Enter the news message you received: ").strip()
    msg = analyze_user_message(user_news)

    print("\nYour Input:", msg["text"])
    print("Auto-detected features:", msg, "\n")

    
    bn = MisinformationBN()
    label, score = bn.posterior({
        "source_cred": msg["source_cred"],
        "ling_uncertainty": msg["ling_uncertainty"],
        "sensational": msg["sensational"],
        "fact_contradiction": "No",   
    })

    print(f"[BN Initial] Score={score}, Estimated Misinformation Level={label}\n")

    
    searcher = KnowledgeGraphSearcher("data/knowledge_base.json")


    bfs_node, bfs_score = searcher.bfs_search(msg["text"])
    astar_node, astar_score = searcher.astar_search(msg["text"])


    print("[Retrieval] BFS found:", bfs_node["id"], "| Score:", bfs_score)
    print("[Retrieval] A* found:", astar_node["id"], "| Score:", astar_score)

    print("\nMost relevant verified evidence:\n", astar_node["text"], "\n")

    
    contradiction = "Yes" if any(word in msg["text"].lower() 
                                  for word in astar_node["text"].lower().split()) == False else "No"

    
    final_label, final_score = bn.posterior({
        "source_cred": msg["source_cred"],
        "ling_uncertainty": msg["ling_uncertainty"],
        "sensational": msg["sensational"],
        "fact_contradiction": contradiction,
    })

    print(f"[BN Final] New Score={final_score}, Final Misinformation Level={final_label}")
    print(f"Contradiction with verified facts: {contradiction}\n")

    
    gp = GraphPlanPlanner()
    initial_facts = {"MessageReceived"}
    if final_label == "High":
        initial_facts.add("MisinformationHigh")
    else:
        initial_facts.add("MisinformationLow")

    goals = {"PublicAdvisoryReady", "HumanReview"}
    plan, final_facts, missing = gp.plan(initial_facts, goals)

    print("[GraphPlan] Action Plan:", plan)
    print("[GraphPlan] Final Facts:", final_facts)
    print("[GraphPlan] Missing Goals:", missing, "\n")

    
    pop = POPPlanner()
    po = pop.build_partial_order()
    print("[POP] Steps:", po["steps"])
    print("[POP] Ordering:", po["ordering"])
    print("[POP] Causal links:", po["causal_links"], "\n")

    
    print("[RL] Training Q-learning model...\n")
    Q = q_learning_train(episodes=1000)
    policy = greedy_policy(Q)

    print("[RL] Learned Moderation Policy:")
    for risk, action in policy.items():
        print(" ", risk, "→", action)
    print()

    
    advisory = generate_advisory(astar_node["text"])

    print("\n=== FINAL OFFICIAL ADVISORY ===\n")
    print(advisory)
    print("\n=================================\n")


if __name__ == "__main__":
    run_demo()
