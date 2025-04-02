import streamlit as st
import pandas as pd
import plotly.express as px

st.title("FAIR Hierarchical Ordering Visualization")

# Input area
st.header("Enter Ordered Letters")
input_order = st.text_input("Enter your hierarchical order of letters FAIR (exactly 4 letters, e.g., FAIR):").upper()
message = st.text_area("Enter your message or explanation (optional):")

# Initialize session state for responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Submit button
if st.button("Submit"):
    if set(input_order) == set('FAIR') and len(input_order) == 4:
        st.session_state.responses.append({'order': input_order, 'message': message})
        st.success(f"Recorded: {input_order}")
    else:
        st.error("Invalid input! Please enter exactly the letters F, A, I, R exactly once each.")

# Display current responses
if st.session_state.responses:
    st.header("Submitted Responses")
    df = pd.DataFrame(st.session_state.responses)

    # Extract first and last letters
    df['first_letter'] = df['order'].str[0]
    df['last_letter'] = df['order'].str[-1]

    # Frequency of first letters
    first_letter_freq = df['first_letter'].value_counts().reset_index()
    first_letter_freq.columns = ['letter', 'count']

    # Frequency of last letters
    last_letter_freq = df['last_letter'].value_counts().reset_index()
    last_letter_freq.columns = ['letter', 'count']

    # Plotting
    st.subheader("Most Frequent First Letter")
    fig_first = px.bar(first_letter_freq, x='letter', y='count', color='letter', title="Frequency of First Letters")
    st.plotly_chart(fig_first)

    st.subheader("Most Frequent Last Letter")
    fig_last = px.bar(last_letter_freq, x='letter', y='count', color='letter', title="Frequency of Last Letters")
    st.plotly_chart(fig_last)

    # Interactive frequency table
    st.subheader("Detailed Response Frequency")
    response_freq = df['order'].value_counts().reset_index()
    response_freq.columns = ['response', 'count']
    st.dataframe(response_freq, use_container_width=True)

    # Messages
    st.subheader("Messages and Explanations")
    st.dataframe(df[['order', 'message']], use_container_width=True)

else:
    st.info("No responses yet. Submit your first entry!")