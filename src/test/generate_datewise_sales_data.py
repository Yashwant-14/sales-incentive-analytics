import os
import csv
import random
from datetime import datetime
from datetime import datetime, timedelta
from resources.dev import config

customer_ids = list(range(1001, 1051))  # 50 customers
store_ids = [301, 302, 303, 304, 305, 306]  # 6 stores

product_data = {
    "Aashirvaad Atta 10kg": 490,
    "Fortune Sunflower Oil 5L": 720,
    "Tata Salt 1kg": 28,
    "Parle-G Biscuits 800g": 60,
    "Nestle Maggi 560g": 95,
    "Colgate Toothpaste 200g": 98,
    "Dettol Soap 4x125g": 155,
    "Amul Butter 500g": 265,
    "Dove Shampoo 650ml": 390,
    "Pepsodent Toothbrush Pack of 4": 120,
    "Nescafe Classic Coffee 100g": 300,
    "Red Label Tea 500g": 180,
    "Kissan Mixed Fruit Jam 500g": 130,
    "Good Day Cookies 600g": 85,
    "Haldiram Bhujia 400g": 100,
    "Everest Red Chilli Powder 200g": 95,
    "MDH Garam Masala 100g": 75,
    "Surf Excel Detergent 1kg": 140,
    "Tide Washing Powder 1kg": 130,
    "Comfort Fabric Conditioner 800ml": 210,
    "Vim Dishwash Bar 3-pack": 55,
    "Lizol Floor Cleaner 1L": 170,
    "Harpic Toilet Cleaner 1L": 145,
    "Kellogg's Cornflakes 475g": 150,
    "Britannia Cheese Slices 200g": 130,
    "Mother Dairy Paneer 200g": 90,
    "Lays Chips 120g": 30,
    "Sprite Soft Drink 2L": 90,
    "Bisleri Water Bottle 2L": 25,
    "Real Mixed Fruit Juice 1L": 110
}

sales_persons = {
    301: [201, 202, 203],
    302: [204, 205, 206],
    303: [207, 208, 209],
    304: [210, 211, 212],
    305: [213, 214, 215],
    306: [216, 217, 218]
}



file_location = config.sales_data_to_s3

if not os.path.exists(file_location):
    os.makedirs(file_location)

input_date_str = input("Enter the date for which you want to generate (YYYY-MM-DD): ")
input_date = datetime.strptime(input_date_str, "%Y-%m-%d")

csv_file_path = os.path.join(file_location, f"sales_data_{input_date_str}.csv")
with open(csv_file_path, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["customer_id", "store_id", "product_name", "sales_date", "sales_person_id", "price", "quantity", "total_cost"])

    for _ in range(4000):
        customer_id = random.choice(customer_ids)
        store_id = random.choice(store_ids)
        product_name = random.choice(list(product_data.keys()))
        sales_date = input_date
        sales_person_id = random.choice(sales_persons[store_id])
        quantity = random.randint(1, 10)
        price = product_data[product_name]
        total_cost = price * quantity

        csvwriter.writerow(
            [customer_id, store_id, product_name, sales_date.strftime("%Y-%m-%d"), sales_person_id, price, quantity,
             total_cost])

    print("CSV file generated successfully.",csv_file_path)
