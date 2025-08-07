import json
import random

# Try to import Google Generative AI package
GENAI_AVAILABLE = False
try:
    import google.generativeai as genai
    import config
    GENAI_AVAILABLE = True
    
    # Configure Gemini API if available
    if hasattr(config, 'GEMINI_API_KEY'):
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
except ImportError:
    print("[WARNING] Google Generative AI package not available. Using fallback mode.")

def chat_with_interview_bot(message, job_role="Software Engineer"):
    """Chat with the interview bot"""
    try:
        if GENAI_AVAILABLE:
            return chat_with_ai(message, job_role)
        else:
            return generate_mock_response(message, job_role)
    except Exception as e:
        print(f"[ERROR] Error in chatbot: {str(e)}")
        return generate_mock_response(message, job_role)

def chat_with_ai(message, job_role):
    """Chat with AI-powered interview bot"""
    try:
        prompt = f"""
        You are an AI interview coach for a {job_role} position. 
        The candidate says: "{message}"
        
        Provide a helpful, encouraging response that:
        1. Acknowledges their message
        2. Gives constructive feedback or advice
        3. Asks a relevant follow-up question
        4. Maintains a professional but friendly tone
        
        Keep your response under 150 words and be specific to the {job_role} role.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[ERROR] AI chatbot failed: {str(e)}")
        return generate_mock_response(message, job_role)

def generate_mock_response(message, job_role):
    """Generate mock responses when AI is not available"""
    
    # Common interview responses
    responses = {
        "hello": [
            "Hello! I'm your AI interview coach for the {role} position. How can I help you prepare today?",
            "Hi there! Ready to practice some interview questions for the {role} role? What would you like to work on?",
            "Welcome! I'm here to help you ace your {role} interview. What's on your mind?"
        ],
        "help": [
            "I can help you practice interview questions, give feedback on your answers, and provide tips for the {role} position. What would you like to focus on?",
            "I'm here to support your interview preparation for the {role} role. We can practice technical questions, behavioral questions, or general interview tips. What interests you?",
            "Let's work on your {role} interview skills! I can ask you questions, provide feedback, or give you specific tips. What would be most helpful?"
        ],
        "technical": [
            "Great! Let's practice some technical questions for the {role} position. Can you tell me about your experience with [relevant technology]?",
            "Technical skills are crucial for the {role} role. What's your strongest technical skill, and how would you demonstrate it in an interview?",
            "For the {role} position, technical questions often focus on problem-solving. How do you approach debugging a complex issue?"
        ],
        "behavioral": [
            "Behavioral questions are important for the {role} role. Can you tell me about a challenging project you worked on?",
            "Let's practice behavioral questions for the {role} position. How do you handle working with difficult team members?",
            "Behavioral questions help assess your soft skills for the {role} role. Tell me about a time you had to learn something quickly."
        ],
        "feedback": [
            "I'd be happy to give you feedback on your {role} interview preparation. What specific area would you like me to focus on?",
            "Feedback is crucial for improving your {role} interview skills. What aspect of your preparation would you like me to evaluate?",
            "Let's work on improving your {role} interview responses. What's a question you find challenging?"
        ]
    }
    
    # Determine response type based on message content
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey"]):
        response_type = "hello"
    elif any(word in message_lower for word in ["help", "what", "how"]):
        response_type = "help"
    elif any(word in message_lower for word in ["technical", "code", "programming", "technology"]):
        response_type = "technical"
    elif any(word in message_lower for word in ["behavioral", "experience", "situation", "story"]):
        response_type = "behavioral"
    elif any(word in message_lower for word in ["feedback", "improve", "better", "practice"]):
        response_type = "feedback"
    else:
        # Default response for other messages
        default_responses = [
            "That's an interesting point about the {role} role. Can you elaborate on that?",
            "Good question! For the {role} position, that's definitely something to consider. What's your take on it?",
            "I appreciate your input on the {role} role. How do you think that would apply in a real interview setting?",
            "That's a great perspective for the {role} position. What other aspects of the role are you thinking about?"
        ]
        return random.choice(default_responses).format(role=job_role)
    
    # Get appropriate responses and format with job role
    available_responses = responses.get(response_type, responses["help"])
    return random.choice(available_responses).format(role=job_role)

if __name__ == "__main__":
    # Test the chatbot
    response = chat_with_interview_bot("Hello, I'm preparing for a Software Engineer interview")
    print(response)
