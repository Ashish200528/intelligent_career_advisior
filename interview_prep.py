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

def get_interview_questions(job_role="", experience_level=""):
    """Get interview questions based on job role and experience level"""
    try:
        if GENAI_AVAILABLE and job_role:
            return get_questions_with_ai(job_role, experience_level)
        else:
            return generate_mock_questions(job_role, experience_level)
    except Exception as e:
        print(f"[ERROR] Error getting interview questions: {str(e)}")
        return generate_mock_questions(job_role, experience_level)

def get_questions_with_ai(job_role, experience_level):
    """Get interview questions using AI"""
    try:
        prompt = f"""
        Generate interview questions for a {job_role} position at {experience_level} level.
        
        Return a JSON object with the following structure:
        {{
            "interview_questions": [
                {{
                    "category": "Technical",
                    "questions": [
                        {{
                            "question": "Question text",
                            "tips": "Tips for answering",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ]
                }},
                {{
                    "category": "Behavioral",
                    "questions": [
                        {{
                            "question": "Question text",
                            "tips": "Tips for answering",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ]
                }}
            ]
        }}
        
        Include 3-5 questions per category, appropriate for the role and experience level.
        """
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"[ERROR] AI interview questions failed: {str(e)}")
        return generate_mock_questions(job_role, experience_level)

def generate_mock_questions(job_role, experience_level):
    """Generate mock interview questions when AI is not available"""
    
    # Question templates by role
    role_questions = {
        "Software Engineer": {
            "technical": [
                "Explain the difference between REST and GraphQL APIs.",
                "How would you optimize a slow database query?",
                "Describe the SOLID principles in object-oriented design.",
                "How do you handle version control in a team environment?",
                "Explain the concept of microservices architecture."
            ],
            "behavioral": [
                "Tell me about a challenging project you worked on.",
                "How do you handle disagreements with team members?",
                "Describe a time when you had to learn a new technology quickly.",
                "How do you prioritize tasks when working on multiple projects?",
                "Tell me about a bug you couldn't solve and how you handled it."
            ]
        },
        "Data Scientist": {
            "technical": [
                "Explain the difference between supervised and unsupervised learning.",
                "How would you handle missing data in a dataset?",
                "Describe the bias-variance tradeoff in machine learning.",
                "How do you evaluate the performance of a classification model?",
                "Explain the concept of overfitting and how to prevent it."
            ],
            "behavioral": [
                "Tell me about a data analysis project you're proud of.",
                "How do you communicate complex findings to non-technical stakeholders?",
                "Describe a time when your analysis led to a significant business impact.",
                "How do you stay updated with the latest ML/AI trends?",
                "Tell me about a time when you had to work with messy data."
            ]
        },
        "Product Manager": {
            "technical": [
                "How do you prioritize features in a product roadmap?",
                "Explain the difference between OKRs and KPIs.",
                "How would you conduct user research for a new feature?",
                "Describe your approach to A/B testing.",
                "How do you measure product success?"
            ],
            "behavioral": [
                "Tell me about a product you launched that failed and what you learned.",
                "How do you handle competing priorities from different stakeholders?",
                "Describe a time when you had to make a decision with incomplete data.",
                "How do you gather and incorporate user feedback?",
                "Tell me about a time when you had to say no to a feature request."
            ]
        }
    }
    
    # Get questions for the specific role or use default
    questions = role_questions.get(job_role, {
        "technical": [
            "Explain your technical background and experience.",
            "How do you approach problem-solving?",
            "Describe a project you worked on recently.",
            "How do you stay updated with technology trends?",
            "What tools and technologies are you most comfortable with?"
        ],
        "behavioral": [
            "Tell me about yourself and your background.",
            "Why are you interested in this position?",
            "Describe a challenging situation you faced at work.",
            "How do you handle stress and pressure?",
            "Where do you see yourself in 5 years?"
        ]
    })
    
    # Create structured response
    result = {
        "interview_questions": [
            {
                "category": "Technical",
                "questions": [
                    {
                        "question": question,
                        "tips": "Focus on your experience and provide specific examples.",
                        "difficulty": random.choice(["Easy", "Medium", "Hard"])
                    }
                    for question in questions["technical"][:4]  # Limit to 4 questions
                ]
            },
            {
                "category": "Behavioral",
                "questions": [
                    {
                        "question": question,
                        "tips": "Use the STAR method: Situation, Task, Action, Result.",
                        "difficulty": random.choice(["Easy", "Medium", "Hard"])
                    }
                    for question in questions["behavioral"][:4]  # Limit to 4 questions
                ]
            }
        ]
    }
    
    return result

if __name__ == "__main__":
    # Test the interview prep
    result = get_interview_questions("Software Engineer", "Mid-level")
    print(json.dumps(result, indent=2))
