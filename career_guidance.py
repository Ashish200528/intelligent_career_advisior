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

def get_career_guidance(current_role="", experience_years="", skills="", interests=""):
    """Get career guidance based on user input"""
    try:
        if GENAI_AVAILABLE and (current_role or skills):
            return get_guidance_with_ai(current_role, experience_years, skills, interests)
        else:
            return generate_mock_guidance(current_role, experience_years, skills, interests)
    except Exception as e:
        print(f"[ERROR] Error getting career guidance: {str(e)}")
        return generate_mock_guidance(current_role, experience_years, skills, interests)

def get_guidance_with_ai(current_role, experience_years, skills, interests):
    """Get career guidance using AI"""
    try:
        prompt = f"""
        Provide career guidance for someone with:
        Current Role: {current_role}
        Experience: {experience_years} years
        Skills: {skills}
        Interests: {interests}
        
        Return a JSON object with the following structure:
        {{
            "skill_gap_analysis": ["Skill 1", "Skill 2", "Skill 3"],
            "skill_development_plan": ["Plan 1", "Plan 2", "Plan 3"],
            "certifications_courses": ["Course 1", "Course 2", "Course 3"],
            "project_ideas": ["Project 1", "Project 2", "Project 3"],
            "estimated_timeline": {{"total_estimated_time": "6-12 months"}},
            "job_readiness_indicator": "Ready/Needs improvement"
        }}
        
        Make the guidance specific to the role and skills mentioned.
        """
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"[ERROR] AI career guidance failed: {str(e)}")
        return generate_mock_guidance(current_role, experience_years, skills, interests)

def generate_mock_guidance(current_role, experience_years, skills, interests):
    """Generate mock career guidance when AI is not available"""
    
    # Skill gap analysis based on role
    skill_gaps = {
        "Software Engineer": ["Advanced algorithms", "System design", "Cloud architecture"],
        "Data Scientist": ["Machine learning", "Statistical analysis", "Big data tools"],
        "Product Manager": ["User research", "Data analysis", "Stakeholder management"],
        "DevOps Engineer": ["Container orchestration", "Infrastructure as code", "Monitoring tools"],
        "UI/UX Designer": ["User research", "Prototyping tools", "Design systems"]
    }
    
    # Development plans
    development_plans = [
        "Take online courses in relevant technologies",
        "Build portfolio projects to showcase skills",
        "Network with professionals in the field",
        "Attend industry conferences and workshops",
        "Contribute to open source projects"
    ]
    
    # Certifications and courses
    certifications = [
        "AWS Certified Solutions Architect",
        "Google Cloud Professional",
        "Microsoft Azure Developer",
        "Certified Scrum Master",
        "Professional certification in relevant field"
    ]
    
    # Project ideas
    project_ideas = [
        "Build a full-stack web application",
        "Create a mobile app with modern frameworks",
        "Develop a data analysis dashboard",
        "Contribute to an open source project",
        "Create a portfolio website"
    ]
    
    # Get role-specific gaps or use default
    gaps = skill_gaps.get(current_role, ["Technical skills", "Industry knowledge", "Practical experience"])
    
    # Randomize some elements for variety
    random.shuffle(development_plans)
    random.shuffle(certifications)
    random.shuffle(project_ideas)
    
    return {
        "skill_gap_analysis": gaps[:3],
        "skill_development_plan": development_plans[:3],
        "certifications_courses": certifications[:3],
        "project_ideas": project_ideas[:3],
        "estimated_timeline": {"total_estimated_time": "6-12 months depending on commitment"},
        "job_readiness_indicator": "Ready for entry-level positions, needs improvement for senior roles"
    }

if __name__ == "__main__":
    # Test the career guidance
    result = get_career_guidance("Software Engineer", "2", "Python, JavaScript", "Web development")
    print(json.dumps(result, indent=2))
