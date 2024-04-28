import streamlit as st
import pandas as pd
import random

# Load the datasets
df = pd.read_csv("food.csv")  # Replace "input.csv" with the actual path to your dataset
substitute_df = pd.read_csv("food_substitutes.csv")  # Load the food substitutes dataset

# Function to calculate BMI
def calc_bmi(weight, height):
    return weight / ((height/100) ** 2)

# Function to calculate water intake
def calc_water_intake(activity_level, weight):
    water = 2000
    
    if activity_level == 'Low':
        water *= 1.0  # No adjustment
    elif activity_level == 'Moderate':
        water *= 1.1  # Increase by 10%
    elif activity_level == 'High':
        water *= 1.2  # Increase by 20%
    
    # rule of thumb: 30-35 ml/kg/day
    water += weight * 3.5
    
    return water

# Function to find substitutes for a given food item
def find_substitute(food_item):
    try:
        substitute = substitute_df[substitute_df['Food Item'].str.lower() == food_item.lower()]
        return substitute["Substitute"].values[0] if not substitute.empty else "Substitute not found"
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Main function to run the Streamlit app
def main():
    st.markdown("<h1 style='text-align: center;'>Daily Diet Planner</h1>", unsafe_allow_html=True)
    
    # Input fields layout
    col1, spacer, col2 = st.columns([2, 0.5, 2])

    with col1:
        # Personal Information
        st.subheader("Personal Information")
        age = st.number_input("Enter your age:", min_value=1, max_value=150, value=25)
        height = st.number_input("Enter your height (in cm):", min_value=50.0, max_value=300.0, value=170.0, step=0.1)
        weight = st.number_input("Enter your weight (in kg):", min_value=1.0, max_value=500.0, value=60.0, step=0.1)
    
    with col2:
        # Input fields for diet plan
        st.subheader("Goal and Activity Level")
        activity_level = st.selectbox("Select your activity level:", ["Low", "Moderate", "High"])
        weight_goal = st.selectbox("Select your weight goal:", ["Lose", "Gain", "Maintain"])

    # Calculate BMI
    bmi = calc_bmi(weight, height)
    st.write(f"<br><h5>Your BMI: {bmi:.2f}</h5>", unsafe_allow_html=True)
        
    # Water intake calculation
    water_intake = calc_water_intake(activity_level, weight)
    st.write(f"<h5>Recommended Daily Water Intake: {water_intake/1000:.2f} liters</h5>", unsafe_allow_html=True)

    # Allergy Input
    allergies = st.text_input("List any food allergies (comma-separated), or leave blank if none:")
    allergy_list = [allergy.strip().lower() for allergy in allergies.split(",")] if allergies else []

    # Filter the dataset based on activity level and weight goal
    filtered_df = df[(df["Activity Level"] == activity_level) & (df["Weight Goal"] == weight_goal)]

    # If there are allergies, remove the food items containing those allergies
    for allergy in allergy_list:
        filtered_df = filtered_df[~filtered_df["Meal Description"].str.lower().str.contains(allergy)]

    # Randomly select 2-3 items for breakfast, lunch, and dinner if the filtered DataFrame is not empty
    if not filtered_df.empty:
        breakfast_items = filtered_df[filtered_df["Meal Type"] == "Breakfast"].sample(n=random.randint(2, 3) if len(filtered_df) >= 2 else 1)
        lunch_items = filtered_df[filtered_df["Meal Type"] == "Lunch"].sample(n=random.randint(2, 3) if len(filtered_df) >= 2 else 1)
        dinner_items = filtered_df[filtered_df["Meal Type"] == "Dinner"].sample(n=random.randint(2, 3) if len(filtered_df) >= 2 else 1)
    else:
        # If the filtered DataFrame is empty, initialize empty DataFrames for breakfast, lunch, and dinner items
        breakfast_items = pd.DataFrame(columns=["Meal Description", "Calories"])
        lunch_items = pd.DataFrame(columns=["Meal Description", "Calories"])
        dinner_items = pd.DataFrame(columns=["Meal Description", "Calories"])

    # Include dietary preferences
    tea_preference = st.checkbox("Include a cup of tea in the meal plan")
    fruit_preference = st.text_input("Specify a fruit to include in the meal plan (e.g., Mango):")

  # Define calorie values for common fruits
    fruit_calories = {
        "Apple": 52,
        "Banana": 89,
        "Orange": 62,
        "Grapes": 69,
        "Strawberries": 32,
        "Mango": 60,
        "Pineapple": 50,
        "Watermelon": 30,
        "Peach": 59,
        "Pear": 57
    }

    fruit_calorie = 0
    if fruit_preference:
        # Add calorie count for selected fruit
        if fruit_preference in fruit_calories:
            fruit_calorie = fruit_calories[fruit_preference]
            st.write(f"{fruit_preference.capitalize()} (Calories: {fruit_calorie}) will be included in the meal plan.")


    # Generate diet plan
    st.subheader("Recommended Food Items:")
    
    # Display selected food items in a table format
    st.write("*Breakfast:*")
    
    breakfast_table = breakfast_items[["Meal Description", "Calories"]].reset_index(drop=True)
    if tea_preference:
        # Add calories for a cup of tea
        # tea_calories = 50  # Adjust calorie count as needed
        breakfast_table.loc[len(breakfast_table.index)] = ['Cup of tea', 150] 
        st.write("A cup of tea will be included in the meal plan.")
        # Add tea calories to the total calorie intake
        # total_calories += tea_calories
    breakfast_table.index += 1  # Start index from 1
    st.table(breakfast_table)
    
    st.write("*Lunch:*")
    lunch_table = lunch_items[["Meal Description", "Calories"]].reset_index(drop=True)
    lunch_table.index += 1  # Start index from 1
    st.table(lunch_table)
    
    st.write("*Dinner:*")
    dinner_table = dinner_items[["Meal Description", "Calories"]].reset_index(drop=True)
    dinner_table.index += 1  # Start index from 1
    st.table(dinner_table)

    # Calculate total calorie intake for all meals
    total_calories = breakfast_items["Calories"].sum() + lunch_items["Calories"].sum() + dinner_items["Calories"].sum()
    st.write("*Total Calorie Intake for the Day:*", total_calories+fruit_calorie)

    Repeat=st.checkbox("Regenerate")
    if Repeat=='True':
        main()
    
    # Find substitute for a given food item
    st.subheader("Find Food Item Substitute")
    food_item_input = st.text_input("Enter a food item to find its substitute:")
    if food_item_input:
        substitute = find_substitute(food_item_input)
        st.write(f"Substitute for {food_item_input}: {substitute}")

    # Repeat=st.checkbox("Repeat")
    # if Repeat=='True':
    #     main()



if __name__ == "__main__":
    main()