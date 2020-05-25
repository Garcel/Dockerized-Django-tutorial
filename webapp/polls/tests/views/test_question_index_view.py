import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question, Choice
from .helper import create_question, set_up_user, set_up_super_user, create_question_without_choices

class QuestionIndexViewTests(TestCase):
    # Tests when user is not superuser or when it's an anonymous user
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_without_choices(self):
        """
        Questions without Choices aren't displayed on the index page.
        """
        set_up_user(self)
        self.assertFalse(self.user.is_superuser)

        create_question_without_choices(question_text="Question wihout Choices.", days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # Tests when user is a superuser
    def test_no_questions_for_admin(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question_for_admin(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question_for_admin(self):
        """
        Questions with a pub_date in the future are displayed on
        the index page for admins.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Future question.>']
        )

    def test_future_question_and_past_question_for_admin(self):
        """
        When both past and future questions exist then both questions
        are displayed for admins.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Future question.>', '<Question: Past question.>']
        )

    def test_two_past_questions_for_admin(self):
        """
        The questions index page may display multiple questions.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_without_choices_for_admin(self):
        """
        Questions without Choices are displayed on the index page for admins.
        """
        set_up_super_user(self)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_authenticated)

        create_question_without_choices(question_text="Question wihout Choices.", days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], 
            ['<Question: Question wihout Choices.>'])

