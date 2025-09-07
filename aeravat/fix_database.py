#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aeravat.settings')
django.setup()

from studentprofile.models import StudentProfile
from django.contrib.auth.models import User

# Clean up duplicate StudentProfile records
print("Cleaning up duplicate StudentProfile records...")

# Get all StudentProfile records grouped by email
from django.db.models import Count
duplicates = StudentProfile.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)

for duplicate in duplicates:
    email = duplicate['email']
    profiles = StudentProfile.objects.filter(email=email).order_by('id')
    
    # Keep the first one, delete the rest
    keep_profile = profiles.first()
    delete_profiles = profiles[1:]
    
    print(f"Email: {email}")
    print(f"  Keeping profile ID: {keep_profile.id}")
    print(f"  Deleting {len(delete_profiles)} duplicate profiles")
    
    for profile in delete_profiles:
        print(f"    Deleting profile ID: {profile.id}")
        profile.delete()

print("\nDuplicate cleanup completed!")

# Create sample quiz data if it doesn't exist
from studentprofile.models import Quiz, Question, Choice

quiz, created = Quiz.objects.get_or_create(
    id=2,
    defaults={
        'title': 'Frontend Development Quiz',
        'description': 'Test your knowledge of frontend development technologies'
    }
)

if created:
    print(f"Created quiz: {quiz.title}")
    
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
        question = Question.objects.create(
            quiz=quiz,
            text=q_data['text'],
            topic=q_data['topic']
        )
        
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
    print(f"Quiz already exists: {quiz.title}")

print("\nSetup completed successfully!")
print("You can now access the quiz at: http://127.0.0.1:8000/quiz/2/")
