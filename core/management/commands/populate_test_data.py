from django.core.management.base import BaseCommand
from datetime import date

from django.db import IntegrityError
from django.utils.dateparse import parse_date

from core.models import Organization, UserProfile, Form1, Form2, Form3, SpecialistDismissalReport
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):

        try:
            Form1.objects.all().delete()
            Form2.objects.all().delete()
            Form3.objects.all().delete()
            SpecialistDismissalReport.objects.all().delete()
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error while deleting data: {e}'))
            return
        org, created = Organization.objects.get_or_create(name='Test Organization')

        user, created = User.objects.get_or_create(username='testuser', defaults={'password': 'password'})
        if created:
            user.set_password('password')
            user.save()

        form1_entries = [
            {'id': 1, 'valid_until': '2100-01-01', 'article_name': 'направлен комиссией на основании', 'order': 2,
             'modified_by': user},
            {'id': 2, 'valid_until': '2100-01-01', 'article_name': 'истечение срока обязательной отработки', 'order': 4,
             'modified_by': user},
            {'id': 3, 'valid_until': '2100-01-01', 'article_name': 'призыв на срочную службу', 'order': 5,
             'modified_by': user},
            {'id': 4, 'valid_until': '2100-01-01', 'article_name': 'поступление в учреждения образования', 'order': 6,
             'modified_by': user},
            {'id': 5, 'valid_until': '2100-01-01', 'article_name': 'переезд в другую местность', 'order': 7,
             'modified_by': user},
            {'id': 6, 'valid_until': '2100-01-01', 'article_name': 'дискредитирующие обстоятельства', 'order': 8,
             'modified_by': user},
            {'id': 7, 'valid_until': '2100-01-01', 'article_name': 'отсутствие жилья', 'order': 9, 'modified_by': user},
            {'id': 8, 'valid_until': '2100-01-01',
             'article_name': 'неудовлетворенность выбранной профессией или специальностью', 'order': 10,
             'modified_by': user},
            {'id': 9, 'valid_until': '2100-01-01', 'article_name': 'неудовлетворенность заработной платы', 'order': 11,
             'modified_by': user},
            {'id': 10, 'valid_until': '2100-01-01', 'article_name': 'проблемы адаптации личности на рабочем месте',
             'order': 12, 'modified_by': user},
            {'id': 11, 'valid_until': '2100-01-01', 'article_name': 'иные причины', 'order': 13, 'modified_by': user},
            {'id': 12, 'valid_until': '2100-01-01', 'article_name': 'Общая численность молодых специалистов(рабочих)',
             'order': 1, 'modified_by': user},
            {'id': 13, 'valid_until': '2100-01-01', 'article_name': 'Количество уволенных молодых специалистов',
             'order': 3, 'modified_by': user}
        ]

        form1_objects = {}
        for entry in form1_entries:
            form1 = Form1.objects.create(**entry)
            form1_objects[entry['id']] = form1

        form2, created = Form2.objects.get_or_create(
            start_date=parse_date('2024-01-01'),
            end_date=parse_date('2024-01-31'),
            organization=org
        )

        form3_entries = [
            {'form1': form1_objects[1], 'form2': form2, 'distribution_count': 10, 'target_distribution_count': 5,
             'modified_by': user},
            {'form1': form1_objects[2], 'form2': form2, 'distribution_count': 8, 'target_distribution_count': 3,
             'modified_by': user},
            {'form1': form1_objects[3], 'form2': form2, 'distribution_count': 6, 'target_distribution_count': 2,
             'modified_by': user},
            {'form1': form1_objects[4], 'form2': form2, 'distribution_count': 7, 'target_distribution_count': 4,
             'modified_by': user},
            {'form1': form1_objects[4], 'form2': form2, 'distribution_count': 9, 'target_distribution_count': 5,
             'modified_by': user},
            {'form1': form1_objects[4], 'form2': form2, 'distribution_count': 5, 'target_distribution_count': 3,
             'modified_by': user},
            {'form1': form1_objects[5], 'form2': form2, 'distribution_count': 4, 'target_distribution_count': 1,
             'modified_by': user},
            {'form1': form1_objects[5], 'form2': form2, 'distribution_count': 3, 'target_distribution_count': 2,
             'modified_by': user},
            {'form1': form1_objects[6], 'form2': form2, 'distribution_count': 2, 'target_distribution_count': 1,
             'modified_by': user},
            {'form1': form1_objects[6], 'form2': form2, 'distribution_count': 1, 'target_distribution_count': 0,
             'modified_by': user},
            {'form1': form1_objects[7], 'form2': form2, 'distribution_count': 11, 'target_distribution_count': 6,
             'modified_by': user},
            {'form1': form1_objects[8], 'form2': form2, 'distribution_count': 12, 'target_distribution_count': 7,
             'modified_by': user},
            {'form1': form1_objects[8], 'form2': form2, 'distribution_count': 13, 'target_distribution_count': 8,
             'modified_by': user},
            {'form1': form1_objects[9], 'form2': form2, 'distribution_count': 12, 'target_distribution_count': 7,
             'modified_by': user},
            {'form1': form1_objects[9], 'form2': form2, 'distribution_count': 0, 'target_distribution_count': 9,
             'modified_by': user},
            {'form1': form1_objects[9], 'form2': form2, 'distribution_count': 2, 'target_distribution_count': 8,
             'modified_by': user},
            {'form1': form1_objects[10], 'form2': form2, 'distribution_count': 8, 'target_distribution_count': 8,
             'modified_by': user},
            {'form1': form1_objects[12], 'form2': form2, 'distribution_count': 3, 'target_distribution_count': 5,
             'modified_by': user},
            {'form1': form1_objects[12], 'form2': form2, 'distribution_count': 7, 'target_distribution_count': 6,
             'modified_by': user}
        ]

        for entry in form3_entries:
            Form3.objects.create(**entry)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
