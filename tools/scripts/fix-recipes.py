#!/usr/bin/env python3
"""Fix recipe data model: merge ingredients + needs_restock, create missing ingredient notes."""

import os

VAULT = "/mnt/c/Users/din18/OneDrive/Apps/remotely-save/OneVault"
INGREDIENTS_DIR = os.path.join(VAULT, "Projects/cooking/ingredients")
RECIPES_DIR = os.path.join(VAULT, "Projects/cooking/recipes")

# Missing ingredients referenced by recipes but not yet in the registry
# All have: false (not currently in stock)
MISSING_INGREDIENTS = [
    ("cabbage-slaw", "Cabbage Slaw", "", "produce", "produce", False, "", False),
    ("paneer", "Paneer", "", "fridge", "dairy", False, "", False),
    ("sweet-plantains", "Sweet Plantains (Frozen)", "", "freezer", "frozen", False, "", False),
    ("plantain-chips", "Plantain Chips", "", "pantry", "snack", False, "", False),
    ("peppers", "Peppers (Bell)", "", "produce", "produce", False, "", False),
    ("cucumber", "Cucumber", "", "produce", "produce", False, "", False),
    ("black-chana", "Black Chana", "", "pantry", "canned", False, "", False),
    ("okra", "Okra", "", "produce", "produce", False, "", False),
    ("lemon", "Lemon", "", "produce", "produce", False, "", False),
    ("chaat-masala", "Chaat Masala", "", "pantry", "spice", False, "", False),
    ("sev", "Sev", "", "pantry", "snack", False, "", False),
    ("falafel", "Falafel (Frozen)", "Trader Joe's", "freezer", "frozen", False, "", False),
    ("avocado", "Avocado", "", "produce", "produce", False, "", False),
    ("tomatoes", "Tomatoes", "", "produce", "produce", False, "", False),
    ("brown-rice", "Brown Rice (Frozen)", "Trader Joe's", "freezer", "frozen", False, "", False),
    ("kale", "Kale", "", "produce", "produce", False, "", False),
    ("sweet-potatoes", "Sweet Potatoes", "", "produce", "produce", False, "", False),
    ("pesto", "Pesto", "Trader Joe's", "fridge", "sauce", False, "", False),
    ("inca-corn", "Inca Corn", "Trader Joe's", "pantry", "snack", False, "", False),
    ("pickled-onions", "Pickled Onions", "", "fridge", "sauce", False, "", False),
    ("samosas", "Vegetable Samosas (Frozen)", "Trader Joe's", "freezer", "frozen", False, "", False),
    ("scallion-pancakes", "Scallion Pancakes (Frozen)", "Trader Joe's", "freezer", "frozen", False, "", False),
    ("sourdough-bread", "Sourdough Bread", "", "pantry", "packaged", False, "", False),
    ("everything-seasoning", "Everything But The Bagel Seasoning", "Trader Joe's", "pantry", "spice", False, "", False),
    ("sriracha", "Sriracha", "", "fridge", "sauce", False, "", False),
]


def write_ingredient(slug, name, brand, location, category, have, qty, always_stock):
    have_str = "true" if have else "false"
    stock_str = "true" if always_stock else "false"
    lines = ["---", f'name: "{name}"']
    if brand:
        lines.append(f'brand: "{brand}"')
    lines.extend([
        f"location: {location}",
        f"category: {category}",
        f"have: {have_str}",
    ])
    if qty:
        lines.append(f'qty: "{qty}"')
    lines.extend([
        f"always_stock: {stock_str}",
        "tags: [cooking/ingredient]",
        "---",
        "",
    ])
    path = os.path.join(INGREDIENTS_DIR, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


# Corrected recipes: ALL ingredients in one list
RECIPES = [
    {
        "slug": "arepa-sweet-and-salty",
        "name": "Arepa Sweet and Salty Stack",
        "energy": "medium",
        "time": 25,
        "meal_time": "night",
        "ingredients": ["cabbage-slaw", "black-beans-canned", "paneer", "sweet-plantains",
                        "zhoug-sauce", "dahi", "plantain-chips"],
        "components": {
            "base": "Cabbage Slaw",
            "protein": "Black Beans + Paneer (fried salty)",
            "veggie": "Sweet Plantains",
            "sauce": "Zhoug (mix with yogurt optional)",
            "crunch": "Plantain Chips (crushed)",
        },
    },
    {
        "slug": "choolah-tandoori",
        "name": "Choolah Tandoori Stack",
        "energy": "medium",
        "time": 20,
        "meal_time": "day",
        "ingredients": ["naan-bread", "paneer", "peppers", "red-onions",
                        "tzatziki", "cucumber"],
        "components": {
            "base": "Garlic Naan",
            "protein": "Paneer (tandoori style, air fried with mustard oil/spices)",
            "veggie": "Peppers + Red Onions (sautéed)",
            "sauce": "Tzatziki OR Tikka Simmer Sauce",
            "crunch": "Cucumber (kachumber style)",
        },
    },
    {
        "slug": "desi-crunch",
        "name": "Desi Crunch Stack",
        "energy": "medium",
        "time": 25,
        "meal_time": "night",
        "ingredients": ["cruciferous-crunch", "black-chana", "okra", "besan",
                        "lemon", "chaat-masala", "sev"],
        "components": {
            "base": "Cruciferous Crunch",
            "protein": "Black Chana (boiled)",
            "veggie": "Okra (besan coated, air fried crispy)",
            "sauce": "Lemon + Chaat Masala (dry style)",
            "crunch": "Sev OR the crispy okra itself",
        },
    },
    {
        "slug": "desi-mex-black-bean-tacos",
        "name": "Desi-Mex Black Bean Tacos",
        "energy": "low",
        "time": 15,
        "meal_time": "night",
        "ingredients": ["taco-shells", "black-beans-canned", "frozen-cauliflower",
                        "red-onions", "zhoug-sauce", "cruciferous-crunch"],
        "how": "Sauté onion + cauliflower 5 min → add beans 2 min → stir in Zhoug → stuff shells. Add cheese/avo.",
        "components": {
            "base": "Taco Shells",
            "protein": "Black Beans (canned, drained)",
            "veggie": "Frozen Cauliflower + Red Onions",
            "sauce": "Zhoug (mixed into beans)",
            "crunch": "Cruciferous Crunch (on top)",
        },
    },
    {
        "slug": "falafel-power-bowl",
        "name": "Falafel Power Bowl",
        "energy": "low",
        "time": 10,
        "meal_time": "night",
        "ingredients": ["cruciferous-crunch", "falafel", "avocado", "tomatoes",
                        "tzatziki", "cucumber"],
        "components": {
            "base": "Cruciferous Crunch",
            "protein": "Falafel (air fried)",
            "veggie": "Avocado + Tomatoes",
            "sauce": "Tzatziki",
            "crunch": "Cucumber",
        },
    },
    {
        "slug": "roots-harvest",
        "name": "Roots Harvest Stack",
        "energy": "high",
        "time": 40,
        "meal_time": "any",
        "ingredients": ["brown-rice", "kale", "chickpeas-canned", "silken-tofu",
                        "sweet-potatoes", "pesto", "lemon", "inca-corn", "pickled-onions"],
        "components": {
            "base": "Brown Rice (Day) OR Kale (Night, massaged)",
            "protein": "Chickpeas OR Tofu (sriracha baked)",
            "veggie": "Sweet Potatoes (roasted)",
            "sauce": "Pesto + Lemon squeeze",
            "crunch": "Inca Corn + Pickled Onions",
        },
    },
    {
        "slug": "samosa-chaat-bowl",
        "name": "Samosa Chaat Bowl",
        "energy": "medium",
        "time": 20,
        "meal_time": "night",
        "ingredients": ["cruciferous-crunch", "black-chana", "samosas",
                        "red-onions", "zhoug-sauce", "sev"],
        "components": {
            "base": "Cruciferous Crunch",
            "protein": "Black Chana + Vegetable Samosas",
            "veggie": "Red Onions",
            "sauce": "Zhoug",
            "crunch": "Sev",
        },
    },
    {
        "slug": "scallion-pancake-wrap",
        "name": "Scallion Pancake Wrap",
        "energy": "medium",
        "time": 18,
        "meal_time": "day",
        "ingredients": ["scallion-pancakes", "egg-whites", "cheese-slices-amul",
                        "red-onions", "zhoug-sauce", "cucumber"],
        "components": {
            "base": "Scallion Pancakes",
            "protein": "Egg Whites + Amul Cheese",
            "veggie": "Red Onions",
            "sauce": "Zhoug",
            "crunch": "Cucumber",
        },
    },
    {
        "slug": "sourdough-avo-toast",
        "name": "Sourdough Avo Toast",
        "energy": "low",
        "time": 8,
        "meal_time": "day",
        "ingredients": ["sourdough-bread", "egg-whites", "avocado", "tomatoes",
                        "everything-seasoning"],
        "components": {
            "base": "Sourdough Bread",
            "protein": "Egg Whites (scrambled)",
            "veggie": "Avocado + Tomatoes",
            "sauce": "—",
            "crunch": "Everything Seasoning",
        },
    },
]


def write_recipe(recipe):
    r = recipe
    ing_links = [f'  - "[[{s}]]"' for s in r["ingredients"]]

    lines = [
        "---",
        f'name: "{r["name"]}"',
        f"energy: {r['energy']}",
        f"time: {r['time']}",
        f"meal_time: {r['meal_time']}",
        "ingredients:",
    ]
    lines.extend(ing_links)
    lines.extend(["tags: [cooking/recipe]", "---", "", f"# {r['name']}", ""])
    lines.extend(["| Component | Ingredient |", "|-----------|-----------|"])
    for comp, ing in r["components"].items():
        lines.append(f"| {comp.capitalize()} | {ing} |")
    if "how" in r:
        lines.extend(["", f"**How:** {r['how']}"])
    lines.append("")

    path = os.path.join(RECIPES_DIR, f"{r['slug']}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


if __name__ == "__main__":
    print("Creating missing ingredient notes...")
    for args in MISSING_INGREDIENTS:
        p = write_ingredient(*args)
        print(f"  + {os.path.basename(p)}")
    print(f"\nCreated {len(MISSING_INGREDIENTS)} missing ingredient notes")

    print("\nRewriting recipe notes with unified ingredients list...")
    for recipe in RECIPES:
        p = write_recipe(recipe)
        print(f"  ~ {os.path.basename(p)}")
    print(f"\nUpdated {len(RECIPES)} recipe notes")
    print("\nFix complete!")
