# Intelligent Career Advisor

A dynamic web application that provides AI-powered career guidance, resume analysis, job matching, and interview preparation. **Deployment-ready for Vercel with simplified authentication.**

## Features

- **Resume Parser**: Upload your resume and get instant feedback on its content and structure
- **Job Matcher**: Find the perfect job matches based on your skills and preferences
- **Career Guidance**: Get personalized career advice and development recommendations
- **Interview Preparation**: Practice common interview questions and get instant feedback
- **Interview Chatbot**: Practice interviews with our AI-powered chatbot

## Demo Credentials

For testing purposes, use these predefined credentials:
- **Email**: admin@careeradvisor.com
- **Password**: admin123

## Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/intelligent-career-advisor)

### Manual Deployment

1. **Fork/Clone this repository**
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Deploy automatically

3. **Environment Variables** (Optional):
   - `GEMINI_API_KEY`: Your Google Gemini API key for enhanced AI features
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)

## Local Development

### Prerequisites

- Python 3.8 or higher
- Google Generative AI API key (optional, for enhanced features)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/intelligent-career-advisor.git
   cd intelligent-career-advisor
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google Generative AI API key in `config.py` (optional):
   ```python
   GEMINI_API_KEY = "your-gemini-api-key"
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

- `app.py`: Main Flask application with routes
- `resume_parser.py`: Resume parsing functionality
- `job_matcher.py`: Job matching functionality
- `career_guidance.py`: Career guidance functionality
- `interview_prep.py`: Interview preparation functionality
- `interview_prep2.py`: Interview chatbot functionality
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `uploads/`: Directory for uploaded resumes
- `output/`: Directory for generated outputs
- `utils/`: Utility functions and helpers
- `config.py`: Configuration settings
- `vercel.json`: Vercel deployment configuration

## Technologies Used

- **Backend**: Flask, Python
- **AI Features**: Google Generative AI (Gemini) - Optional
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Animations**: Animate.css
- **Icons**: Font Awesome
- **Deployment**: Vercel

## Key Features

### Resume Parser
- Upload PDF resumes
- Extract skills, experience, and education
- Calculate resume score
- AI-powered analysis (when API key is available)

### Job Matcher
- Find relevant job opportunities
- Filter by location and skills
- AI-powered job recommendations
- Mock job listings when AI is unavailable

### Career Guidance
- Personalized career advice
- Skill gap analysis
- Development plans
- Certification recommendations
- Project ideas

### Interview Preparation
- Role-specific interview questions
- Technical and behavioral questions
- Answer tips and guidance
- Difficulty levels

### Interview Chatbot
- Interactive interview practice
- AI-powered responses
- Role-specific coaching
- Mock responses when AI is unavailable

## Deployment Notes

- **No Database Required**: Uses file-based storage and session management
- **Simplified Authentication**: Predefined credentials for demo purposes
- **Vercel Compatible**: Optimized for serverless deployment
- **Fallback Mode**: Works without AI API keys using mock data
- **Static File Handling**: Configured for Vercel's file system

## Troubleshooting

### Google Generative AI Package Not Available
If you see the warning about Google Generative AI package:
- The application will work in fallback mode with mock data
- To enable AI features, install: `pip install google-generativeai`
- Set your API key in `config.py`

### Vercel Deployment Issues
- Ensure all files are committed to your repository
- Check that `vercel.json` is in the root directory
- Verify Python version compatibility (3.8+)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The AI models used in this application use Google's Generative AI (Gemini)
- Frontend design inspired by modern web design principles
- Simplified for easy deployment and testing 