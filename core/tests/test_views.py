# myapp/tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Organization, UserProfile
from django.test import Client

@pytest.fixture
def create_test_data():
    # Создание организаций
    org1 = Organization.objects.create(name='Organization 1')
    org2 = Organization.objects.create(name='Organization 2')

    # Создание пользователей
    user1 = User.objects.create_user(username='Александр', password='password')
    user2 = User.objects.create_user(username='Владислав', password='password')

    # Создание профилей пользователей
    UserProfile.objects.create(user=user1, organization=org1)
    UserProfile.objects.create(user=user2, organization=org2)

    return {
        'org1': org1,
        'org2': org2,
        'user1': user1,
        'user2': user2
    }

@pytest.mark.django_db
def test_organization_list_view(create_test_data):
    client = Client()
    user = create_test_data['user1']
    client.login(username='Александр', password='password')

    response = client.get(reverse('organization_list'))  # Предполагается, что вы используете имя URL 'organization_list'

    assert response.status_code == 200
    assert 'Organization 1' in response.content.decode()
    assert 'Organization 2' in response.content.decode()

@pytest.mark.django_db
def test_organization_detail_view(create_test_data):
    client = Client()
    user = create_test_data['user1']
    client.login(username='Александр', password='password')

    response = client.get(reverse('organization_detail', args=[create_test_data['org1'].id]))  # Предполагается, что вы используете имя URL 'organization_detail'

    assert response.status_code == 200
    assert 'Organization 1' in response.content.decode()
