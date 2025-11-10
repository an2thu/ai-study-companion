"""
AI Study Assistant with ChatGPT Integration
A simple Python application that helps students study using OpenAI's API
"""

from flask import Flask, render_template, request, jsonify
import openai
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)


openai.api_key = "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"  

DATABASE = 'study_assistant.db'

def init_db():
    """Initialize database for storing conversation history"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        session_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Study templates for different learning styles
STUDY_TEMPLATES = {
    "explain": "Explain the following concept in simple terms that a college student can understand: {topic}",
    
    "flashcards": "Create 5 flashcard-style questions and answers about: {topic}. Format each as Q: [question] A: [answer]",
    
    "practice": "Generate 3 practice problems about: {topic}. Include the answer and step-by-step solution for each.",
    
    "summary": "Create a concise study summary of the following topic with key points and important details: {topic}",
    
    "quiz": "Create a 5-question multiple choice quiz about: {topic}. Format: Question, then options A-D, then correct answer."
}

@app.route('/')
def index():
    """Main page"""
    return jsonify({
        'message': 'AI Study Assistant API',
        'endpoints': {
            '/api/study': 'POST - Ask study question',
            '/api/generate': 'POST - Generate study materials',
            '/api/history': 'GET - View study history',
            '/api/subjects': 'GET - Get studied subjects'
        }
    })

@app.route('/api/study', methods=['POST'])
def ask_study_question():
    """Ask a general study question"""
    data = request.json
    question = data.get('question', '')
    subject = data.get('subject', 'General')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cheaper than GPT-4
            messages=[
                {"role": "system", "content": "You are a helpful study assistant for college students. Provide clear, concise explanations."},
                {"role": "user", "content": question}
            ],
            max_tokens=500,  # Limit to control costs
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Save to database
        conn = get_db()
        conn.execute('''INSERT INTO study_sessions (subject, question, answer, session_type)
                       VALUES (?, ?, ?, ?)''',
                    (subject, question, answer, 'general'))
        conn.commit()
        conn.close()
        
        return jsonify({
            'question': question,
            'answer': answer,
            'subject': subject
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_study_material():
    """Generate specific study materials (flashcards, quizzes, etc.)"""
    data = request.json
    topic = data.get('topic', '')
    material_type = data.get('type', 'explain')  # explain, flashcards, practice, summary, quiz
    subject = data.get('subject', 'General')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    if material_type not in STUDY_TEMPLATES:
        return jsonify({'error': 'Invalid material type'}), 400
    
    try:
        # Create prompt from template
        prompt = STUDY_TEMPLATES[material_type].format(topic=topic)
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant creating study materials for college students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Save to database
        conn = get_db()
        conn.execute('''INSERT INTO study_sessions (subject, question, answer, session_type)
                       VALUES (?, ?, ?, ?)''',
                    (subject, topic, answer, material_type))
        conn.commit()
        conn.close()
        
        return jsonify({
            'topic': topic,
            'type': material_type,
            'content': answer,
            'subject': subject
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get study session history"""
    subject = request.args.get('subject')
    session_type = request.args.get('type')
    limit = request.args.get('limit', 20)
    
    conn = get_db()
    
    query = 'SELECT * FROM study_sessions WHERE 1=1'
    params = []
    
    if subject:
        query += ' AND subject = ?'
        params.append(subject)
    
    if session_type:
        query += ' AND session_type = ?'
        params.append(session_type)
    
    query += ' ORDER BY created_at DESC LIMIT ?'
    params.append(limit)
    
    sessions = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify([dict(s) for s in sessions])

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get list of subjects studied"""
    conn = get_db()
    
    subjects = conn.execute('''
        SELECT subject, COUNT(*) as count, MAX(created_at) as last_studied
        FROM study_sessions
        GROUP BY subject
        ORDER BY last_studied DESC
    ''').fetchall()
    
    conn.close()
    
    return jsonify([dict(s) for s in subjects])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get study statistics"""
    conn = get_db()
    
    # Total sessions
    total = conn.execute('SELECT COUNT(*) as count FROM study_sessions').fetchone()['count']
    
    # By type
    by_type = conn.execute('''
        SELECT session_type, COUNT(*) as count
        FROM study_sessions
        GROUP BY session_type
    ''').fetchall()
    
    # By subject
    by_subject = conn.execute('''
        SELECT subject, COUNT(*) as count
        FROM study_sessions
        GROUP BY subject
        ORDER BY count DESC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'total_sessions': total,
        'by_type': [dict(t) for t in by_type],
        'top_subjects': [dict(s) for s in by_subject]
    })

if __name__ == '__main__':
    init_db()
    print("AI Study Assistant is running!")
    print("Get your free OpenAI API key at: https://platform.openai.com")
    print("\nAvailable study types:")
    for key in STUDY_TEMPLATES.keys():
        print(f"  - {key}")
    print("\nStarting server on http://localhost:5000")
    app.run(debug=True, port=5000)
