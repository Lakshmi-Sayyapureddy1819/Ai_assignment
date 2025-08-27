import google.generativeai as genai
from prompts import tech_stack_prompt, fallback_prompt

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def get_gemini_response(prompt_messages):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content(prompt_messages)  # prompt_messages is list of strings
    return response.text.strip()

def generate_tech_questions_gemini(stack):
    system_prompt = (
        "You are a helpful interviewer bot that generates relevant and clear technical interview questions. "
        "Generate 5 distinct questions tailored for the candidate's tech stack. "
        "Only list questions without explanations or apologies."
    )
    user_prompt = tech_stack_prompt(stack)

    prompt_messages = [system_prompt, user_prompt]
    print(f"DEBUG: Prompt messages to Gemini: {prompt_messages}")

    try:
        response_text = get_gemini_response(prompt_messages)
        print(f"DEBUG: Gemini API raw response:\n{response_text}")

        questions_list = [q.strip() for q in response_text.split('\n') if q.strip()]
        questions_list = [q for q in questions_list if "couldn't understand" not in q.lower()]
        return questions_list[:5]
    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        return [fallback_prompt()]

def check_exit(text):
    return text.lower().strip() in ['exit', 'quit', 'stop']
