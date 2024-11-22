# 🥞Recipe Generation Using Gemini API 

This repository contains a **Recipe Generator App** that uses **Google Gemini API** to generate recipes based on user inputs such as cuisine type, dietary preferences, cooking time, and ingredients. The app also allows users to log in/register, generate recipes, and view their recipe history.

## ⚙️Features

- **User Authentication**: Login and registration functionality.
- **Recipe Generation**: Generate recipes based on user inputs such as ingredients, cuisine, dietary preferences, and cooking time.
- **Recipe History**: View a history of previously generated recipes linked to the user's account.
- **Database Integration**: Stores user recipe history in a SQLite database.

---

## 📋Prerequisites

1. Python 3.8 or higher installed.
2. `pip` (Python package installer).
3. Access to Google Gemini API (API Key required).

---

## 🛠️Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/recipe-generator.git
cd recipe-generator
```

### Step 2: Create and Activate a Virtual Environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### ✨Step 4: Set Up Environment Variables

1. Create a `.env` file in the project directory.
2. Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your Google Gemini API Key:

```
GOOGLE_GEMINI_KEY=YOUR_API_KEY
```

### Step 5: Run the App

```bash
streamlit run app.py
```

---

## How to Use

1. Open the app in your browser (Streamlit will provide a local URL after running the app).
2. Log in or register to create a new account.
3. Navigate through the app:
   - **Generate Recipe**: Enter your preferences and generate a custom recipe.
   - **Recipe History**: View all previously generated recipes.

---

## Acknowledgments

- [Google Gemini API](https://developers.generativeai.google.com/) for powering the recipe generation.
- [Streamlit](https://streamlit.io/) for creating the interactive app.
