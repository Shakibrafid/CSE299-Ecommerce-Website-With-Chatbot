# Free Local Product Recommendation AI

This folder contains a no-cost, database-aware shopping assistant that reads the backend SQLite database directly and answers customer questions without relying on external APIs or paid AI services.

## Files

- `free_product_ai.py` — Local recommendation engine that reads products and categories from the Django database.

## Example usage

```bash
cd /workspaces/CSE299-Ecommerce-Website-With-Chatbot
python Chatbot/free_product_ai.py
```

Then ask questions like:

- "Recommend a good product under 5000 taka"
- "Compare wireless earbuds and smart watch"
- "Which product is best for fitness and comfort?"
- "I want something stylish and affordable"

The assistant checks the real backend database and gives advice based on product name, category, description, and price.
