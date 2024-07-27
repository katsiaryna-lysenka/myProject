import pytest
from django.contrib.auth.models import User
from core.models import Organization, UserProfile, Form1, Form2, Form3
import datetime

@pytest.fixture
def create_test_data():
    org1 = Organization.objects.create(name='Organization 1')
    org2 = Organization.objects.create(name='Organization 2')

    user1 = User.objects.create_user(username='Александр', password='password')
    user2 = User.objects.create_user(username='Владислав', password='password')

    profile1 = UserProfile.objects.create(user=user1, organization=org1)
    profile2 = UserProfile.objects.create(user=user2, organization=org2)

    form1_entries = [
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='направлен комиссией на основании', order=2,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='истечение срока обязательной отработки', order=4,
                             modified_by=user2),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='призыв на срочную службу', order=5,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='поступление в учреждения образования', order=6,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='переезд в другую местность', order=7,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='дискредитирующие обстоятельства', order=8,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='отсутствие жилья', order=9,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='неудовлетворенность выбранной профессией или специальностью', order=10,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='неудовлетворенность заработной платы', order=11,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='проблемы адаптации личности на рабочем месте', order=12,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='иные причины', order=13,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='Общая численность молодых специалистов(рабочих)', order=1,
                             modified_by=user1),
        Form1.objects.create(valid_until=datetime.date(2100, 1, 1),
                             article_name='Количество уволенных молодых специалистов', order=3,
                             modified_by=user1)
    ]

    form2_entries = [
        Form2.objects.create(start_date=datetime.date(2100, 1, 1), end_date=datetime.date(2100, 1, 31), organization=org1),
        Form2.objects.create(start_date=datetime.date(2100, 2, 1), end_date=datetime.date(2100, 2, 28), organization=org2),
    ]

    form3_entries = [
        Form3.objects.create(form1=form1_entries[0], form2=form2_entries[0], distribution_count=10, target_distribution_count=5, modified_by=user1),
        Form3.objects.create(form1=form1_entries[1], form2=form2_entries[1], distribution_count=20, target_distribution_count=15, modified_by=user2),
    ]

    return {
        'org1': org1,
        'org2': org2,
        'user1': user1,
        'user2': user2,
        'profile1': profile1,
        'profile2': profile2,
        'form1_entries': form1_entries,
        'form2_entries': form2_entries,
        'form3_entries': form3_entries
    }

def test_organization_creation(create_test_data):
    data = create_test_data
    assert Organization.objects.count() == 2
    assert data['org1'].name == 'Organization 1'
