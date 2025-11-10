# AI Study Assistant with ChatGPT Integration

A Python-based AI study assistant that helps students generate study materials, practice questions, and explanations using OpenAI's GPT API.

## Features

- **Ask Questions**: Get clear explanations of complex topics
- **Generate Flashcards**: Auto-create Q&A flashcards for memorization
- **Practice Problems**: Generate problems with step-by-step solutions
- **Study Summaries**: Create concise topic summaries
- **Practice Quizzes**: Generate multiple-choice quizzes
- **Study History**: Track all study sessions with SQLite database
- **Subject Organization**: Organize materials by subject

## Tech Stack

- **Backend**: Python Flask
- **AI**: OpenAI GPT-3.5-turbo API
- **Database**: SQLite
- **API Design**: RESTful architecture

## Installation

1. Clone the repository:
```bash
git clone https://github.com/an2thu/ai-study-assistant.git
cd ai-study-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get OpenAI API key:
- Sign up at https://platform.openai.com
- Create API key (you get $5 free credit)
- Add key to `app.py` line 14

4. Run the application:
```bash
python app.py
```

5. API is now available at `http://localhost:5000`

## API Endpoints

### Ask Study Question
```bash
POST /api/study
{
  "question": "Explain recursion in programming",
  "subject": "Computer Science"
}
```

### Generate Study Materials
```bash
POST /api/generate
{
  "topic": "Binary Search Trees",
  "type": "flashcards",  # or "practice", "summary", "quiz"
  "subject": "Data Structures"
}
```

### Get Study History
```bash
GET /api/history?subject=Programming&limit=10
```

### Get Study Statistics
```bash
GET /api/stats
```

## Study Material Types

- `explain` - Get clear explanation of concept
- `flashcards` - Generate 5 Q&A flashcards
- `practice` - Create 3 practice problems with solutions
- `summary` - Make concise study summary
- `quiz` - Generate 5-question multiple choice quiz

## Cost Management

- Uses GPT-3.5-turbo (cheaper than GPT-4)
- Token limits set to control costs
- Typical cost: $0.002 per question
- $5 credit = ~2,500 study questions

## Database Schema
```sql
study_sessions table:
- id (PRIMARY KEY)
- subject (TEXT)
- question (TEXT)
- answer (TEXT)
- session_type (TEXT)
- created_at (TIMESTAMP)
```

## Example Usage

**Generate Flashcards:**
```python
import requests

response = requests.post('http://localhost:5000/api/generate', json={
    'topic': 'SQL JOIN operations',
    'type': 'flashcards',
    'subject': 'Databases'
})

print(response.json()['content'])
```

**Ask Question:**
```python
response = requests.post('http://localhost:5000/api/study', json={
    'question': 'What is the difference between stack and queue?',
    'subject': 'Data Structures'
})

print(response.json()['answer'])
```

## Skills Demonstrated

- API integration (OpenAI)
- RESTful API design
- Database management (SQLite)
- Prompt engineering
- Backend development (Flask)
- Cost optimization strategies
- Error handling
- Data persistence

## Future Enhancements

- Add user authentication
- Implement conversation threading
- Add voice input/output
- Create web frontend interface
- Add spaced repetition system
- Export study materials to PDF
- Mobile app version

## Author

Ananthu Rajeev  
Information Technology Student, University of South Florida  
GitHub: https://github.com/an2thu  
LinkedIn: https://linkedin.com/in/ananthu-rajeev-a700341a5

## License

MIT License - feel free to use for your own studies!

## Disclaimer

Requires OpenAI API key. Free tier includes $5 credit. This is an educational project demonstrating AI integration.
