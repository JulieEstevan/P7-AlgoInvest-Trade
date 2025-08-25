import csv

BUDGET = 500
CSV_FILE = "actions_list.csv"


def read_csv(filename):
    """Reads the CSV file and returns a list of actions in dictionary form"""
    actions = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cost = float(row["Coût par action (en euros)"])
            profit_percent = float(row["Bénéfice (après 2 ans)"].replace("%", "")) / 100
            benefit = cost * profit_percent
            actions.append({
                "name": row["Actions #"],
                "cost": cost,
                "benefit": benefit
            })
    return actions


def optimized_knapsack(actions, budget):
    """Optimized Backpack Algorithm (DP)"""
    n = len(actions)

    # DP matrix (n+1 x budget+1)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    # Filling
    for i in range(1, n + 1):
        for w in range(1, budget + 1):
            cost = int(actions[i - 1]["cost"])
            benefit = actions[i - 1]["benefit"]

            if cost <= w:
                dp[i][w] = max(benefit + dp[i - 1][w - cost], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruction of the selected actions
    w = budget
    chosen_actions = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen_actions.append(actions[i - 1])
            w -= int(actions[i - 1]["cost"])

    return chosen_actions, dp[n][budget]


if __name__ == "__main__":
    actions = read_csv(CSV_FILE)
    best_combination, best_profit = optimized_knapsack(actions, BUDGET)

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(f"- {action['name']} | Coût: {action['cost']:.2f} € | Bénéfice: {action['benefit']:.2f} €")

    total_cost = sum(a["cost"] for a in best_combination)
    print(f"\nCoût total: {total_cost:.2f} €")
    print(f"Bénéfice total après 2 ans: {best_profit:.2f} €")
