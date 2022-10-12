import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, pub_date):
    q = Question(question_text=question_text, pub_date=pub_date)
    q.save()
    return q

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):

    def test_empty_choice_set_question_does_not_appear(self):
        """
        Questions with no choices are not displayed on the index page.
        """
        create_question("testing question", timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_non_empty_choice_set_question_appears(self):
        """
        Questions with choices are displayed on the index page.
        """
        test_question = create_question("testing question", timezone.now())
        test_question.choice_set.create(choice_text="choice1", votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [test_question])

    def test_empty_choice_set_and_non_empty_choice_set_questions(self):
        """
        Questions with choices are displayed on the index page, and those without
        are not.
        """
        test_question_with_choice = create_question("testing question", timezone.now())
        test_question_with_choice.choice_set.create(choice_text="choice1", votes=0)
        test_question_without_choice = create_question("testing question", timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                [test_question_with_choice],
                                )

    