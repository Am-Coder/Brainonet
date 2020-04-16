# from django.test import TestCase
import pytest
# Create your tests here.


@pytest.mark.django_db
def test_was_published_recently_with_old_question(client):
    assert 1 == 1