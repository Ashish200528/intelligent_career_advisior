import fitz  # PyMuPDF
import json
import os
import re
from datetime import datetime
import random
import PyPDF2
import shutil

# Import from config and file_helpers if available
try:
    import config
    from utils.file_helpers import save_json_to_file, load_json_from_file
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Try to import Google Generative AI package
GENAI_AVAILABLE = False
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
    
    # Configure Gemini API if available
    if CONFIG_AVAILABLE and hasattr(config, 'GEMINI_API_KEY'):
        genai.configure(api_key=config.GEMINI_API_KEY)
        if hasattr(config, 'RESUME_PARSER_MODEL'):
            model = genai.GenerativeModel(model_name=config.RESUME_PARSER_MODEL)
        else:
            model = genai.GenerativeModel(model_name="gemini-2.0-flash")
except ImportError:
    print("[WARNING] Google Generative AI package not available. Using fallback mode.")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        print(f"[DEBUG] Opening file: {pdf_path}")
        if not os.path.exists(pdf_path):
            print(f"[ERROR] File does not exist at {pdf_path}")
            return None
        
        # Get file size
        file_size = os.path.getsize(pdf_path)
        print(f"[DEBUG] File size: {file_size} bytes")
        
        # Check if file is empty
        if file_size == 0:
            print("[ERROR] File is empty")
            return None
            
        # First try to read as a text file (some files might be text files with .pdf extension)
        try:
            with open(pdf_path, 'r', encoding='utf-8') as file:
                text = file.read()
                if text:
                    print(f"[INFO] Successfully read as text file: {len(text)} chars")
                    return text
        except UnicodeDecodeError:
            print("[DEBUG] Not a text file, continuing with PDF extraction")
        except Exception as e:
            print(f"[DEBUG] Error reading as text file: {str(e)}")
        
        # Try using PyMuPDF (fitz) first
        try:
            print("[DEBUG] Attempting to use PyMuPDF (fitz)")
            doc = fitz.open(pdf_path)
            print(f"[DEBUG] PDF opened successfully with PyMuPDF. Number of pages: {len(doc)}")
            
            text = ""
            for page_num, page in enumerate(doc, 1):
                print(f"[DEBUG] Processing page {page_num}...")
                page_text = page.get_text()
                text += page_text
                print(f"[DEBUG] Extracted {len(page_text)} characters from page {page_num}")
            
            doc.close()
            print(f"[DEBUG] Total text extracted with PyMuPDF: {len(text)} characters")
            
            if not text.strip():
                print("[WARNING] Extracted text is empty")
                return None
                
            return text
        except Exception as e:
            print(f"[WARNING] Error with PyMuPDF: {str(e)}, falling back to PyPDF2")
            
            # Fallback to PyPDF2
            try:
                print("[DEBUG] Attempting to use PyPDF2")
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        print(f"[DEBUG] Processing page {page_num+1} with PyPDF2...")
                        page_text = pdf_reader.pages[page_num].extract_text()
                        text += page_text
                        print(f"[DEBUG] Extracted {len(page_text)} characters from page {page_num+1}")
                    
                    print(f"[DEBUG] Total text extracted with PyPDF2: {len(text)} characters")
                    
                    if not text.strip():
                        print("[WARNING] Extracted text is empty")
                        return None
                        
                    return text
            except Exception as e:
                print(f"[ERROR] Error with PyPDF2: {str(e)}")
                return None
                
    except Exception as e:
        print(f"[ERROR] Error extracting text from PDF: {str(e)}")
        return None

def get_resume_prompt(resume_text):
    """Generate prompt for resume analysis"""
    prompt = f"""
    Analyze the following resume and extract structured information. Return the result as a JSON object with the following structure:
    
    {{
        "name": "Full Name",
        "email": "Email Address",
        "phone": "Phone Number",
        "summary": "Professional Summary",
        "skills": ["Skill 1", "Skill 2", "Skill 3"],
        "experience": [
            {{
                "job_role": "Job Title",
                "company": "Company Name",
                "duration": "Duration",
                "responsibilities": ["Responsibility 1", "Responsibility 2"]
            }}
        ],
        "education": [
            {{
                "degree": "Degree Name",
                "institution": "Institution Name",
                "years": "Year Range"
            }}
        ],
        "resume_score": 85
    }}
    
    Resume Text:
    {resume_text}
    
    Please analyze this resume and return only the JSON object.
    """
    return prompt

def parse_resume_file(file):
    """Parse resume from uploaded file"""
    try:
        # Save the uploaded file temporarily
        temp_path = os.path.join('uploads', 'temp_resume.pdf')
        os.makedirs('uploads', exist_ok=True)
        file.save(temp_path)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(temp_path)
        if not resume_text:
            return {"error": "Could not extract text from the uploaded file"}
        
        # Parse the resume using AI
        if GENAI_AVAILABLE:
            try:
                prompt = get_resume_prompt(resume_text)
                response = model.generate_content(prompt)
                result = json.loads(response.text)
                result['parsed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return result
            except Exception as e:
                print(f"[ERROR] AI parsing failed: {str(e)}")
                # Fallback to basic parsing
                return parse_resume_basic(resume_text)
        else:
            # Use basic parsing when AI is not available
            return parse_resume_basic(resume_text)
            
    except Exception as e:
        return {"error": f"Error processing resume: {str(e)}"}

def parse_resume_text(resume_text):
    """Parse resume from text"""
    try:
        if GENAI_AVAILABLE:
            try:
                prompt = get_resume_prompt(resume_text)
                response = model.generate_content(prompt)
                result = json.loads(response.text)
                result['parsed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return result
            except Exception as e:
                print(f"[ERROR] AI parsing failed: {str(e)}")
                return parse_resume_basic(resume_text)
        else:
            return parse_resume_basic(resume_text)
    except Exception as e:
        return {"error": f"Error processing resume: {str(e)}"}

def parse_resume_basic(resume_text):
    """Basic resume parsing without AI"""
    try:
        # Extract basic information using regex
        name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', resume_text)
        name = name_match.group(1) if name_match else "Not found"
        
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text)
        email = email_match.group(0) if email_match else "Not found"
        
        phone_match = re.search(r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})', resume_text)
        phone = phone_match.group(1) if phone_match else "Not found"
        
        # Extract skills (basic approach)
        skills = extract_skills(resume_text)
        
        # Extract experience
        experience = extract_experience(resume_text)
        
        # Extract education
        education = extract_education(resume_text)
        
        # Calculate score
        score = calculate_resume_score(skills, education, experience)
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "summary": "Professional summary extracted from resume",
            "skills": skills,
            "experience": experience,
            "education": education,
            "resume_score": score,
            "parsed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": f"Error in basic parsing: {str(e)}"}

def extract_skills(text):
    """Extract skills from resume text"""
    # Common technical skills
    technical_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
        'AWS', 'Docker', 'Kubernetes', 'Git', 'HTML', 'CSS', 'TypeScript',
        'Angular', 'Vue.js', 'PHP', 'C++', 'C#', '.NET', 'Ruby', 'Go',
        'Rust', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'TensorFlow',
        'PyTorch', 'Machine Learning', 'Data Science', 'DevOps', 'Agile'
    ]
    
    found_skills = []
    for skill in technical_skills:
        if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
            found_skills.append(skill)
    
    return found_skills[:10]  # Limit to 10 skills

def extract_education(text):
    """Extract education information"""
    education = []
    
    # Look for degree patterns
    degree_patterns = [
        r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.).*?(University|College|Institute)',
        r'(University|College|Institute).*?(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.)'
    ]
    
    for pattern in degree_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            education.append({
                "degree": match.group(0),
                "institution": "University/College",
                "years": "Not specified"
            })
    
    return education if education else [{"degree": "Not specified", "institution": "Not specified", "years": "Not specified"}]

def extract_experience(text):
    """Extract work experience"""
    experience = []
    
    # Look for job patterns
    job_patterns = [
        r'(Software Engineer|Developer|Programmer|Manager|Analyst|Consultant).*?(Company|Corp|Inc|LLC)',
        r'(Company|Corp|Inc|LLC).*?(Software Engineer|Developer|Programmer|Manager|Analyst|Consultant)'
    ]
    
    for pattern in job_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            experience.append({
                "job_role": match.group(1) if match.group(1) else "Not specified",
                "company": match.group(2) if match.group(2) else "Not specified",
                "duration": "Not specified",
                "responsibilities": ["Responsibility details not extracted"]
            })
    
    return experience if experience else [{"job_role": "Not specified", "company": "Not specified", "duration": "Not specified", "responsibilities": ["No experience found"]}]

def calculate_resume_score(skills, education, experience):
    """Calculate a basic resume score"""
    score = 50  # Base score
    
    # Add points for skills
    score += len(skills) * 2
    
    # Add points for education
    score += len(education) * 5
    
    # Add points for experience
    score += len(experience) * 10
    
    # Cap the score at 95
    return min(score, 95)
