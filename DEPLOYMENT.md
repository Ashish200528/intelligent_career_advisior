# Deployment Guide - Intelligent Career Advisor

This guide will help you deploy your career advisor application to Vercel with minimal complexity.

## 🚀 Quick Deploy (Recommended)

### Option 1: One-Click Deploy
1. Click the "Deploy with Vercel" button in the README
2. Connect your GitHub account
3. Import the repository
4. Deploy automatically

### Option 2: Manual Deploy
1. **Fork/Clone this repository** to your GitHub account
2. **Go to [vercel.com](https://vercel.com)** and sign up/login
3. **Click "New Project"**
4. **Import your repository** from GitHub
5. **Deploy** - Vercel will automatically detect it's a Python Flask app

## 📋 Pre-Deployment Checklist

✅ **Project Structure Verified:**
- `app.py` - Main Flask application (all modules imported)
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates (updated for simplified structure)
- `static/` - CSS/JS files

✅ **All Core Modules Included:**
- `resume_parser.py` - Resume parsing functionality
- `job_matcher.py` - Job matching functionality  
- `career_guidance.py` - Career guidance functionality
- `interview_prep.py` - Interview preparation
- `interview_prep2.py` - Interview chatbot

✅ **Authentication Simplified:**
- Predefined credentials: `admin@careeradvisor.com` / `admin123`
- No database required
- No email verification needed

✅ **Dependencies Updated:**
- Removed MySQL dependency
- Added Vercel-compatible packages
- Fallback mode for AI features

✅ **Templates Updated:**
- All form fields match simplified backend structure
- Career guidance form updated with proper fields
- Job matcher form includes location and skills fields
- Interview prep form includes experience level selection

## 🔧 Environment Variables (Optional)

For enhanced AI features, you can add these environment variables in Vercel:

1. **Go to your Vercel project dashboard**
2. **Navigate to Settings → Environment Variables**
3. **Add the following variables:**

```
GEMINI_API_KEY=your_google_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key (optional)
```

**⚠️ IMPORTANT**: Make sure you have removed any hardcoded API keys from `config.py`. The application now uses environment variables for security.

### Getting API Keys:
- **Google Gemini API**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI API**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)

## 🎯 Features Ready for Deployment

### ✅ Resume Parser
- Upload PDF resumes
- Extract skills, experience, education
- AI-powered analysis (with API key)
- Fallback to basic parsing
- **Form Fields**: File upload only

### ✅ Job Matcher
- Find relevant job opportunities
- Filter by position, location, skills
- AI-powered recommendations
- Mock job listings when AI unavailable
- **Form Fields**: Job Position, Location, Skills

### ✅ Career Guidance
- Personalized career advice
- Skill gap analysis
- Development plans
- Certification recommendations
- **Form Fields**: Current Role, Years of Experience, Skills, Career Interests

### ✅ Interview Preparation
- Role-specific questions
- Technical and behavioral categories
- Answer tips and guidance
- Difficulty levels
- **Form Fields**: Job Role, Experience Level (Entry/Mid/Senior/Lead)

### ✅ Interview Chatbot
- Interactive practice sessions
- AI-powered responses
- Role-specific coaching
- Mock responses when AI unavailable
- **Form Fields**: Message input, Job Role selection

## 🛠️ Local Testing

Before deploying, test locally:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd intelligent-career-advisor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser
# http://localhost:5000
```

**Test Credentials:**
- Email: `admin@careeradvisor.com`
- Password: `admin123`

## 📁 Project Structure

```
intelligent-career-advisor/
├── app.py                 # Main Flask application (all modules imported)
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── config.py            # Configuration settings
├── resume_parser.py     # Resume parsing functionality
├── job_matcher.py       # Job matching functionality
├── career_guidance.py   # Career guidance functionality
├── interview_prep.py    # Interview preparation
├── interview_prep2.py   # Interview chatbot
├── templates/           # HTML templates (updated)
│   ├── base.html
│   ├── login.html       # Shows demo credentials
│   ├── dashboard.html   # Static stats
│   ├── resume_parser.html
│   ├── job_matcher.html # Updated form fields
│   ├── career_guidance.html # Updated form fields
│   ├── interview_prep.html # Updated form fields
│   └── interview_chatbot.html
├── static/              # Static files (CSS, JS)
├── uploads/             # Upload directory
├── output/              # Output directory
└── utils/               # Utility functions
```

## 🔍 Troubleshooting

### Common Issues:

**1. Build Fails on Vercel**
- Check that `vercel.json` is in the root directory
- Ensure `requirements.txt` is present
- Verify Python version compatibility (3.8+)
- All core modules are properly included

**2. AI Features Not Working**
- Add your API keys as environment variables
- The app will work in fallback mode without API keys
- Check the console for error messages
- All modules have fallback mechanisms
- **IMPORTANT**: Remove any hardcoded API keys from config.py

**3. File Upload Issues**
- Vercel has limitations on file uploads
- Consider using external storage for production
- Current setup works for demo purposes

**4. Login Issues**
- Use the predefined credentials: `admin@careeradvisor.com` / `admin123`
- No registration required for demo

**5. Form Submission Issues**
- All templates updated to match simplified backend
- Form fields properly aligned with app.py routes
- No database dependencies in forms

**6. Serverless Function Crashes**
- Check for hardcoded API keys in config.py
- Ensure all environment variables are set in Vercel
- Verify no file system operations on Vercel
- Check Vercel logs for specific error messages

### Debugging Steps:

1. **Check Vercel Logs:**
   - Go to your Vercel dashboard
   - Click on your project
   - Navigate to "Functions" tab
   - Check for error messages

2. **Test API Keys:**
   - Verify your API keys are valid
   - Test locally with API keys first
   - Check environment variables in Vercel

3. **Verify Dependencies:**
   - All required packages are in `requirements.txt`
   - No MySQL dependencies (removed for Vercel compatibility)
   - All core modules are included and working

4. **Test All Features:**
   - Resume parser with PDF upload
   - Job matcher with position/location/skills
   - Career guidance with role/experience/skills/interests
   - Interview prep with role/experience level
   - Interview chatbot with message input

## 🎉 Post-Deployment

### What's Working:
- ✅ Simplified authentication (predefined credentials)
- ✅ Resume parsing (with/without AI, PDF upload)
- ✅ Job matching (with/without AI, multiple filters)
- ✅ Career guidance (with/without AI, comprehensive form)
- ✅ Interview preparation (with/without AI, experience levels)
- ✅ Interview chatbot (with/without AI, interactive)
- ✅ Responsive design
- ✅ Modern UI/UX
- ✅ All templates updated and functional

### Demo Features:
- Upload and parse resumes (PDF support)
- Find job matches (position, location, skills filters)
- Get career guidance (role, experience, skills, interests)
- Practice interview questions (role-specific, experience levels)
- Chat with AI interviewer (interactive practice)

## 📞 Support

If you encounter issues:

1. **Check the logs** in your Vercel dashboard
2. **Test locally** first to isolate issues
3. **Verify environment variables** are set correctly
4. **Check the README.md** for detailed setup instructions
5. **Verify all modules are included** and properly imported

## 🚀 Next Steps

After successful deployment:

1. **Customize the application** for your specific needs
2. **Add your own API keys** for enhanced AI features
3. **Modify the predefined credentials** for production use
4. **Add more features** as needed
5. **Optimize for performance** if required
6. **Test all features** with the updated form structures

---

**🎯 Your career advisor application is now ready for deployment to Vercel!**

The application has been simplified to work without complex database setups while maintaining all core features. All modules are properly included and working. Users can access the demo with the predefined credentials and explore all the career development tools with updated, user-friendly forms.
