from django.contrib.auth.models import User
from django.db import models, connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Название организации')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user.username


class Form1(models.Model):
    id = models.AutoField(primary_key=True)
    valid_until = models.DateField(verbose_name='Дата, до которой является актуальной')
    article_name = models.CharField(max_length=255, verbose_name='Наименование статьи')
    order = models.IntegerField(verbose_name='Порядок следования статей')

    last_modified = models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего изменения записи')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Имя пользователя, изменившего запись')

    class Meta:
        verbose_name = 'Показатели молодых специалистов'
        verbose_name_plural = 'Показатели молодых специалистов'

    def __str__(self):
        return self.article_name


class Form2(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(verbose_name='Дата начала отчетного периода')
    end_date = models.DateField(verbose_name='Дата окончания отчетного периода')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления записи в БД')

    class Meta:
        verbose_name = 'Шапка месячных форм молодых специалистов'
        verbose_name_plural = 'Шапки месячных форм молодых специалистов'

    def __str__(self):
        return f'{self.organization.name} ({self.start_date} - {self.end_date})'


class Form3(models.Model):
    id = models.AutoField(primary_key=True)
    form1 = models.ForeignKey(Form1, on_delete=models.CASCADE, verbose_name='Связь с формой 1')
    form2 = models.ForeignKey(Form2, on_delete=models.CASCADE, verbose_name='Связь с формой 2')
    distribution_count = models.IntegerField(verbose_name='Количество молодых специалистов по Распределению')
    target_distribution_count = models.IntegerField(verbose_name='Количество молодых специалистов по Целевому распределению')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего изменения записи')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Имя пользователя, изменившего запись')

    class Meta:
        verbose_name = 'Линии месячных форм молодых специалистов'
        verbose_name_plural = 'Линии месячных форм молодых специалистов'

    def __str__(self):
        return f'Form3: {self.form1} - {self.form2}'


class SpecialistDismissalReport(models.Model):
    organization_name = models.CharField(max_length=255)
    total_young_specialists = models.IntegerField(null=True, blank=True)
    commission_referred_total = models.IntegerField(null=True, blank=True)
    total_dismissed_specialists = models.IntegerField(null=True, blank=True)
    term_expired_total = models.IntegerField(null=True, blank=True)
    military_service_total = models.IntegerField(null=True, blank=True)
    education_institution_total = models.IntegerField(null=True, blank=True)
    relocation_total = models.IntegerField(null=True, blank=True)
    discrediting_circumstances_total = models.IntegerField(null=True, blank=True)
    housing_absence_total = models.IntegerField(null=True, blank=True)
    rep_beg_period = models.DateField()
    rep_end_period = models.DateField()

    class Meta:
        db_table = 'source_table'

    @staticmethod
    def create_sql_view():
        sql_script = """
            CREATE OR REPLACE VIEW specialist_dismissal_report_view 
            WITH (security_invoker=true, security_barrier=true)
            AS SELECT
                organization_name,
                total_young_specialists,
                commission_referred_total,
                total_dismissed_specialists,
                term_expired_total,
                military_service_total,
                education_institution_total,
                relocation_total,
                discrediting_circumstances_total,
                housing_absence_total,
                rep_beg_period,
                rep_end_period
            FROM
                source_table;
            """
        with connection.cursor() as cursor:
            cursor.execute(sql_script)

