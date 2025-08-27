import csv

CSV_FILE = "dataset_2.csv"
# CSV_FILE = "actions_list.csv"


def read_csv(filename):
    """Reads the CSV file and returns a list of actions in dictionary form"""
    actions = []
    with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ignore header
        for row in reader:
            try:
                cost = float(row[1])
                profit_percent = float(row[2].replace("%", "")) / 100 if "%" in row[2] else float(row[2]) / 100
                benefit = cost * profit_percent

                # ⚠️ On ignore les actions incohérentes
                if cost > 0 and benefit > 0:
                    actions.append({
                        "name": row[0],
                        "cost": cost,
                        "benefit": benefit
                    })
            except ValueError:
                continue  # ignore lignes invalides
    return actions


def optimized_knapsack_fast(actions, budget):
    """Knapsack optimisé avec tableau 1D (mémoire réduite)"""
    budget_cents = int(budget * 100)
    n = len(actions)

    # tableau DP 1D
    dp = [0] * (budget_cents + 1)
    keep = [[False] * (budget_cents + 1) for _ in range(n)]  # pour reconstruire la solution

    for i in range(n):
        cost_cents = int(actions[i]["cost"] * 100)
        benefit = actions[i]["benefit"]

        # ⚠️ remplir à rebours pour éviter d’écraser les calculs
        for w in range(budget_cents, cost_cents - 1, -1):
            if benefit + dp[w - cost_cents] > dp[w]:
                dp[w] = benefit + dp[w - cost_cents]
                keep[i][w] = True

    # Reconstruction de la solution
    w = budget_cents
    selected_actions = []
    for i in range(n - 1, -1, -1):
        if keep[i][w]:
            selected_actions.append(actions[i])
            w -= int(actions[i]["cost"] * 100)

    total_cost = sum(a["cost"] for a in selected_actions)
    total_benefit = dp[budget_cents]

    return selected_actions, total_cost, total_benefit


if __name__ == "__main__":
    actions = read_csv(CSV_FILE)
    budget = 500  # budget en €
    selected, cost, benefit = optimized_knapsack_fast(actions, budget)

    print("Actions sélectionnées :")
    for action in selected:
        print(f"- {action['name']} | Coût: {action['cost']} € | Bénéfice: {action['benefit']:.2f} €")

    print(f"\nCoût total = {cost:.2f} € (budget max = {budget} €)")
    print(f"Bénéfice total = {benefit:.2f} €")
