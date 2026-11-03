# PART 1 - KNOWLEDGE REPRESENTATION (KR): KNOWLEDGE BASE

# The dictionary stores facts about the current weather.
# The facts are grouped into three categories:
# temperature, weather conditions, and environment.
facts = {
    "temperature": 32,          # degrees Celsius
    "is_raining": False,
    "humidity": 85,              # percent
    "wind_speed": 10,            # kilometers per hour
    "dark_clouds": True,
    "has_thunder": False
}


# PART 2 - RULE-BASED REASONING (RBR)

def rule_hot_weather(knowledge):
    """IF temperature is above 30, THEN advise staying cool."""
    if knowledge["temperature"] > 30:
        return "The weather is hot. Stay hydrated and seek shade."
    return None


def rule_rainy_weather(knowledge):
    """IF it is raining, THEN advise bringing an umbrella."""
    if knowledge["is_raining"]:
        return "It is raining. Bring an umbrella."
    return None


def rule_high_humidity(knowledge):
    """IF humidity is at least 80%, THEN advise extra comfort precautions."""
    if knowledge["humidity"] >= 80:
        return "Humidity is high. Stay in a well-ventilated area."
    return None


def rule_dark_clouds(knowledge):
    """IF dark clouds are present, THEN advise monitoring the weather."""
    if knowledge["dark_clouds"]:
        return "Dark clouds are present. Monitor the weather for possible rain."
    return None


def rule_thunderstorm(knowledge):
    """IF thunder is detected, THEN advise moving to a safe indoor place."""
    if knowledge["has_thunder"]:
        return "Thunder is detected. Stay indoors and follow weather advisories."
    return None

# The inference engine checks every rule against the knowledge base.
def inference_engine(knowledge):
    rules = [
        rule_hot_weather,
        rule_rainy_weather,
        rule_high_humidity,
        rule_dark_clouds,
        rule_thunderstorm
    ]

    inferred_actions = []
    for rule in rules:
        result = rule(knowledge)
        if result is not None:
            inferred_actions.append(result)

    return inferred_actions


# PART 3 - CASE-BASED REASONING (CBR)

case_base = [
    {
        "problem": {
            "is_raining": True,
            "dark_clouds": True,
            "high_humidity": True,
            "has_thunder": False
        },
        "solution": "Bring an umbrella and monitor the weather."
    },
    {
        "problem": {
            "is_raining": False,
            "dark_clouds": False,
            "high_humidity": False,
            "has_thunder": False
        },
        "solution": "Enjoy the clear weather and continue normal activities."
    },
    {
        "problem": {
            "is_raining": True,
            "dark_clouds": True,
            "high_humidity": True,
            "has_thunder": True
        },
        "solution": "Stay indoors and follow official weather advisories."
    }
]


def similarity(new_problem, old_problem):
    """
    Compare two cases feature by feature.
    Similarity = matching features / total features.
    The result is a value from 0.0 to 1.0.
    """
    features = new_problem.keys()
    if not features:
        return 0.0

    matches = sum(
        1 for feature in features
        if new_problem[feature] == old_problem.get(feature)
    )
    return matches / len(features)


def retrieve_case(new_problem, cases):
    """RETRIEVE: find and return the most similar past case."""
    best_case = None
    best_score = -1

    for case in cases:
        score = similarity(new_problem, case["problem"])
        if score > best_score:
            best_score = score
            best_case = case

    return best_case, best_score


def reuse_solution(retrieved_case):
    """REUSE: use the solution from the most similar past case."""
    return retrieved_case["solution"]


def revise_solution(proposed_solution):
    """
    REVISE: allow the user to accept the proposed solution
    or enter an adjusted solution. Press Enter to keep it.
    """
    print("\nProposed solution:", proposed_solution)
    revised = input("Revise the solution? Type a new solution or press Enter to keep it: ")
    if revised.strip():
        return revised.strip()
    return proposed_solution


def retain_case(new_problem, final_solution, cases):
    """RETAIN: save the new problem and final solution as a new case."""
    cases.append({
        "problem": new_problem.copy(),
        "solution": final_solution
    })


# MAIN PROGRAM - DISPLAY INPUT, PROCESS, AND OUTPUT

def main():
    print("=" * 60)
    print("TA4: KNOWLEDGE REPRESENTATION, RBR, AND CBR")
    print("=" * 60)

    print("\nPART 1 - KNOWLEDGE BASE")
    for fact, value in facts.items():
        print(f"- {fact}: {value}")

    print("\nPART 2 - RULE-BASED REASONING")
    actions = inference_engine(facts)
    print("Rule-Based Reasoning Actions:")
    if actions:
        for action in actions:
            print("-", action)
    else:
        print("- No rules were triggered.")

    print("\nPART 3 - CASE-BASED REASONING")
    # This sample problem is based on the current weather facts.
    new_problem = {
        "is_raining": facts["is_raining"],
        "dark_clouds": facts["dark_clouds"],
        "high_humidity": facts["humidity"] >= 80,
        "has_thunder": facts["has_thunder"]
    }

    print("New problem:", new_problem)

    # RETRIEVE
    matched_case, score = retrieve_case(new_problem, case_base)
    print(f"Retrieved case similarity: {score:.0%}")

    # REUSE
    proposed_solution = reuse_solution(matched_case)
    print("Reused solution:", proposed_solution)

    # REVISE
    final_solution = revise_solution(proposed_solution)
    print("Final solution:", final_solution)


if __name__ == "__main__":
    main()
