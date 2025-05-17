import json
from models.product import Product
from models.cart import Cart

PRODUCTS_FILE = "products.json"


default_products = [
 Product("OOP Mastery eBook", "Master Object-Oriented Programming with real Python projects", 25.0),
Product("Next.js Portfolio Template", "Professional portfolio template built with Tailwind and Next.js", 20.0),
Product("Streamlit AI Dashboard", "Build your own AI-powered dashboard with Python and Streamlit", 18.0),
Product("Figma Template", "Modern, reusable Figma components for SaaS products and landing pages", 12.0),
Product("DevMart E-commerce Template", "Full e-commerce frontend in Next.js and Tailwind, inspired by this site", 22.0),
Product("Agentic AI Crash Course", "Learn how to build agent-based AI apps with Python and LangChain", 15.0),
Product("Python Game Source Code", "Download and learn from this fully playable Pygame-based platformer", 10.0),
Product("OOP Book", "Learn OOP in Python", 30.0),
Product("Agentic AI Course", "Course on autonomous intelligent agents using Python", 15.0)

]

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            data = json.load(f)
            return [Product.from_dict(p) for p in data]
    except FileNotFoundError:
        save_products(default_products)
        return default_products


def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump([p.to_dict() for p in products], f, indent=4)


products = load_products()

user_carts = {}
