import json
import random
from datetime import datetime, timedelta

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

def find_job_matches(job_position="", location="", skills=""):
    """Find job matches based on position, location, and skills"""
    try:
        if GENAI_AVAILABLE and job_position:
            return find_jobs_with_ai(job_position, location, skills)
        else:
            return generate_mock_jobs(job_position, location, skills)
    except Exception as e:
        print(f"[ERROR] Error finding job matches: {str(e)}")
        return generate_mock_jobs(job_position, location, skills)

def find_jobs_with_ai(job_position, location, skills):
    """Find jobs using AI"""
    try:
        prompt = f"""
        Search for job listings for the position: {job_position}
        Location: {location if location else 'Remote/Anywhere'}
        Skills: {skills if skills else 'General skills'}
        
        Return a JSON array of 5-8 job listings with the following structure:
        {{
            "jobs": [
                {{
                    "title": "Job Title",
                    "company": "Company Name",
                    "location": "Location",
                    "posted_date": "Recent date",
                    "description": "Short job description",
                    "url": "#"
                }}
            ]
        }}
        
        Make sure the jobs are relevant to the position and skills mentioned.
        """
        
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"[ERROR] AI job matching failed: {str(e)}")
        return generate_mock_jobs(job_position, location, skills)

def generate_mock_jobs(job_position, location, skills):
    """Generate mock job listings when AI is not available"""
    job_titles = [
        "Software Engineer", "Frontend Developer", "Backend Developer", 
        "Full Stack Developer", "Data Scientist", "DevOps Engineer",
        "Product Manager", "UI/UX Designer", "QA Engineer", "System Administrator"
    ]
    
    companies = [
        "TechCorp", "InnovateSoft", "Digital Solutions", "CloudTech", "DataFlow",
        "WebWorks", "AppStudio", "CodeCraft", "DevHub", "TechStart"
    ]
    
    locations = [
        "San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA",
        "Boston, MA", "Denver, CO", "Chicago, IL", "Remote", "Hybrid"
    ]
    
    descriptions = [
        "Join our dynamic team to build innovative solutions using cutting-edge technologies.",
        "We're looking for a passionate developer to help us scale our platform.",
        "Opportunity to work on exciting projects with modern tech stack.",
        "Help us transform the industry with your technical expertise.",
        "Collaborate with talented engineers in a fast-paced environment."
    ]
    
    # Generate 6-8 random jobs
    num_jobs = random.randint(6, 8)
    jobs = []
    
    for i in range(num_jobs):
        # Use provided job position or random one
        title = job_position if job_position else random.choice(job_titles)
        company = random.choice(companies)
        job_location = location if location else random.choice(locations)
        
        # Generate a recent date
        days_ago = random.randint(1, 30)
        posted_date = (datetime.now() - timedelta(days=days_ago)).strftime("%B %d, %Y")
        
        jobs.append({
            "title": title,
            "company": company,
            "location": job_location,
            "posted_date": posted_date,
            "description": random.choice(descriptions),
            "url": "#"
        })
    
    return {"jobs": jobs}

if __name__ == "__main__":
    # Test the job matcher
    result = find_job_matches("Software Engineer", "San Francisco", "Python, React")
    print(json.dumps(result, indent=2))
