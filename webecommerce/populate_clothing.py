import os
import django
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webecommerce.settings') 
django.setup()

from store.models import Product, Category

def populate():
    #Create Clothing Categories
    categories_data = [
        ('T-Shirts', 't-shirts'),
        ('Sweatshirts', 'sweatshirts'),
        ('Hoodies', 'hoodies'),
        ('Oversized', 'oversized')
    ]
    
    cat_objs = {}
    for name, slug in categories_data:
        cat, created = Category.objects.get_or_create(name=name, slug=slug)
        cat_objs[name] = cat

    #Sample Clothing Data (Name, Description, Price, Category Name)
    clothing_items = [
        ("Classic White Tee", "100% Organic cotton, essential fit.", 25, "T-Shirts"),
        ("Midnight Black Shirt", "Premium heavy-weight cotton.", 30, "T-Shirts"),
        ("Vintage Graphic Tee", "90s inspired aesthetic print.", 35, "T-Shirts"),
        ("Urban Grey Sweatshirt", "Soft fleece lining for comfort.", 55, "Sweatshirts"),
        ("Navy Crewneck", "Classic athletic silhouette.", 50, "Sweatshirts"),
        ("Pastel Pink Crew", "Lightweight summer sweatshirt.", 45, "Sweatshirts"),
        ("Essential Black Hoodie", "Double-lined hood with kangaroo pocket.", 65, "Hoodies"),
        ("Forest Green Hoodie", "Earth-tone heavy fleece.", 70, "Hoodies"),
        ("Streetwear Oversized Tee", "Drop shoulder relaxed fit.", 40, "Oversized"),
        ("Boxy Fit Sweatshirt", "Modern cropped and wide cut.", 60, "Oversized"),
        ("Striped Long Sleeve", "Classic nautical style.", 38, "T-Shirts"),
        ("Logo Print Hoodie", "Minimalist brand embroidery.", 75, "Hoodies"),
        ("Acid Wash Sweatshirt", "Unique distressed look.", 65, "Sweatshirts"),
        ("Tie-Dye Summer Tee", "Hand-dyed vibrant patterns.", 32, "T-Shirts"),
        ("Techwear Zip Hoodie", "Water-resistant fabric.", 85, "Hoodies"),
        ("Minimalist Pocket Tee", "Simple design with functional pocket.", 28, "T-Shirts"),
        ("Cozy Sherpa Sweatshirt", "Maximum warmth for winter.", 90, "Sweatshirts"),
        ("Breezy Linen Shirt", "Perfect for tropical weather.", 45, "T-Shirts"),
        ("Distressed Oversized Hoodie", "Edge-cut streetwear style.", 78, "Oversized"),
        ("Sport Performance Tee", "Moisture-wicking fabric.", 30, "T-Shirts"),
    ]

    for name, desc, price, cat_name in clothing_items:
        Product.objects.get_or_create(
            name=name,
            description=desc,
            price=price,
            category=cat_objs[cat_name],
            stock=random.randint(10, 100)
        )
    print("Successfully added 20 Apparel products!")

if __name__ == '__main__':
    populate()