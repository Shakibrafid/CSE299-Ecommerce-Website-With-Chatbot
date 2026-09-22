import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Back" / "db.sqlite3"


def connect_db(db_path=None):
    db_path = Path(db_path or DB_PATH)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def clean_text(value):
    return (value or "").strip()


def find_products_by_query(conn, query):
    if not query:
        return []

    q = query.lower().strip()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT p.id, p.name, p.description, p.price, p.compare_price, c.name AS category_name
        FROM store_product p
        LEFT JOIN store_category c ON c.id = p.category_id
        WHERE p.is_active = 1
        ORDER BY p.price ASC
        """
    ).fetchall()

    if not rows:
        return []

    keywords = [token for token in re.split(r"[^a-z0-9]+", q) if token]
    matches = []
    for row in rows:
        haystack = " ".join([
            row["name"],
            row["category_name"] or "",
            row["description"] or "",
        ]).lower()
        score = 0
        for keyword in keywords:
            if keyword in haystack:
                score += 1
        if score:
            matches.append((score, row))

    matches.sort(key=lambda item: (-item[0], item[1]["price"]))
    results = [row for _, row in matches[:5]]
    if results:
        return results

    if any(word in q for word in ["budget", "cheap", "low cost", "affordable", "value"]):
        return [row for row in rows[:3]]

    return rows[:3]


def extract_budget(query):
    numbers = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", query or "")
    if not numbers:
        return None
    value = float(numbers[0].replace(",", ""))
    return value


def format_money(amount):
    return f"৳{float(amount):,.2f}"


def offer_general_advice(conn, query):
    products = conn.execute(
        """
        SELECT p.id, p.name, p.description, p.price, p.compare_price, c.name AS category_name
        FROM store_product p
        LEFT JOIN store_category c ON c.id = p.category_id
        WHERE p.is_active = 1
        ORDER BY p.price ASC
        """
    ).fetchall()

    budget = extract_budget(query)
    q = (query or "").lower()
    if any(word in q for word in ["fitness", "health", "exercise", "workout", "sport", "running"]):
        relevant = [row for row in products if "watch" in (row["name"] or "").lower() or "running" in (row["name"] or "").lower() or "mat" in (row["name"] or "").lower()]
    elif any(word in q for word in ["style", "fashion", "wear", "outfit", "bag", "jacket"]):
        relevant = [row for row in products if "jacket" in (row["name"] or "").lower() or "bag" in (row["name"] or "").lower()]
    elif any(word in q for word in ["work", "office", "desk", "home", "comfort", "chair"]):
        relevant = [row for row in products if "chair" in (row["name"] or "").lower() or "lamp" in (row["name"] or "").lower()]
    elif any(word in q for word in ["music", "pod", "travel", "phone", "audio"]):
        relevant = [row for row in products if "earbuds" in (row["name"] or "").lower()]
    else:
        relevant = products[:5]

    if budget:
        relevant = [row for row in relevant if float(row["price"]) <= budget + 5000]
        if not relevant:
            relevant = products[:3]

    top = relevant[:3]
    if not top:
        return "I could not find a matching product in the store right now. Please ask about categories like electronics, fashion, home, or sports."

    lines = [
        "Here are my best picks for your preferences:",
    ]
    for row in top:
        savings = ""
        if row["compare_price"]:
            savings = f" Save {format_money(float(row['compare_price']) - float(row['price']))}."
        lines.append(
            f"- {row['name']} ({row['category_name']}): {format_money(row['price'])}{savings} {row['description'] or 'Good value for the price.'}"
        )
    lines.append("If you want, I can compare two products directly or suggest the best option for your budget and use case.")
    return "\n".join(lines)


def compare_products(conn, product_names):
    if not product_names:
        return "Please mention the two product names you want to compare."

    rows = []
    for name in product_names:
        row = conn.execute(
            """
            SELECT p.id, p.name, p.description, p.price, p.compare_price, c.name AS category_name
            FROM store_product p
            LEFT JOIN store_category c ON c.id = p.category_id
            WHERE p.is_active = 1 AND LOWER(p.name) LIKE ?
            LIMIT 1
            """,
            (f"%{name.lower()}%",),
        ).fetchone()
        if row:
            rows.append(row)

    if len(rows) < 2:
        return "I found fewer than two matching products. Try names like Wireless Earbuds, Smart Watch, Running Shoes, or Leather Crossbody Bag."

    product_a, product_b = rows[0], rows[1]
    price_a = float(product_a["price"])
    price_b = float(product_b["price"])
    cheaper = product_a if price_a <= price_b else product_b
    smarter = product_a if product_a["compare_price"] and float(product_a["compare_price"]) > price_a else product_b

    return (
        f"Comparison: {product_a['name']} vs {product_b['name']}\n"
        f"- {product_a['name']}: {format_money(price_a)}; {product_a['description'] or 'Simple everyday value.'}\n"
        f"- {product_b['name']}: {format_money(price_b)}; {product_b['description'] or 'Strong everyday value.'}\n"
        f"Best value: {cheaper['name']} is cheaper.\n"
        f"Best overall fit for everyday shopping: {smarter['name']} gives a stronger deal on the current pricing."
    )


def answer_customer(question):
    conn = connect_db()
    text = clean_text(question)
    if not text:
        return "Please ask me about a product, a budget, or what you need to buy."

    lowered = text.lower()
    if "compare" in lowered:
        names = []
        for name in [
            "wireless earbuds",
            "smart watch",
            "classic denim jacket",
            "leather crossbody bag",
            "ergonomic office chair",
            "ambient table lamp",
            "running shoes",
            "yoga mat",
        ]:
            if name in lowered:
                names.append(name)
        if len(names) >= 2:
            return compare_products(conn, names)

    product_matches = find_products_by_query(conn, text)
    if product_matches and any(keyword in lowered for keyword in ["recommend", "best", "suggest", "need", "buy", "look for", "choose", "advice", "budget", "cheap", "good"]):
        top = product_matches[:3]
        lines = ["I recommend these products based on your request:"]
        for row in top:
            lines.append(f"- {row['name']} ({row['category_name']}): {format_money(row['price'])} — {row['description'] or 'Strong value for the category.'}")
        return "\n".join(lines)

    return offer_general_advice(conn, text)


if __name__ == "__main__":
    user_question = input("Ask the shopping assistant: ").strip()
    print("\nAI assistant:\n")
    print(answer_customer(user_question))
