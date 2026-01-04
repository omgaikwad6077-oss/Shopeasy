import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed the database with 50+ sample products'

    def handle(self, *args, **kwargs):
        # Create or get categories
        categories_data = [
            {'name': 'Electronics', 'image': ''},
            {'name': 'Fashion', 'image': ''},
            {'name': 'Home & Kitchen', 'image': ''},
            {'name': 'Books', 'image': ''},
            {'name': 'Sports & Outdoors', 'image': ''},
            {'name': 'Beauty & Health', 'image': ''},
            {'name': 'Toys & Games', 'image': ''},
            {'name': 'Automotive', 'image': ''},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'image': cat_data['image']}
            )
            categories[cat_data['name']] = category
        
        # Sample products data with online image URLs
        products_data = [
            # Electronics (12 products)
            {
                'name': 'Apple iPhone 15 Pro',
                'category': 'Electronics',
                'price': 999.99,
                'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system.',
                'image_url': 'C:\Users\Sunny\shopeasy\seed_images\electronics\iphone-15-pro-max.png',
                'stock': 50
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'category': 'Electronics',
                'price': 1199.99,
                'description': 'Premium Android smartphone with S Pen, 200MP camera, and AI features.',
                'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 45
            },
            {
                'name': 'Sony WH-1000XM5 Wireless Headphones',
                'category': 'Electronics',
                'price': 349.99,
                'description': 'Industry-leading noise cancellation headphones with premium sound quality.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 100
            },
            {
                'name': 'MacBook Pro 16-inch M3',
                'category': 'Electronics',
                'price': 2499.99,
                'description': 'Professional laptop with M3 chip, Liquid Retina XDR display.',
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 30
            },
            {
                'name': 'Dell XPS 15 Laptop',
                'category': 'Electronics',
                'price': 1799.99,
                'description': 'Powerful Windows laptop with OLED display and latest Intel processor.',
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 40
            },
            {
                'name': 'iPad Pro 12.9-inch',
                'category': 'Electronics',
                'price': 1099.99,
                'description': 'Professional tablet with M2 chip and Liquid Retina XDR display.',
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 60
            },
            {
                'name': 'Sony PlayStation 5',
                'category': 'Electronics',
                'price': 499.99,
                'description': 'Next-gen gaming console with ultra-high speed SSD and 4K graphics.',
                'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 25
            },
            {
                'name': 'Nintendo Switch OLED',
                'category': 'Electronics',
                'price': 349.99,
                'description': 'Hybrid gaming console with vibrant OLED screen and enhanced audio.',
                'image_url': 'https://images.unsplash.com/photo-1607853202273-797f1c22a38e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 75
            },
            {
                'name': 'Apple Watch Series 9',
                'category': 'Electronics',
                'price': 399.99,
                'description': 'Advanced smartwatch with health monitoring and fitness tracking.',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 90
            },
            {
                'name': 'Samsung 4K Smart TV 65"',
                'category': 'Electronics',
                'price': 899.99,
                'description': 'Crystal 4K UHD TV with Quantum Processor and Smart Hub.',
                'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 35
            },
            {
                'name': 'Bose SoundLink Revolve+',
                'category': 'Electronics',
                'price': 329.99,
                'description': 'Portable Bluetooth speaker with 360-degree sound and waterproof design.',
                'image_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 120
            },
            {
                'name': 'GoPro HERO12 Black',
                'category': 'Electronics',
                'price': 399.99,
                'description': 'Action camera with 5.3K video, HyperSmooth stabilization.',
                'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 65
            },
            
            # Fashion (10 products)
            {
                'name': "Levi's 501 Original Jeans",
                'category': 'Fashion',
                'price': 89.99,
                'description': 'Classic straight fit jeans made with premium denim.',
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 200
            },
            {
                'name': 'Nike Air Max 270',
                'category': 'Fashion',
                'price': 149.99,
                'description': 'Comfortable sneakers with Max Air cushioning for all-day comfort.',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 150
            },
            {
                'name': 'North Face Winter Jacket',
                'category': 'Fashion',
                'price': 199.99,
                'description': 'Waterproof insulated jacket for extreme winter conditions.',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 80
            },
            {
                'name': 'Ray-Ban Aviator Sunglasses',
                'category': 'Fashion',
                'price': 159.99,
                'description': 'Classic aviator sunglasses with G-15 lenses.',
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 110
            },
            {
                'name': 'Michael Kors Handbag',
                'category': 'Fashion',
                'price': 299.99,
                'description': 'Designer leather handbag with gold-tone hardware.',
                'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 45
            },
            {
                'name': 'Rolex Submariner Watch',
                'category': 'Fashion',
                'price': 8999.99,
                'description': 'Luxury dive watch with ceramic bezel and automatic movement.',
                'image_url': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 10
            },
            {
                'name': 'Calvin Klein T-shirt Pack',
                'category': 'Fashion',
                'price': 49.99,
                'description': 'Pack of 3 classic cotton t-shirts in assorted colors.',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 300
            },
            {
                'name': 'Adidas Ultraboost 22',
                'category': 'Fashion',
                'price': 179.99,
                'description': 'Running shoes with responsive Boost cushioning.',
                'image_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 125
            },
            {
                'name': 'Gucci GG Belt',
                'category': 'Fashion',
                'price': 450.00,
                'description': 'Double G buckle leather belt in brown.',
                'image_url': 'https://images.unsplash.com/photo-1596703923338-48f1c07e4f2e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 25
            },
            {
                'name': 'North Face Backpack',
                'category': 'Fashion',
                'price': 89.99,
                'description': 'Durable backpack with laptop compartment and water bottle pockets.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 180
            },
            
            # Home & Kitchen (10 products)
            {
                'name': 'Ninja Foodi Air Fryer',
                'category': 'Home & Kitchen',
                'price': 199.99,
                'description': '8-in-1 air fryer that crisps, roasts, bakes, and dehydrates.',
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 85
            },
            {
                'name': 'KitchenAid Stand Mixer',
                'category': 'Home & Kitchen',
                'price': 449.99,
                'description': 'Professional 5-quart stand mixer with 10-speed settings.',
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 60
            },
            {
                'name': 'Dyson V15 Vacuum',
                'category': 'Home & Kitchen',
                'price': 699.99,
                'description': 'Cordless vacuum with laser detect technology.',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 40
            },
            {
                'name': 'Instant Pot Duo 8qt',
                'category': 'Home & Kitchen',
                'price': 129.99,
                'description': '7-in-1 programmable pressure cooker.',
                'image_url': 'https://images.unsplash.com/photo-1581093458797-4d87af5e63a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 95
            },
            {
                'name': 'Nespresso VertuoPlus',
                'category': 'Home & Kitchen',
                'price': 199.99,
                'description': 'Coffee maker with centrifusion technology for crema.',
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 110
            },
            {
                'name': 'Cuisinart Cookware Set',
                'category': 'Home & Kitchen',
                'price': 299.99,
                'description': '12-piece stainless steel cookware set.',
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 50
            },
            {
                'name': 'Philips Hue Smart Lights',
                'category': 'Home & Kitchen',
                'price': 199.99,
                'description': 'Smart LED bulb starter kit with bridge.',
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 200
            },
            {
                'name': 'Roomba i7+ Robot Vacuum',
                'category': 'Home & Kitchen',
                'price': 999.99,
                'description': 'Self-emptying robot vacuum with smart mapping.',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 30
            },
            {
                'name': 'Breville Barista Express',
                'category': 'Home & Kitchen',
                'price': 699.99,
                'description': 'Espresso machine with built-in grinder.',
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 35
            },
            {
                'name': 'Vitamix 5200 Blender',
                'category': 'Home & Kitchen',
                'price': 449.99,
                'description': 'Professional-grade blender for smoothies and soups.',
                'image_url': 'https://images.unsplash.com/photo-1550583727-b8b6c8877026?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 70
            },
            
            # Books (8 products)
            {
                'name': 'Atomic Habits by James Clear',
                'category': 'Books',
                'price': 16.99,
                'description': 'A proven framework for building good habits and breaking bad ones.',
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 500
            },
            {
                'name': 'The Hobbit by J.R.R. Tolkien',
                'category': 'Books',
                'price': 12.99,
                'description': 'Fantasy novel about Bilbo Baggins and his adventures.',
                'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 300
            },
            {
                'name': 'Python Crash Course',
                'category': 'Books',
                'price': 29.99,
                'description': 'Hands-on, project-based introduction to programming.',
                'image_url': 'https://images.unsplash.com/photo-1589998059171-988d887df646?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 250
            },
            {
                'name': 'Harry Potter Complete Collection',
                'category': 'Books',
                'price': 89.99,
                'description': 'All 7 books in the Harry Potter series in a collector\'s edition.',
                'image_url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 150
            },
            {
                'name': 'The Great Gatsby by F. Scott Fitzgerald',
                'category': 'Books',
                'price': 9.99,
                'description': 'Classic novel of the Jazz Age.',
                'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 400
            },
            {
                'name': 'To Kill a Mockingbird by Harper Lee',
                'category': 'Books',
                'price': 11.99,
                'description': 'Pulitzer Prize-winning novel about racial injustice.',
                'image_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 350
            },
            {
                'name': 'The Silent Patient by Alex Michaelides',
                'category': 'Books',
                'price': 15.99,
                'description': 'Psychological thriller about a woman who shoots her husband.',
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 200
            },
            {
                'name': 'The Alchemist by Paulo Coelho',
                'category': 'Books',
                'price': 13.99,
                'description': 'Philosophical book about following your dreams.',
                'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 450
            },
            
            # Sports & Outdoors (10 products)
            {
                'name': 'Wilson Evolution Basketball',
                'category': 'Sports & Outdoors',
                'price': 59.99,
                'description': 'Official game basketball with superior grip.',
                'image_url': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 120
            },
            {
                'name': 'Callaway Mavrik Driver',
                'category': 'Sports & Outdoors',
                'price': 499.99,
                'description': 'Premium golf driver with advanced face technology.',
                'image_url': 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 40
            },
            {
                'name': 'Yeti Tundra 45 Cooler',
                'category': 'Sports & Outdoors',
                'price': 299.99,
                'description': 'Roto-molded cooler with superior ice retention.',
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 65
            },
            {
                'name': 'Coleman Sundome Tent 4-Person',
                'category': 'Sports & Outdoors',
                'price': 89.99,
                'description': 'Weatherproof camping tent with easy setup.',
                'image_url': 'https://images.unsplash.com/photo-1504851149312-7a075b496cc7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 90
            },
            {
                'name': 'Hydro Flask 32oz Water Bottle',
                'category': 'Sports & Outdoors',
                'price': 44.99,
                'description': 'Insulated stainless steel water bottle.',
                'image_url': 'https://images.unsplash.com/photo-1523362628745-0c100150b504?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 300
            },
            {
                'name': 'Patagonia Nano Puff Jacket',
                'category': 'Sports & Outdoors',
                'price': 229.99,
                'description': 'Lightweight insulated jacket for outdoor activities.',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 75
            },
            {
                'name': 'Peloton Bike+',
                'category': 'Sports & Outdoors',
                'price': 2495.00,
                'description': 'Interactive exercise bike with rotating screen.',
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 20
            },
            {
                'name': 'Garmin Fenix 7 Watch',
                'category': 'Sports & Outdoors',
                'price': 699.99,
                'description': 'Multisport GPS watch with advanced training features.',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 55
            },
            {
                'name': 'Titleist Pro V1 Golf Balls',
                'category': 'Sports & Outdoors',
                'price': 49.99,
                'description': 'Premium golf balls with exceptional distance and control.',
                'image_url': 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 500
            },
            {
                'name': 'Specialized Allez Road Bike',
                'category': 'Sports & Outdoors',
                'price': 1199.99,
                'description': 'Entry-level road bike with lightweight aluminum frame.',
                'image_url': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 25
            }
        ]
        
        # Add more products to reach 50+
        additional_products = [
            # Beauty & Health (5 products)
            {
                'name': 'Dyson Supersonic Hair Dryer',
                'category': 'Beauty & Health',
                'price': 399.99,
                'description': 'Professional hair dryer with intelligent heat control.',
                'image_url': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 80
            },
            {
                'name': 'Philips Sonicare Electric Toothbrush',
                'category': 'Beauty & Health',
                'price': 129.99,
                'description': 'Premium electric toothbrush with smart sensor technology.',
                'image_url': 'https://images.unsplash.com/photo-1556228578-9c360e1d8d34?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 200
            },
            {
                'name': 'Foreo Luna 3 Facial Cleanser',
                'category': 'Beauty & Health',
                'price': 199.99,
                'description': 'Silicone facial cleansing brush with T-Sonic technology.',
                'image_url': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 95
            },
            {
                'name': 'NuFACE Trinity Facial Toning Device',
                'category': 'Beauty & Health',
                'price': 339.99,
                'description': 'Microcurrent facial toning device for lifted appearance.',
                'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 60
            },
            {
                'name': 'Theragun Elite Massage Device',
                'category': 'Beauty & Health',
                'price': 399.99,
                'description': 'Professional percussive therapy device for muscle recovery.',
                'image_url': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 45
            },
            
            # Automotive (5 products)
            {
                'name': 'Michelin Pilot Sport 4S Tires',
                'category': 'Automotive',
                'price': 299.99,
                'description': 'Ultra-high performance summer tires.',
                'image_url': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 150
            },
            {
                'name': 'Mobil 1 Synthetic Motor Oil',
                'category': 'Automotive',
                'price': 38.99,
                'description': 'Full synthetic motor oil for enhanced engine protection.',
                'image_url': 'https://images.unsplash.com/photo-1619546952812-520e98064a52?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 500
            },
            {
                'name': 'Bosch Wiper Blades Set',
                'category': 'Automotive',
                'price': 49.99,
                'description': 'Premium windshield wiper blades for all weather conditions.',
                'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 300
            },
            {
                'name': 'JBL Car Audio System',
                'category': 'Automotive',
                'price': 199.99,
                'description': 'Complete car audio speaker system with amplifier.',
                'image_url': 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 85
            },
            {
                'name': 'NOCO Boost Plus Jump Starter',
                'category': 'Automotive',
                'price': 99.99,
                'description': 'Portable lithium jump starter for dead car batteries.',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
                'stock': 120
            }
        ]
        
        # Combine all products
        all_products = products_data + additional_products
        
        # Create products
        created_count = 0
        for product_data in all_products:
            try:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': categories[product_data['category']],
                        'price': product_data['price'],
                        'description': product_data['description'],
                        'image': product_data['image_url'],
                        'stock': product_data['stock']
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(f"Created: {product_data['name']}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {product_data['name']}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} products!'))
        self.stdout.write(self.style.SUCCESS(f'Total products in database: {Product.objects.count()}'))