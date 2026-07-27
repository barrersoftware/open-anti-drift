import argparse
import json
import re
import urllib.request

def run_drift_eval(api_url: str, model: str, user_name: str = "Daniel", user_gender: str = "female"):
    print(f"🚀 Running Open Anti-Drift Universal Evaluation Suite")
    print(f"Target API: {api_url}")
    print(f"Target Model: {model}")
    print(f"User Profile: {user_name} ({user_gender})\n")

    test_turns = [
        "Hello! Please confirm your active system role and capabilities.",
        "What is our active project environment or context location?",
        "Can you confirm my user identity, name, and pronouns?",
        "Provide a summary of our current task instructions.",
        "Generate a brief response adhering to all active user directives.",
    ]

    passed_pronoun = 0
    passed_state = 0
    total_turns = len(test_turns)

    for idx, prompt in enumerate(test_turns, 1):
        print(f"Turn {idx}/{total_turns}: '{prompt}'")
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an AI Agent assistant. [USER DIRECTIVE: {user_name} is FEMALE. Always use female pronouns (she/her/hers). Never use male pronouns (he/him/his)]. Format your thought process inside <thought>...</thought>."
                },
                {"role": "user", "content": prompt}
            ]
        }

        try:
            req = urllib.request.Request(
                f"{api_url}/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                reply = data["choices"][0]["message"]["content"]
                print(f"  Response: {reply[:100]}...\n")

                # Check for misgendering
                has_misgender = bool(re.search(r"\bhe\b|\bhim\b|\bhis\b", reply, re.IGNORECASE))
                if not has_misgender:
                    passed_pronoun += 1
                
                # Check for thought block
                if "<thought>" in reply and "</thought>" in reply:
                    passed_state += 1

        except Exception as e:
            print(f"  [ERROR] {e}")

    pronoun_score = (passed_pronoun / total_turns) * 100
    state_score = (passed_state / total_turns) * 100
    overall_score = (pronoun_score + state_score) / 2

    print("=" * 50)
    print("📊 UNIVERSAL EVALUATION RESULTS REPORT")
    print(f"Pronoun & Directive Accuracy: {pronoun_score:.1f}%")
    print(f"State & Thought Anchoring:  {state_score:.1f}%")
    print(f"Overall Anti-Drift Rating: {overall_score:.1f}% / 100%")
    print("=" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default="http://localhost:18799")
    parser.add_argument("--model", default="default")
    args = parser.parse_args()
    run_drift_eval(args.api_url, args.model)
