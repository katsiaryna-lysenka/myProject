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

        Form1.objects.all().delete()

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

        form2, created = Form2.objects.get_or_create(
            start_date=parse_date('2024-01-01'),
            end_date=parse_date('2024-01-31'),
            organization=org
        )

        for form1 in Form1.objects.all():
            Form3.objects.get_or_create(
                form1=form1,
                form2=form2,
                defaults={
                    'distribution_count': 10,
                    'target_distribution_count': 5,
                    'modified_by': user
                }
            )

        reports = [
            {
                'organization_name': 'Итого',
                'total_young_specialists': 100,
                'commission_referred_total': 10,
                'commission_referred_target': 5,
                'commission_referred_distribution': 5,
                'total_dismissed_specialists': 15,
                'term_expired_total': 6,
                'term_expired_target': 2,
                'term_expired_distribution': 4,
                'military_service_total': 2,
                'military_service_target': 2,
                'military_service_distribution': 2,
                'education_institution_total': 5,
                'education_institution_target': 3,
                'education_institution_distribution': 2,
                'relocation_total': 2,
                'relocation_target': 1,
                'relocation_distribution': 1,
                'discrediting_circumstances_total': 1,
                'discrediting_circumstances_target': 0,
                'discrediting_circumstances_distribution': 1,
                'housing_absence_total': 1,
                'housing_absence_target': 1,
                'housing_absence_distribution': 0,
            }
        ]

        for report in reports:
            SpecialistDismissalReport.objects.get_or_create(**report)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
