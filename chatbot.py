import google.generativeai as genai
from prompts import tech_stack_prompt, fallback_prompt, end_prompt

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def get_gemini_response(prompt, model_name="gemini-pro"):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_tech_questions(stack):
    prompt = tech_stack_prompt(stack)
    try:
        questions = get_gemini_response(prompt)
        questions_list = [q.strip() for q in questions.split('\n') if q.strip()]
        return questions_list[:5]
    except Exception:
        return [fallback_prompt()]

def check_exit(input_text):
    return input_text.lower().strip() in ["exit", "quit", "stop"]

def end_conversation():
    return end_prompt()
