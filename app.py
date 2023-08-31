import streamlit as st
import requests

def flask_endpoint():
    st.title("Welcome!")
    st.write("Run colab notebook and enter ngrok endpoint below")
    st.write('[Link for notebook ](https://colab.research.google.com/drive/12RwX-04JpNQJ1ApPGeS7IAg3QTPhl_z5?usp=sharing)')
    st.write("Enter the ngrok endpoint below:")
    
    st.session_state.flaskendpoint = st.text_input("Enter ngrok endpoint:", value=st.session_state.flaskendpoint if 'flaskendpoint' in st.session_state else "")
    
    if st.button("Continue"):
        st.session_state.page = "select_language"

def select_params():
    st.title("Select Language, Difficulty Level, and Number of Topics")

    st.session_state.language = st.text_input("Enter Language:", value=st.session_state.language if 'language' in st.session_state else "")
    st.session_state.difficulty = st.selectbox("Select Difficulty:", ["Basic", "Intermediate", "Advanced"], index=0 if 'difficulty' not in st.session_state else ["Basic", "Intermediate", "Advanced"].index(st.session_state.difficulty))
    st.session_state.num_topics = st.number_input("Number of Topics:", min_value=1, value=st.session_state.num_topics if 'num_topics' in st.session_state else 1)

    if st.button("Generate"):
        response = requests.post(
            st.session_state.flaskendpoint+"/generate_topics/",
            json={
                "language": st.session_state.language,
                "difficulty": st.session_state.difficulty,
                "num_topics": st.session_state.num_topics
            }
        )
        if response.status_code == 200:
            response_data = response.json()
            st.session_state.json_response = response_data
            st.session_state.reply = response_data['reply']  # Store the reply in session_state
        else:
            st.write('Error sending data to the server.')

    # Display the reply if it exists in session_state
    if 'reply' in st.session_state:
        st.write(st.session_state.reply)

            
def learn_concept():
    st.title("Learn Concept")
    
    st.session_state.concept = st.text_input("Enter concept name you want to learn:", value=st.session_state.concept if 'concept' in st.session_state else "")
    
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = False

    if 'user_code' not in st.session_state:
        st.session_state.user_code = ""

    if st.button("Generate"):

        response = requests.post(
            st.session_state.flaskendpoint+"/generate_question/",
            json={
                "language": st.session_state.language,
                "concept":st.session_state.concept,
            }
        )
        if response.status_code == 200:
            response_data = response.json()
            st.session_state.question=response_data['question']
            st.write(response_data['question'])
        else:
            st.write('Error sending data to the server.')
        
        
        st.session_state.user_code = st.text_area("Enter your code here:", value=st.session_state.user_code)

        if st.button('View Solution'):
            response = requests.post(
            st.session_state.flaskendpoint+"/generate_code/",
            json={
                "question": st.session_state.question
            }
        )
        if response.status_code == 200:
            response_data = response.json()
            st.write(response_data['code'])
        else:
            st.write('Error sending data to the server.')
        if st.button("Reset"):
            st.session_state.generate_clicked = False
            st.session_state.user_code = ""

    
def display_sidebar():
    st.sidebar.title("Menu")
    
    if st.sidebar.button("Welcome"):
        st.session_state.page = "welcome"
    if st.sidebar.button("Language & Difficulty"):
        st.session_state.page = "select_language"
    if st.sidebar.button("Learn Concept"):
        st.session_state.page = "learn_concept"


def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
        
    display_sidebar()

    # Check if 'page' exists in st.session_state before accessing it
    if 'page' in st.session_state:
        if st.session_state.page == "welcome":
            flask_endpoint()
        elif st.session_state.page == "select_language":
            select_params()
        elif st.session_state.page == "learn_concept":
            learn_concept()


if __name__ == "__main__":
    main()
