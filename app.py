import os
from dotenv import load_dotenv
import streamlit as st
from prompts import greeting_prompt, info_prompts, fallback_prompt, end_prompt, tech_stack_prompt
from chatbot import configure_gemini, generate_tech_questions_gemini, check_exit
from utils import validate_email, validate_phone, save_candidate_data
from translation import detect_language, translate_to_english, translate_from_english

# Load Gemini API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
configure_gemini(API_KEY)

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("TalentScout Hiring Assistant 🤖")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate = {}
    st.session_state.conversation = [{"role": "assistant", "content": greeting_prompt()}]
    st.session_state.finished = False
    st.session_state.user_lang = "en"  # default English

# Show first input prompt after greeting automatically
if (
    len(st.session_state.conversation) == 1
    and st.session_state.conversation[0]["role"] == "assistant"
    and st.session_state.step == 0
):
    st.session_state.conversation.append({"role": "assistant", "content": info_prompts()[0]})

user_input = st.chat_input("Type your message here...")

if user_input:
    # Detect user language and translate input to English if needed
    user_lang = detect_language(user_input)
    st.session_state.user_lang = user_lang
    if user_lang != "en":
        user_input_en = translate_to_english(user_input)
    else:
        user_input_en = user_input

    # Append user original input to conversation
    st.session_state.conversation.append({"role": "user", "content": user_input})

    if check_exit(user_input_en):
        st.session_state.conversation.append({"role": "assistant", "content": end_prompt()})
        st.session_state.finished = True
    elif not st.session_state.finished:
        info_steps = ["name", "email", "phone", "experience", "position", "location", "stack"]
        step = st.session_state.step
        current_field = info_steps[step] if step < len(info_steps) else None

        valid = True
        if current_field == "email" and not validate_email(user_input_en):
            st.session_state.conversation.append({"role": "assistant", "content": "That doesn't look like a valid email address. Please try again."})
            valid = False
        if current_field == "phone" and not validate_phone(user_input_en):
            st.session_state.conversation.append({"role": "assistant", "content": "Phone number must be digits only, 7-15 characters. Please try again."})
            valid = False

        if valid and current_field:
            st.session_state.candidate[current_field] = user_input_en
            st.session_state.step += 1
            print(f"DEBUG: Collected field '{current_field}' with value: {user_input_en}")

            if st.session_state.step < len(info_steps):
                next_prompt = info_prompts()[st.session_state.step]
                # Translate prompt back to user language if needed
                if user_lang != "en":
                    next_prompt_translated = translate_from_english(next_prompt, user_lang)
                else:
                    next_prompt_translated = next_prompt
                st.session_state.conversation.append({"role": "assistant", "content": next_prompt_translated})
            else:
                stack = st.session_state.candidate.get("stack", "")
                print(f"DEBUG: Tech stack entered: '{stack}'")

                tech_questions = generate_tech_questions_gemini(stack)
                print(f"DEBUG: Generated tech questions: {tech_questions}")

                if not tech_questions or (len(tech_questions) == 1 and "couldn't understand" in tech_questions[0].lower()):
                    tech_questions = [fallback_prompt()]

                questions_display = "\n".join(f"{i+1}. {q}" for i, q in enumerate(tech_questions))
                st.session_state.candidate["questions"] = tech_questions
                save_candidate_data(st.session_state.candidate)

                # Translate questions display to user language if needed
                if user_lang != "en":
                    questions_display_translated = translate_from_english(questions_display, user_lang)
                    end_prompt_translated = translate_from_english(end_prompt(), user_lang)
                else:
                    questions_display_translated = questions_display
                    end_prompt_translated = end_prompt()

                st.session_state.conversation.append({"role": "assistant", "content": "Here are your tailored technical questions:"})
                st.session_state.conversation.append({"role": "assistant", "content": questions_display_translated})
                st.session_state.conversation.append({"role": "assistant", "content": end_prompt_translated})
                st.session_state.finished = True
        elif not valid:
            pass
        else:
            st.session_state.conversation.append({"role": "assistant", "content": fallback_prompt()})

# Display conversation messages
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

