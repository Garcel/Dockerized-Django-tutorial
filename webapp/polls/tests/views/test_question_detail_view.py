import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Choice
from .helper import create_question, set_up_user, create_question_without_choices, set_up_super_user

class QuestionDetailViewTests(TestCase):
    # Tests when user is not superuser or when it's an anonymous user
    def test_no_question(self):
        """
        If question doesn't exist then returns a 404 not found.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        url = reverse('polls:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices(self):
        """
        The detail view of a question without Choices
        returns a 404 not found.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        question_no_choices = create_question_without_choices(question_text="Question wihout Choices.", days=-1)
        url = reverse('polls:detail', args=(question_no_choices.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Tests when user is a superuser
    def test_no_question_for_admin(self):
        """
        For admins, if question doesn't exist then returns a 404 not found.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)

        url = reverse('polls:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_for_admin(self):
        """
        For admins, the detail view of a question with a pub_date in the future
        returns a the question's text.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)

        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertContains(response, future_question.question_text)

    def test_past_question_for_admin(self):
        """
        For admins, the detail view of a question with a pub_date in the past
        displays the question's text.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)

        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_question_without_choices_for_admin(self):
        """
        For admins, the detailview of a question without Choices
        returns a 404 not found.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)

        question_no_choices = create_question_without_choices(question_text="Question wihout Choices.", days=-1)
        url = reverse('polls:detail', args=(question_no_choices.id,))
        response = self.client.get(url)
        self.assertContains(response, question_no_choices.question_text)
