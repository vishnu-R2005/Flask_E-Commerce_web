from app import db
from app.models import Product

def update_null_images():
    # Update all products with NULL or empty image fields
    products = Product.query.filter((Product.image == None) | (Product.image == '')).all()
    for product in products:
        product.image = 'uploads/placeholder.png'  # relative path inside /static/
        print(f"Updated product {product.id} with placeholder image")

    db.session.commit()
    print("All NULL product images updated!")

if __name__ == "__main__":
    update_null_images()
