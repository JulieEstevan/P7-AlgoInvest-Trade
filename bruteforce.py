import csv
import itertools

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
            benefit = cost * profit_percent  # profit in euros
            actions.append({
                "name": row["Actions #"],
                "cost": cost,
                "benefit": benefit
            })
    return actions


def brute_force(actions):
    """Explore all possible combinations and return the best one"""
    best_combination = None
    best_profit = 0

    for i in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, i):
            total_cost = sum(a["cost"] for a in combination)
            total_profit = sum(a["benefit"] for a in combination)

            if total_cost <= BUDGET and total_profit > best_profit:
                best_profit = total_profit
                best_combination = combination

    return best_combination, best_profit


if __name__ == "__main__":
    actions = read_csv(CSV_FILE)
    best_combination, best_profit = brute_force(actions)

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(f"- {action['name']} | Coût: {action['cost']:.2f} € | Bénéfice: {action['benefit']:.2f} €")

    total_cost = sum(a["cost"] for a in best_combination)
    print(f"\nCoût total: {total_cost:.2f} €")
    print(f"Bénéfice total après 2 ans: {best_profit:.2f} €")

