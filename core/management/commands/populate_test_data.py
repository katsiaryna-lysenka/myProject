from django.core.management.base import BaseCommand
from datetime import date

from core.models import Organization, UserProfile, Form1, Form2, Form3
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Create test organization
        Organization.objects.filter(name='Test Organization').delete()

        # Create test organization
        org = Organization.objects.create(name='Test Organization')

        # Check if user exists, if not create a new one
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(username='testuser', password='password')
        else:
            user = User.objects.get(username='testuser')

        # Create Form1 entries
        form1_entries = [
            {'valid_until': '2100-01-01', 'article_name': 'направлен комиссией на основании', 'order': 2, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'истечение срока обязательной отработки', 'order': 4, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'призыв на срочную службу', 'order': 5, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'поступление в учреждения образования', 'order': 6, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'переезд в другую местность', 'order': 7, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'дискредитирующие обстоятельства', 'order': 8, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'отсутствие жилья', 'order': 9, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'неудовлетворенность выбранной профессией или специальностью', 'order': 10, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'неудовлетворенность заработной платы', 'order': 11, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'проблемы адаптации личности на рабочем месте', 'order': 12, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'иные причины', 'order': 13, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'Общая численность молодых специалистов(рабочих)', 'order': 1, 'modified_by': user},
            {'valid_until': '2100-01-01', 'article_name': 'Количество уволенных молодых специалистов', 'order': 3, 'modified_by': user}
        ]

        for entry in form1_entries:
            Form1.objects.create(**entry)

        # Create Form2 entry
        form2 = Form2.objects.create(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            organization=org
        )

        # Create Form3 entries
        for form1 in Form1.objects.all():
            Form3.objects.create(
                form1=form1,
                form2=form2,
                distribution_count=10,
                target_distribution_count=5,
                modified_by=user
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))