
import sqlite3
import streamlit as st

# Set up the web page title and icon
st.set_page_config(page_title="Cruelty-Free Registry Search", page_icon="")
st.title(" Cruelty-Free Registry")
st.write("Search the registry to verify active certification status.")

# Create a text input box on the web page for the user
user_search = st.text_input("Enter brand name to search:", value="")

# Add a search button
if st.button("Search Registry") or user_search:
    # Connect to your existing SQLite database
    conn = sqlite3.connect('cruelty_free_registry.db')
    cursor = conn.cursor()

    # Use wildcards so partial typing works (e.g., typing "100" finds "100% Pure")
    search_term = f"%{user_search}%"

    query = '''
        SELECT certification_type, brand_name, is_certified
        FROM cruelty_free_brands
        WHERE brand_name LIKE :search_input
        ORDER BY certification_type ASC;
    '''
    
    cursor.execute(query, {"search_input": search_term})
    results = cursor.fetchall()
    conn.close()

    # Display the results cleanly on the page
    if results:
        st.subheader(f"Results for '{user_search}'")
        
        # Format the data into a clean, scannable interactive table on the web page
        table_data = []
        for row in results:
            table_data.append({
                "Certification Body": row[0],
                "Brand Name": row[1],
                "Officially Certified": row[2]
            })
            
        st.dataframe(table_data, use_container_width=True)
    else:
        st.warning(f"No brands matched '{user_search}'.")

