def greeting_prompt():
    return (
        "Hello! Welcome to TalentScout's Hiring Assistant. "
        "I'll collect some basic details, and then ask technical questions based on your chosen tech stack. "
        "Type 'exit' anytime to finish our chat."
    )

def info_prompts():
    return [
        "What is your Full Name?",
        "Please enter your Email Address.",
        "What is your Phone Number?",
        "How many years of professional experience do you have?",
        "What position(s) are you applying for?",
        "Where are you currently located?",
        "Please list your Tech Stack (languages, frameworks, databases, tools)."
    ]

def tech_stack_prompt(stack):
    return (
        f"Generate 3 to 5 technical interview questions on this candidate's tech stack: {stack}. "
        "Ask about applied skills, common pitfalls, and understanding of fundamentals. "
        "Only list the questions numbered 1-5."
    )

def fallback_prompt():
    return "Sorry, I couldn't understand that. Could you clarify or try again?"

def end_prompt():
    return "Thank you for your time! Your application has been received. We will contact you soon. Goodbye!"
