import sqlite3

# 1. Connect to database (creates the file if it doesn't exist)
conn = sqlite3.connect('cruelty_free_registry.db')
cursor = conn.cursor()

# 2. Create the table with your custom schema
# Note: We enforce a strict constraint on is_certified to only accept 'Yes' or 'No'
cursor.execute('''
CREATE TABLE IF NOT EXISTS cruelty_free_brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certification_type TEXT NOT NULL,  -- Leaping Bunny, PETA, etc.
    brand_name TEXT NOT NULL,
    is_certified TEXT CHECK(is_certified IN ('Yes', 'No')) NOT NULL
)
''')

# 3. Insert data from your audited list
# Applying your rule: 786 Cosmetics and 100% Pure are certified. 
# SkinLabo, OrganicaLibra, and Abbott do not hold active official certs, so they are marked 'No'.
audited_brands = [
    # Grouped by Certification Type to support your strict sorting logic
    ('Leaping Bunny', '786 Cosmetics', 'Yes'),
    ('Leaping Bunny', '100% Pure', 'Yes'),
    ('Leaping Bunny', 'SkinLabo', 'No'),
    ('Leaping Bunny', 'OrganicaLibra', 'No'),
    ('Leaping Bunny', '1121 Apothecary', 'No'),
    
    ('PETA', '82°E', 'Yes'),
    ('PETA', '3INA', 'Yes'),
    ('PETA', '12 Grabs', 'No'),
    ('PETA', '24K Cosmetics', 'No'),
    ('PETA', 'Abbott', 'No')
]

# Insert records cleanly
cursor.executemany('''
INSERT INTO cruelty_free_brands (certification_type, brand_name, is_certified)
VALUES (?, ?, ?)
''', audited_brands)

conn.commit()

# 4. Query data to verify the strict certification sorting
print("--- DATABASE EXPORT (Sorted Strictly by Certification) ---")
cursor.execute('''
    SELECT certification_type, brand_name, is_certified 
    FROM cruelty_free_brands 
    ORDER BY certification_type ASC, brand_name ASC
''')

for row in cursor.fetchall():
    print(f"Cert: {row[0]:<15} | Brand: {row[1]:<25} | Certified Status: {row[2]}")

conn.close()
-- This query looks for the brand and displays it based on its certification type


SELECT certification_type, brand_name, is_certified
FROM cruelty_free_brands
WHERE brand_name LIKE :user_search_input
ORDER BY certification_type ASC;
