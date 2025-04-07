import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Share your opinion about FAIR")

# File to save responses
DATA_FILE = 'responses.csv'

# Load existing responses
if os.path.exists(DATA_FILE):
    responses_df = pd.read_csv(DATA_FILE)
else:
    responses_df = pd.DataFrame(columns=['order', 'message'])

# Input area
st.header("FAIR hierarchy")
input_order = st.text_input("Enter the letters of FAIR in hierarchical order, from the most to the least important (exactly 4 letters, e.g., IRAF):").upper()
message = st.text_area("Enter your message or explanation (optional):")

# Submit button
if st.button("Submit"):
    if set(input_order) == set('FAIR') and len(input_order) == 4:
        new_response = pd.DataFrame([{'order': input_order, 'message': message}])
        responses_df = pd.concat([responses_df, new_response], ignore_index=True)
        responses_df.to_csv(DATA_FILE, index=False)
        st.success(f"Recorded: {input_order}")
    else:
        st.error("Invalid input! Please enter exactly the letters F, A, I, R exactly once each.")

# Display current responses
if not responses_df.empty:
    st.header("Submitted Responses")

    # Extract first and last letters
    responses_df['first_letter'] = responses_df['order'].str[0]
    responses_df['last_letter'] = responses_df['order'].str[-1]

    # Frequency of first letters
    first_letter_freq = responses_df['first_letter'].value_counts().reset_index()
    first_letter_freq.columns = ['letter', 'count']

    # Frequency of last letters
    last_letter_freq = responses_df['last_letter'].value_counts().reset_index()
    last_letter_freq.columns = ['letter', 'count']

    # Plotting
    st.subheader("Most Frequent First Letter")
    fig_first = px.bar(first_letter_freq, x='letter', y='count', color='letter')
    st.plotly_chart(fig_first)

    st.subheader("Most Frequent Last Letter")
    fig_last = px.bar(last_letter_freq, x='letter', y='count', color='letter')
    st.plotly_chart(fig_last)

    # Interactive frequency table
    st.subheader("Detailed Response Frequency")
    response_freq = responses_df['order'].value_counts().reset_index()
    response_freq.columns = ['response', 'count']
    st.dataframe(response_freq, use_container_width=True)

    # Messages
    st.subheader("Messages and Explanations")
    st.dataframe(responses_df[['order', 'message']], use_container_width=True)

else:
    st.info("No responses yet. Submit your first entry!")