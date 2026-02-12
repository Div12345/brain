#!/usr/bin/env python3
"""Migrate cooking inventory and stacks to one-note-per-entity Obsidian structure."""

import os

VAULT = "/mnt/c/Users/din18/OneDrive/Apps/remotely-save/OneVault"
INGREDIENTS_DIR = os.path.join(VAULT, "Projects/cooking/ingredients")
RECIPES_DIR = os.path.join(VAULT, "Projects/cooking/recipes")

os.makedirs(INGREDIENTS_DIR, exist_ok=True)
os.makedirs(RECIPES_DIR, exist_ok=True)

# ── Ingredients ──────────────────────────────────────────────────────────────

INGREDIENTS = [
    # PANTRY - Spices & Seasonings
    ("red-chilli-powder", "Red Chilli Powder", "unknown", "pantry", "spice", True, "14 oz (400g)", False),
    ("coriander-powder", "Coriander Powder", "Roshan", "pantry", "spice", True, "", False),
    ("hing", "Compounded Asafoetida (Hing)", "LG", "pantry", "spice", True, "small jar", False),
    ("ground-nutmeg", "Ground Nutmeg", "Stonemill", "pantry", "spice", True, "jar", False),
    ("ground-cloves", "Ground Cloves", "Stonemill", "pantry", "spice", True, "jar", False),
    ("dried-basil", "Dried Basil", "Simply Organic", "pantry", "spice", True, "glass jar", False),
    ("dried-rosemary", "Dried Rosemary", "Simply Organic", "pantry", "spice", True, "glass jar", False),
    ("cumin-seeds", "Cumin Seeds", "Laxmi", "pantry", "spice", True, "14 oz (400g)", False),
    ("mustard-seeds", "Mustard Seeds", "Laxmi", "pantry", "spice", True, "14 oz (400g)", False),
    ("chutney-powder", "Chutney Powder", "Brahmins", "pantry", "spice", True, "100g box", False),

    # PANTRY - Coffee & Beverages
    ("cothas-coffee", "Cothas Coffee (South Indian Filter)", "Cothas", "pantry", "coffee", True, "yellow bag", False),
    ("sukku-malli-coffee", "Sukku Malli Coffee Powder (Dry Ginger)", "Sri Krishna Sweets", "pantry", "coffee", True, "200g", False),
    ("instant-coffee", "Instant Coffee/Spice Jar", "Medaglia", "pantry", "coffee", True, "small jar", False),

    # PANTRY - Flours
    ("all-purpose-flour", "All Purpose Flour", "Gold Medal", "pantry", "flour", True, "", False),
    ("maida-flour", "Maida Flour (Superfine Wheat)", "Taza", "pantry", "flour", True, "2 lbs", False),
    ("besan", "Besan / Gram Flour", "Laxmi", "pantry", "flour", True, "", False),
    ("sooji", "Sooji / Semolina (Rava)", "Keshav's", "pantry", "flour", True, "2 lbs", False),
    ("kanji-mao-flour", "Kanji Mao / Sattu Mao Flour", "Bombay General Stores", "pantry", "flour", True, "500g", False),
    ("gf-baking-flour", "Gluten-Free 1-to-1 Baking Flour", "Bob's Red Mill", "pantry", "flour", True, "", False),
    ("corn-starch", "Corn Starch", "Good & Gather", "pantry", "flour", True, "box", False),

    # PANTRY - Baking
    ("baking-soda", "Baking Soda", "Giant Eagle", "pantry", "baking", True, "", False),
    ("baking-powder", "Baking Powder (Double-Acting)", "Good & Gather", "pantry", "baking", True, "8.1 oz (230g)", False),
    ("granulated-sugar", "Premium Granulated Sugar", "Baker's Corner", "pantry", "baking", True, "large bag", False),
    ("brown-sugar", "Brown Sugar", "", "pantry", "baking", True, "bag", False),
    ("pancake-mix-bobs", "Buttermilk Pancake & Waffle Mix (Whole Grain)", "Bob's Red Mill", "pantry", "baking", True, "", False),
    ("pancake-mix-millville", "Buttermilk Pancake & Waffle Mix (Complete)", "Millville", "pantry", "baking", True, "", False),
    ("pineapple-cake-mix", "Pineapple Supreme Cake Mix", "Duncan Hines", "pantry", "baking", True, "", False),
    ("blueberry-muffin-mix", "Blueberry Muffin/Biscuit Mix", "", "pantry", "baking", True, "", False),

    # PANTRY - Packaged
    ("taco-shells", "Organic Yellow Corn Taco Shells", "Trader Joe's", "pantry", "packaged", True, "12 shells, 5.5 oz", False),
    ("mac-and-cheese-tjs", "Cheddar Macaroni & Cheese", "Trader Joe's", "pantry", "packaged", True, "7.25 oz", False),
    ("mac-and-cheese", "Macaroni & Cheese Dinner", "", "pantry", "packaged", True, "", False),
    ("chia-seeds", "Organic Chia Seeds", "Trader Joe's", "pantry", "packaged", True, "", False),
    ("bhel-puri", "Bhel Puri Snack Mix", "Haldiram's", "pantry", "packaged", True, "large bag", False),
    ("marshmallows", "Marshmallows", "Giant Eagle", "pantry", "packaged", True, "", False),
    ("froot-loops", "Froot Loops Cereal Cup", "Kellogg's", "pantry", "packaged", True, "1 oz", False),
    ("dark-syrup", "Dark Syrup/Sauce", "", "pantry", "packaged", True, "bottle", False),

    # PANTRY - Canned
    ("chickpeas-canned", "Chick Peas / Garbanzos (Canned)", "Goya", "pantry", "canned", True, "multiple cans", False),
    ("kidney-beans", "Dark Red Kidney Beans (Canned)", "Dakota's Pride", "pantry", "canned", True, "can", False),
    ("corn-canned", "Whole Kernel Golden Sweet Corn (Canned)", "Happy Harvest", "pantry", "canned", True, "multiple cans", False),
    ("vegetable-soup", "Vegetable Soup (Low Sodium)", "Campbell's", "pantry", "canned", True, "7.25 oz", False),
    ("peach-slices", "Peach Slices in Natural Juice", "NeoStar", "pantry", "canned", True, "can", False),

    # COUNTER
    ("ghee", "Pure Ghee", "Amul", "counter", "staple", True, "2 x 1L tins", False),
    ("ketchup", "Rich Tomato Ketchup", "Maggi", "counter", "sauce", True, "bottle", False),

    # FRIDGE - Sauces & Condiments
    ("zhoug-sauce", "Zhoug Sauce (Spicy Green)", "Trader Joe's", "fridge", "sauce", True, "8 oz (227g)", True),
    ("jalapeno-sauce", "Jalapeño Sauce", "Trader Joe's", "fridge", "sauce", True, "10 oz", False),
    ("pickled-jalapenos", "Pickled Jalapeño Pepper Slices", "Trader Joe's", "fridge", "sauce", True, "12.5 fl oz", False),
    ("peri-peri-sauce", "Peri-Peri Sauce (Fermented Dried Chilies)", "Trader Joe's", "fridge", "sauce", True, "6.76 fl oz", False),
    ("soyaki", "Soyaki Teriyaki Sauce/Marinade", "Trader Joe's", "fridge", "sauce", True, "21 oz", False),
    ("marinara-sauce", "Marinara Sauce", "Rao's Homemade", "fridge", "sauce", True, "28 oz, 2 jars", False),
    ("soy-sauce", "Soy Sauce", "Kikkoman", "fridge", "sauce", True, "15 fl oz", False),
    ("balsamic-vinaigrette", "Balsamic Vinaigrette", "Ken's Steak House", "fridge", "sauce", True, "16 fl oz", False),
    ("chilean-everything-sauce", "Chilean Everything Sauce", "Sir Kensington's", "fridge", "sauce", True, "bottle", False),
    ("italian-dressing", "Italian Dressing", "Pampa", "fridge", "sauce", True, "16 fl oz", False),
    ("gongura-pickle", "Gongura Red Chilli Pickle", "Priya", "fridge", "sauce", True, "10.6 oz (300g)", False),
    ("tamarind-concentrate", "Tamarind Concentrate", "Laxmi", "fridge", "sauce", True, "14 oz (400g)", False),
    ("ginger-garlic-paste", "Ginger Garlic Paste", "Shan", "fridge", "sauce", True, "~24 oz jar", False),
    ("vanilla-extract", "Vanilla Extract (Organic)", "", "fridge", "baking", True, "small bottle", False),

    # FRIDGE - Dips
    ("hummus", "Roasted Red Pepper Hummus", "Trader Joe's", "fridge", "dip", True, "tub", False),
    ("tzatziki", "Tzatziki / Herb Dip", "", "fridge", "dip", True, "tub", False),

    # FRIDGE - Dairy
    ("butter", "Salted Butter (4 Quarters)", "Trader Joe's", "fridge", "dairy", True, "16 oz (1 lb)", False),
    ("dahi", "Dahi (Indian Whole Milk Plain Yogurt)", "Dahi", "fridge", "dairy", True, "2 lbs (907g)", False),
    ("cheese-slices-amul", "Cheese Slices (Processed)", "Amul", "fridge", "dairy", True, "", False),
    ("taco-cheese", "Cheddar & Asadero Taco Shredded Cheese", "Kraft", "fridge", "dairy", True, "bag", False),
    ("silken-tofu", "Silken Tofu (Lite Firm)", "Mori-Nu", "fridge", "dairy", True, "10.8 oz", False),
    ("milk-2pct", "2% Reduced Fat Milk", "Turner's", "fridge", "dairy", True, "jug", False),
    ("milk-1pct-uht", "1% Low Fat Milk (UHT)", "Schreiber", "fridge", "dairy", True, "carton", False),
    ("milk-1pct", "1% Low Fat Milk", "Marcel's Modern Pantry", "fridge", "dairy", True, "carton", False),

    # FRIDGE - Prepared/Fresh
    ("dosa-batter", "Dosa Batter (Vegan, GF)", "PRiyems", "fridge", "prepared", True, "1800g party size", False),
    ("ginger-root", "Fresh Ginger Root", "", "fridge", "produce", True, "whole pieces", False),
    ("coconut", "Whole Coconut", "", "fridge", "produce", True, "1", False),

    # FREEZER
    ("frozen-berry-medley", "Frozen Berry Medley (Strawberry, Blackberry, Blueberry, Raspberry)", "Giant Eagle", "freezer", "frozen", True, "12 oz", False),
    ("frozen-smoothie-mix", "Frozen Smoothie Mix (Dragon Fruit, Spinach, Kale)", "", "freezer", "frozen", True, "bag", False),
    ("frozen-green-beans", "Frozen Green Beans / Hari Mirch", "", "freezer", "frozen", True, "bag", False),
    ("paneer-paratha", "Paneer Paratha (Stuffed Flatbread)", "", "freezer", "frozen", True, "", False),
    ("naan-bread", "Naan Bread (Restaurant-Style, Frozen)", "", "freezer", "frozen", True, "", True),
    ("cascadian-farm-frozen", "Cascadian Farm Organic Frozen Item", "Cascadian Farm", "freezer", "frozen", True, "bag", False),
    ("frozen-mixed-vegetables", "Frozen Mixed Vegetables", "", "freezer", "frozen", True, "", False),

    # NOT IN INVENTORY — always-stock items that are currently out
    ("red-onions", "Red Onions", "", "produce", "produce", False, "", True),
    ("cruciferous-crunch", "Cruciferous Crunch", "Trader Joe's", "produce", "produce", False, "", True),
    ("frozen-cauliflower", "Frozen Cauliflower", "", "freezer", "frozen", False, "", True),
    ("black-beans-canned", "Black Beans (Canned)", "", "pantry", "canned", False, "", True),
    ("egg-whites", "Egg Whites", "", "fridge", "dairy", False, "", True),
]
# Fields: (slug, name, brand, location, category, have, qty, always_stock)

def write_ingredient(slug, name, brand, location, category, have, qty, always_stock):
    have_str = "true" if have else "false"
    stock_str = "true" if always_stock else "false"
    lines = [
        "---",
        f"name: \"{name}\"",
    ]
    if brand:
        lines.append(f"brand: \"{brand}\"")
    lines.append(f"location: {location}")
    lines.append(f"category: {category}")
    lines.append(f"have: {have_str}")
    if qty:
        lines.append(f"qty: \"{qty}\"")
    lines.append(f"always_stock: {stock_str}")
    lines.append("tags: [cooking/ingredient]")
    lines.append("---")
    lines.append("")

    path = os.path.join(INGREDIENTS_DIR, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path

# ── Recipes ──────────────────────────────────────────────────────────────────

RECIPES = [
    {
        "slug": "arepa-sweet-and-salty",
        "name": "Arepa Sweet and Salty Stack",
        "energy": "medium",
        "time": 25,
        "meal_time": "night",
        "ingredients": ["black-beans-canned", "zhoug-sauce", "dahi"],
        "needs_restock": ["cabbage-slaw", "paneer", "sweet-plantains", "plantain-chips"],
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
        "ingredients": ["naan-bread", "zhoug-sauce", "tzatziki"],
        "needs_restock": ["paneer", "red-onions", "peppers", "cucumber"],
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
        "ingredients": ["besan"],
        "needs_restock": ["cruciferous-crunch", "black-chana", "okra", "lemon", "chaat-masala", "sev"],
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
        "ingredients": ["taco-shells", "zhoug-sauce"],
        "needs_restock": ["black-beans-canned", "frozen-cauliflower", "red-onions", "cruciferous-crunch"],
        "components": {
            "base": "Taco Shells",
            "protein": "Black Beans (canned, drained)",
            "veggie": "Frozen Cauliflower + Red Onions",
            "sauce": "Zhoug (mixed into beans)",
            "crunch": "Cruciferous Crunch (on top)",
        },
        "how": "Sauté onion + cauliflower 5 min → add beans 2 min → stir in Zhoug → stuff shells. Add cheese/avo.",
    },
    {
        "slug": "falafel-power-bowl",
        "name": "Falafel Power Bowl",
        "energy": "low",
        "time": 10,
        "meal_time": "night",
        "ingredients": ["tzatziki"],
        "needs_restock": ["cruciferous-crunch", "falafel", "avocado", "tomatoes", "cucumber"],
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
        "ingredients": ["chickpeas-canned", "silken-tofu"],
        "needs_restock": ["brown-rice", "kale", "sweet-potatoes", "pesto", "lemon", "inca-corn", "pickled-onions"],
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
        "ingredients": ["zhoug-sauce"],
        "needs_restock": ["cruciferous-crunch", "black-chana", "samosas", "red-onions", "sev"],
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
        "ingredients": ["zhoug-sauce", "cheese-slices-amul"],
        "needs_restock": ["scallion-pancakes", "egg-whites", "red-onions", "cucumber"],
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
        "ingredients": [],
        "needs_restock": ["sourdough-bread", "egg-whites", "avocado", "tomatoes", "everything-seasoning"],
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
    # Build ingredient links
    have_links = [f"  - \"[[{s}]]\"" for s in r["ingredients"]]
    need_links = [f"  - \"[[{s}]]\"" for s in r["needs_restock"]]

    lines = [
        "---",
        f"name: \"{r['name']}\"",
        f"energy: {r['energy']}",
        f"time: {r['time']}",
        f"meal_time: {r['meal_time']}",
    ]

    if have_links:
        lines.append("ingredients:")
        lines.extend(have_links)
    else:
        lines.append("ingredients: []")

    if need_links:
        lines.append("needs_restock:")
        lines.extend(need_links)

    lines.append("tags: [cooking/recipe]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {r['name']}")
    lines.append("")
    lines.append("| Component | Ingredient |")
    lines.append("|-----------|-----------|")
    for comp, ing in r["components"].items():
        lines.append(f"| {comp.capitalize()} | {ing} |")

    if "how" in r:
        lines.append("")
        lines.append(f"**How:** {r['how']}")

    lines.append("")

    path = os.path.join(RECIPES_DIR, f"{r['slug']}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


# ── Execute ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Creating ingredient notes...")
    for args in INGREDIENTS:
        p = write_ingredient(*args)
        print(f"  ✓ {os.path.basename(p)}")

    print(f"\nCreated {len(INGREDIENTS)} ingredient notes in {INGREDIENTS_DIR}")

    print("\nCreating recipe notes...")
    for recipe in RECIPES:
        p = write_recipe(recipe)
        print(f"  ✓ {os.path.basename(p)}")

    print(f"\nCreated {len(RECIPES)} recipe notes in {RECIPES_DIR}")
    print("\nMigration complete!")
