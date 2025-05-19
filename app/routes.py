from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return "<h1>Welcome to the Product Catalog</h1>"

@main.route("/products")
def products():
    sample_products = ["Laptop", "Phone", "Tablet"]
    return "<br>".join(sample_products)