from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as generativeai
import sqlite3

load_dotenv()

# Configuring our API key
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")
generativeai.configure(api_key=GOOGLE_GEMINI_KEY)

# Enhanced prompt for LLM
prompt = [
    """
    You are an expert in generating recipes based on various parameters such as cuisine, dietary preferences, cooking time, and ingredients.
    The recipe should include the following components: Title, Ingredients (list all ingredients clearly), Instructions (detailed step-by-step), and Cooking Time.
    """
]

# Function to get LLM response
def get_gemini_response(question, prompt):
    model = generativeai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Database setup
def init_db():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipe_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recipe TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_recipe_to_db(username, recipe):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT INTO recipe_history (username, recipe) VALUES (?, ?)', (username, recipe))
    conn.commit()
    conn.close()

def get_user_recipes_from_db(username):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT recipe FROM recipe_history WHERE username = ?', (username,))
    recipes = c.fetchall()
    conn.close()
    return [r[0] for r in recipes]

# Initialize the database
init_db()

# Streamlit App
st.set_page_config(page_title="Recipe Generator", layout="wide")
st.title("Recipe Generator")

# User authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Login/Register", "Generate Recipe", "Recipe History"])

# Login/Register Page
if page == "Login/Register":
    st.subheader("Login/Register")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type='password')

    if st.button("Login"):
        if username and password:  # Simple check; replace with actual authentication
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Please enter both username and password.")

    if st.button("Register"):
        if username and password:  # Simple registration logic
            st.success(f"User  {username} registered successfully!")
        else:
            st.error("Please enter both username and password.")

# Recipe Generation Page
elif page == "Generate Recipe":
    if st.session_state.authenticated:
        st.subheader("Generate a Recipe")
        col1, col2 = st.columns(2)
        with col1:
            cuisine = st.text_input("Cuisine (e.g., Italian, Indian, Chinese, Mexican):")
            diet = st.selectbox("Dietary Preference:", options=["Vegetarian", "Non-Vegetarian"])
        with col2:
            max_time = st.number_input("Max Cooking Time (in minutes):", min_value=1, max_value=180, value=30)
            ingredients = st.text_area("Ingredients (comma-separated):")

        submit = st.button("Generate Recipe")

        # If submit button is clicked
        if submit:
            # Construct the question based on user inputs
            question = f"Generate a {diet.lower()} {cuisine.lower()} recipe that takes less than {max_time} minutes with the following ingredients: {ingredients}."
            
            # Get recipe from LLM response
            response = get_gemini_response(question, prompt)
            st.subheader("Generated Recipe:")
            response_parts = response.split('\n')
            for part in response_parts:
                if part.startswith('Title:'):
                    st.write(f"**{part}**")
                elif part.startswith('Ingredients:'):
                    st.write(f"**{part}**")
                elif part.startswith('Instructions:'):
                    st.write(f"**{part}**")
                else:
                    st.write(part)  # Display the generated recipe

            # Save the generated recipe to database
            save_recipe_to_db(st.session_state.username, response)
    else:
        st.warning("Please log in to generate a recipe.")

# Recipe History Page
elif page == "Recipe History":
    if st.session_state.authenticated:
        st.subheader("Recipe History :")
        user_recipes = get_user_recipes_from_db(st.session_state.username)
        if user_recipes:
            for recipe in user_recipes:
                response_parts = recipe.split('\n')
                for part in response_parts:
                    if part.startswith('Title:'):
                        st.write(f"**{part}**")
                    elif part.startswith('Ingredients:'):
                        st.write(f"**{part}**")
                    elif part.startswith('Instructions:'):
                        st.write(f"**{part}**")
                    else:
                        st.write(part)
                st.write("---")
        else:
            st.write("No recipes found in history.")
    else:
        st.warning("Please log in to view your recipe history.")

# Logout
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.success("Logged out successfully!")