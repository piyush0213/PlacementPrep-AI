#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aeravat.settings')
django.setup()

from studentprofile.models import Quiz, Question, Choice, StudentProfile

# Create a sample quiz
quiz, created = Quiz.objects.get_or_create(
    id=2,
    defaults={
        'title': 'Frontend Development Quiz',
        'description': 'Test your knowledge of frontend development technologies'
    }
)

if created:
    print(f"Created quiz: {quiz.title}")
else:
    print(f"Quiz already exists: {quiz.title}")

# Create sample questions for the quiz
questions_data = [
    {
        'text': 'What does HTML stand for?',
        'topic': 'HTML',
        'choices': [
            ('HyperText Markup Language', True),
            ('High Tech Modern Language', False),
            ('Home Tool Markup Language', False),
            ('Hyperlink and Text Markup Language', False),
        ]
    },
    {
        'text': 'Which CSS property is used to change the text color?',
        'topic': 'CSS',
        'choices': [
            ('text-color', False),
            ('color', True),
            ('font-color', False),
            ('text-style', False),
        ]
    },
    {
        'text': 'What is JavaScript primarily used for?',
        'topic': 'JavaScript',
        'choices': [
            ('Styling web pages', False),
            ('Adding interactivity to web pages', True),
            ('Creating databases', False),
            ('Server-side programming only', False),
        ]
    }
]

for q_data in questions_data:
    question, created = Question.objects.get_or_create(
        quiz=quiz,
        text=q_data['text'],
        defaults={'topic': q_data['topic']}
    )
    
    if created:
        print(f"Created question: {question.text}")
        
        # Create choices for the question
        for choice_text, is_correct in q_data['choices']:
            Choice.objects.create(
                question=question,
                choice_text=choice_text,
                is_correct=is_correct
            )
            print(f"  Created choice: {choice_text} ({'correct' if is_correct else 'incorrect'})")
    else:
        print(f"Question already exists: {question.text}")

print("\nSample data created successfully!")
print("You can now access the quiz at: http://127.0.0.1:8000/quiz/2/")
