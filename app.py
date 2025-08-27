import os
from dotenv import load_dotenv
import streamlit as st
from prompts import greeting_prompt, info_prompts, fallback_prompt
from chatbot import configure_gemini, generate_tech_questions, check_exit, end_conversation
from utils import validate_email, validate_phone, save_candidate_data

# Setup Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
configure_gemini(API_KEY)

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("TalentScout Hiring Assistant 🤖")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate = {}
    st.session_state.conversation = [{"role": "assistant", "content": greeting_prompt()}]
    st.session_state.finished = False

for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if not st.session_state.finished:
    user_input = st.chat_input("Type here...")

    info_steps = ["name", "email", "phone", "experience", "position", "location", "stack"]
    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})

        if check_exit(user_input):
            st.session_state.conversation.append({"role": "assistant", "content": end_conversation()})
            st.session_state.finished = True
        else:
            step = st.session_state.step
            current_field = info_steps[step] if step < len(info_steps) else None

            valid = True
            if current_field == "email" and not validate_email(user_input):
                st.session_state.conversation.append({"role": "assistant", "content": "That doesn't look like a valid email address. Please try again."})
                valid = False
            if current_field == "phone" and not validate_phone(user_input):
                st.session_state.conversation.append({"role": "assistant", "content": "Phone number must be digits only, 7-15 characters."})
                valid = False

            if valid and current_field:
                st.session_state.candidate[current_field] = user_input
                st.session_state.step += 1
                if st.session_state.step < len(info_steps):
                    st.session_state.conversation.append({"role": "assistant", "content": info_prompts()[st.session_state.step]})
                else:
                    stack = st.session_state.candidate["stack"]
                    tech_questions = generate_tech_questions(stack)
                    questions_display = "\n".join(f"{i+1}. {q}" for i, q in enumerate(tech_questions))
                    st.session_state.candidate["questions"] = tech_questions
                    save_candidate_data(st.session_state.candidate)
                    st.session_state.conversation.append({"role": "assistant", "content": "Here are your tailored technical questions:"})
                    st.session_state.conversation.append({"role": "assistant", "content": questions_display})
                    st.session_state.conversation.append({"role": "assistant", "content": end_conversation()})
                    st.session_state.finished = True
            elif not valid:
                pass
            else:
                st.session_state.conversation.append({"role": "assistant", "content": fallback_prompt()})
