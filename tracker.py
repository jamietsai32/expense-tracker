import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.title("Daily Expense Tracker 💰")
st.subheader("Add a new expense")

# inputs
amount = st.number_input("Enter an expense amount:", min_value=0.0, format="%.2f")
categories = ["Food", "Transport", "Shopping", "Entertainment", "Bills", "Other"]
category = st.selectbox("Select category:", categories)
date = st.date_input("Select date", date.today())
description = st.text_input("Enter expense description:")

if st.button("Add Expense"):
    new_expense = {
        "Date" : date,
        "Category" : category,
        "Amount" : amount,
        "Description" : description
    }
    try:
        df = pd.read_csv("expenses.csv")
        df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_expense])
    df.to_csv("expenses.csv", index=False)
    st.success("Expense added!")

st.subheader("Expense History 🧾")
if st.button("Clear history"):
    open("expenses.csv", "w").close()
    colums = ["Date", "Category", "Amount", "Description"]
    pd.DataFrame(columns=colums).to_csv("expenses.csv", index=False)
    st.success("Expense history cleared!")
try:
    df = pd.read_csv("expenses.csv")
    if df.empty:
        st.write("No expenses recorded yet.")
    else:
        st.dataframe(df)
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.write("No expenses recorded yet.")
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

if not df.empty:
    st.subheader("Expense Summary 📊")
    st.write("Choose a category to filter:")
    filter_options = categories + ["Day", "Month", "Year"]
    selected_category = st.selectbox("Select Category", filter_options)
    filtered_data = df[df["Category"] == selected_category]
    if filtered_data.empty:
        st.write("No expenses found for this category.")
    else:
        st.dataframe(filtered_data)
        total_expense = filtered_data["Amount"].sum()
        st.write(f"Total expense in {selected_category}: ${total_expense:.2f}")