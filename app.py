import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 🏷️ Page Configuration
st.set_page_config(page_title="Calories & Macros Calculator", page_icon="🍱", layout="centered")

st.title("🍱 Calories & Macronutrients Calculator")
st.write("Track your food intake, calories, and macros easily using NumPy & Pandas!")

# Step 1: Food Database
food_data = {
    'Food': ['Rice', 'Apple', 'Egg', 'Chicken Breast', 'Milk', 'Bread', 'Banana'],
    'Calories_per_100g': [130, 52, 155, 165, 42, 265, 89],
    'Protein_per_100g': [2.7, 0.3, 13, 31, 3.4, 9, 1.1],
    'Carbs_per_100g': [28, 14, 1.1, 0, 5, 49, 23],
    'Fat_per_100g': [0.3, 0.2, 11, 3.6, 1, 3.2, 0.3]
}

food_df = pd.DataFrame(food_data)

# Step 2: User Input Section
st.subheader("🍽️ Enter your food intake (in grams):")

quantities = {}
for food in food_df['Food']:
    quantities[food] = st.number_input(f"{food} (g)", min_value=0, max_value=1000, value=0, step=10)

# Step 3: Merge data with user input
quantities_df = pd.DataFrame(list(quantities.items()), columns=['Food', 'Quantity_g'])
merged_df = pd.merge(food_df, quantities_df, on='Food')

# Step 4: Calculate nutrients
for col in ['Calories_per_100g', 'Protein_per_100g', 'Carbs_per_100g', 'Fat_per_100g']:
    nutrient = col.replace('_per_100g', '')
    merged_df[nutrient] = (merged_df[col] * merged_df['Quantity_g']) / 100

# Step 5: Totals
totals = {
    'Total Calories (kcal)': np.sum(merged_df['Calories']),
    'Total Protein (g)': np.sum(merged_df['Protein']),
    'Total Carbs (g)': np.sum(merged_df['Carbs']),
    'Total Fat (g)': np.sum(merged_df['Fat'])
}

# Step 6: Display results
if merged_df['Quantity_g'].sum() > 0:
    st.subheader("📊 Detailed Nutrient Breakdown")
    st.dataframe(merged_df[['Food', 'Quantity_g', 'Calories', 'Protein', 'Carbs', 'Fat']])

    st.subheader("🔥 Summary")
    for key, value in totals.items():
        st.write(f"**{key}:** {value:.2f}")

    # Step 7: Macronutrient Pie Chart
    st.subheader("🥧 Macronutrient Distribution")
    fig, ax = plt.subplots()
    labels = ['Protein', 'Carbs', 'Fat']
    values = [totals['Total Protein (g)'], totals['Total Carbs (g)'], totals['Total Fat (g)']]
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("👆 Enter quantities above to see your calorie breakdown.")
