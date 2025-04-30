import streamlit as st
from classifier import classify_medical_note

st.set_page_config(page_title="MEDI-TAG", page_icon="🧠")

st.title("🏷️ MEDI-TAG")
st.subheader("Classify your medical notes into disease categories")

user_input = st.text_area("Enter a medical note or symptom description:")

if st.button("Classify"):
    if user_input.strip() == "":
        st.warning("Please enter something first.")
    else:
        label, confidence = classify_medical_note(user_input)
        st.success(f"Predicted: **{label}** ({confidence}%)")
