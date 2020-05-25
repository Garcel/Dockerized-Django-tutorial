import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Choice

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published) and with 
    a Choice.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    create_choice(question, 'dummy Choice')
    return question

def create_choice(question, choice_text):
    """
    Create a Choice with the given `choice_text` and for the given Question
    """
    return Choice.objects.create(question=question, choice_text=choice_text)

def create_question_without_choices(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published) but WITHOUT
    any Choices.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def set_up_user(view):
    # Create user
    view.username = 'dummy'
    view.password = 'secret'
    view.user = User.objects.create_user(view.username, 'dummy@example.com', view.password)

def set_up_super_user(view):
    # Create super user
    view.username = 'admin'
    view.password = 'secret'
    view.user = User.objects.create_superuser(view.username, 'admin@example.com', view.password)
    view.client.login(username=view.username, password=view.password)