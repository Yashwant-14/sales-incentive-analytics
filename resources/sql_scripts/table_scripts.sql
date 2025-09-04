CREATE TABLE product_staging_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(1)
);


CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(255),
    pincode VARCHAR(10),
    phone_number VARCHAR(20),
    customer_joining_date DATE
);

-- Insert command for customer
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Saanvi', 'Krishna', 'Delhi', '122009', '9173121081', '2021-01-20');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Dhanush', 'Sahni', 'Delhi', '122009', '9155328165', '2022-03-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yasmin', 'Shan', 'Delhi', '122009', '9191478300', '2023-04-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vidur', 'Mammen', 'Delhi', '122009', '9119017511', '2020-10-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shamik', 'Doctor', 'Delhi', '122009', '9105180499', '2022-10-30');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Ryan', 'Dugar', 'Delhi', '122009', '9142616565', '2020-08-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Romil', 'Shanker', 'Delhi', '122009', '9129451313', '2021-10-29');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Krish', 'Tandon', 'Delhi', '122009', '9145683399', '2020-01-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Divij', 'Garde', 'Delhi', '122009', '9141984713', '2020-11-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Hunar', 'Tank', 'Delhi', '122009', '9169808085', '2023-01-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Zara', 'Dhaliwal', 'Delhi', '122009', '9129776379', '2023-06-13');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sumer', 'Mangal', 'Delhi', '122009', '9138607933', '2020-05-01');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Rhea', 'Chander', 'Delhi', '122009', '9103434731', '2023-08-09');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yuvaan', 'Bawa', 'Delhi', '122009', '9162077019', '2023-02-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sahil', 'Sabharwal', 'Delhi', '122009', '9174928780', '2021-03-16');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Tiya', 'Kashyap', 'Delhi', '122009', '9105126094', '2023-03-23');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kimaya', 'Lala', 'Delhi', '122009', '9115616831', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vardaniya', 'Jani', 'Delhi', '122009', '9125068977', '2022-07-19');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Indranil', 'Dutta', 'Delhi', '122009', '9120667755', '2023-07-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kavya', 'Sachar', 'Delhi', '122009', '9157628717', '2022-05-04');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Manjari', 'Sule', 'Delhi', '122009', '9112525501', '2023-02-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Akarsh', 'Kalla', 'Delhi', '122009', '9113226332', '2021-03-05');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Miraya', 'Soman', 'Delhi', '122009', '9111455455', '2023-07-06');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shalv', 'Chaudhary', 'Delhi', '122009', '9158099495', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Jhanvi', 'Bava', 'Delhi', '122009', '9110074097', '2022-07-14');


--store table
CREATE TABLE store (
    id INT PRIMARY KEY,
    address VARCHAR(255),
    store_pincode VARCHAR(10),
    store_manager_name VARCHAR(100),
    store_opening_date DATE,
    reviews TEXT
);

--data of store table
INSERT INTO store (id, address, store_pincode, store_manager_name, store_opening_date, reviews)
VALUES
    (301, 'Bengaluru', '560001', 'Ananya Sharma', '2021-03-12', 'Well-maintained store with excellent customer service.'),
    (302, 'Mumbai',    '400020', 'Arjun Mehta',   '2020-11-25', 'Wide range of products and quick checkout process.'),
    (303, 'Pune',      '411014', 'Rohan Deshpande','2022-07-18', 'Modern layout with a pleasant shopping experience.'),
    (304, 'Hyderabad', '500081', 'Sneha Reddy',   '2019-09-09', 'Helpful staff and good product availability.'),
    (305, 'Chennai',   '600042', 'Vikram Iyer',   '2023-02-28', 'Neatly organized sections and professional staff.'),
    (306, 'Kolkata',   '700016', 'Priya Sen',     '2021-06-05', 'Great ambience and reliable customer assistance.');


-- product table
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    current_price DECIMAL(10, 2),
    old_price DECIMAL(10, 2),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    expiry_date DATE
);


--product table data
INSERT INTO product (name, current_price, old_price, created_date, updated_date, expiry_date)
VALUES
    ('Aashirvaad Atta 10kg', 490, 490, '2022-02-15', NULL, '2025-12-31'),
    ('Fortune Sunflower Oil 5L', 720, 720, '2021-08-20', NULL, '2025-12-31'),
    ('Tata Salt 1kg', 28, 28, '2020-11-05', NULL, '2025-12-31'),
    ('Parle-G Biscuits 800g', 60, 60, '2023-03-12', NULL, '2025-12-31'),
    ('Nestle Maggi 560g', 95, 95, '2021-06-25', NULL, '2025-12-31'),
    ('Colgate Toothpaste 200g', 98, 98, '2022-09-10', NULL, '2025-12-31'),
    ('Dettol Soap 4x125g', 155, 155, '2020-07-19', NULL, '2025-12-31'),
    ('Amul Butter 500g', 265, 265, '2023-01-08', NULL, '2025-12-31'),
    ('Dove Shampoo 650ml', 390, 390, '2021-10-17', NULL, '2025-12-31'),
    ('Pepsodent Toothbrush Pack of 4', 120, 120, '2022-03-22', NULL, '2025-12-31'),
    ('Nescafe Classic Coffee 100g', 300, 300, '2020-05-11', NULL, '2025-12-31'),
    ('Red Label Tea 500g', 180, 180, '2021-12-09', NULL, '2025-12-31'),
    ('Kissan Mixed Fruit Jam 500g', 130, 130, '2023-06-30', NULL, '2025-12-31'),
    ('Good Day Cookies 600g', 85, 85, '2022-08-14', NULL, '2025-12-31'),
    ('Haldiram Bhujia 400g', 100, 100, '2020-04-27', NULL, '2025-12-31'),
    ('Everest Red Chilli Powder 200g', 95, 95, '2021-07-21', NULL, '2025-12-31'),
    ('MDH Garam Masala 100g', 75, 75, '2023-02-09', NULL, '2025-12-31'),
    ('Surf Excel Detergent 1kg', 140, 140, '2020-09-15', NULL, '2025-12-31'),
    ('Tide Washing Powder 1kg', 130, 130, '2022-05-19', NULL, '2025-12-31'),
    ('Comfort Fabric Conditioner 800ml', 210, 210, '2021-01-28', NULL, '2025-12-31'),
    ('Vim Dishwash Bar 3-pack', 55, 55, '2023-07-04', NULL, '2025-12-31'),
    ('Lizol Floor Cleaner 1L', 170, 170, '2020-10-23', NULL, '2025-12-31'),
    ('Harpic Toilet Cleaner 1L', 145, 145, '2022-04-11', NULL, '2025-12-31'),
    ('Kellogg''s Cornflakes 475g', 150, 150, '2021-03-02', NULL, '2025-12-31'),
    ('Britannia Cheese Slices 200g', 130, 130, '2023-09-10', NULL, '2025-12-31'),
    ('Mother Dairy Paneer 200g', 90, 90, '2020-06-18', NULL, '2025-12-31'),
    ('Lays Chips 120g', 30, 30, '2021-11-27', NULL, '2025-12-31'),
    ('Sprite Soft Drink 2L', 90, 90, '2022-07-13', NULL, '2025-12-31'),
    ('Bisleri Water Bottle 2L', 25, 25, '2020-08-04', NULL, '2025-12-31'),
    ('Real Mixed Fruit Juice 1L', 110, 110, '2021-09-29', NULL, '2025-12-31');



--sales team table
CREATE TABLE sales_team (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    manager_id INT,
    is_manager CHAR(1),
    address VARCHAR(255),
    pincode VARCHAR(10),
    joining_date DATE
);

-- Sales team data
INSERT INTO sales_team (id, first_name, last_name, manager_id, is_manager, address, pincode, joining_date) VALUES
-- Store 301 (Manager: Ananya Sharma, Employee IDs: 201,202,203)
(201, 'Ananya', 'Sharma', 201, 'Y', 'Bengaluru', '560001', '2021-03-12'),
(202, 'Ravi', 'Kumar', 201, 'N', 'Bengaluru', '560001', '2021-03-15'),
(203, 'Meena', 'Patil', 201, 'N', 'Bengaluru', '560001', '2021-03-18'),

-- Store 302 (Manager: Arjun Mehta, Employee IDs: 204,205,206)
(204, 'Arjun', 'Mehta', 204, 'Y', 'Mumbai', '400020', '2020-11-25'),
(205, 'Neha', 'Verma', 204, 'N', 'Mumbai', '400020', '2020-12-01'),
(206, 'Suresh', 'Rao', 204, 'N', 'Mumbai', '400020', '2020-12-05'),

-- Store 303 (Manager: Rohan Deshpande, Employee IDs: 207,208,209)
(207, 'Rohan', 'Deshpande', 207, 'Y', 'Pune', '411014', '2022-07-18'),
(208, 'Priya', 'Kulkarni', 207, 'N', 'Pune', '411014', '2022-07-22'),
(209, 'Amit', 'Joshi', 207, 'N', 'Pune', '411014', '2022-07-25'),

-- Store 304 (Manager: Sneha Reddy, Employee IDs: 210,211,212)
(210, 'Sneha', 'Reddy', 210, 'Y', 'Hyderabad', '500081', '2019-09-09'),
(211, 'Rajesh', 'Naidu', 210, 'N', 'Hyderabad', '500081', '2019-09-12'),
(212, 'Divya', 'Goud', 210, 'N', 'Hyderabad', '500081', '2019-09-15'),

-- Store 305 (Manager: Vikram Iyer, Employee IDs: 213,214,215)
(213, 'Vikram', 'Iyer', 213, 'Y', 'Chennai', '600042', '2023-02-28'),
(214, 'Lakshmi', 'Krishnan', 213, 'N', 'Chennai', '600042', '2023-03-03'),
(215, 'Arun', 'Nair', 213, 'N', 'Chennai', '600042', '2023-03-06'),

-- Store 306 (Manager: Priya Sen, Employee IDs: 216,217,218)
(216, 'Priya', 'Sen', 216, 'Y', 'Kolkata', '700016', '2021-06-05'),
(217, 'Kunal', 'Chatterjee', 216, 'N', 'Kolkata', '700016', '2021-06-08'),
(218, 'Shreya', 'Mukherjee', 216, 'N', 'Kolkata', '700016', '2021-06-12');






--s3 bucket table
CREATE TABLE s3_bucket_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bucket_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(20)
);


--s3 bucket data
INSERT INTO s3_bucket_info (bucket_name, status, created_date, updated_date)
VALUES ('de-project-01-data-pipeline-input', 'active', NOW(), NOW());


--Data Mart customer
CREATE TABLE customers_data_mart (
    customer_id INT ,
    full_name VARCHAR(100),
    address VARCHAR(200),
    phone_number VARCHAR(20),
    sales_date_month DATE,
    total_sales DECIMAL(10, 2)
);


--sales mart table
CREATE TABLE sales_team_data_mart (
    store_id INT,
    sales_person_id INT,
    full_name VARCHAR(255),
    sales_month VARCHAR(10),
    total_sales DECIMAL(10, 2),
    incentive DECIMAL(10, 2)
);