import os

# Directory paths - using relative paths for Vercel compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
INPUT_DIR = os.path.join(BASE_DIR, 'input')

# File paths
RESUME_PDF = os.path.join(INPUT_DIR, 'resume.pdf')
STRUCTURED_RESUME_JSON = os.path.join(OUTPUT_DIR, 'structured_resume.json')
JOB_MATCHES_JSON = os.path.join(OUTPUT_DIR, 'job_matches.json')
CAREER_GUIDANCE_JSON = os.path.join(OUTPUT_DIR, 'career_guidance.json')
INTERVIEW_PREP_JSON = os.path.join(OUTPUT_DIR, 'interview_prep.json')
CONVERSATION_JSON = os.path.join(OUTPUT_DIR, 'conversation.json')

# API Keys - Use environment variables for security
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Other configuration settings
MAX_JOBS_TO_RETURN = 10

# File paths for resume samples
RESUME_SAMPLES_DIR = os.path.join(BASE_DIR, "resume_samples")

# Create directories if they don't exist (only if not on Vercel)
if not os.environ.get('VERCEL'):
    os.makedirs(RESUME_SAMPLES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path for Sample_resume.pdf
SAMPLE_RESUME_PATH = os.path.join(RESUME_SAMPLES_DIR, "Sample_resume.pdf")

# Model configurations
RESUME_PARSER_MODEL = "gemini-2.0-flash"
JOB_MATCHER_MODEL = "gemini-2.5-pro-preview-03-25"
