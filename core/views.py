from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization, UserProfile, Form1, Form2, Form3, SpecialistDismissalReport
from .serializers import OrganizationSerializer, UserProfileSerializer, Form1Serializer, Form2Serializer, Form3Serializer
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class Form1ListCreateView(generics.ListCreateAPIView):
    queryset = Form1.objects.all()
    serializer_class = Form1Serializer


class Form1DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form1.objects.all()
    serializer_class = Form1Serializer


class Form2ListCreateView(generics.ListCreateAPIView):
    queryset = Form2.objects.all()
    serializer_class = Form2Serializer


class Form2DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form2.objects.all()
    serializer_class = Form2Serializer


class Form3ListCreateView(generics.ListCreateAPIView):
    queryset = Form3.objects.all()
    serializer_class = Form3Serializer


class Form3DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form3.objects.all()
    serializer_class = Form3Serializer


class ExportExcelView(APIView):
    def get(self, request, format=None):
        data = self.get_data()

        output = self.export_to_excel(data, month='январь')
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'
        return response

    @staticmethod
    def get_data():
        data = []

        # Fetch organizations
        organizations = Organization.objects.all()
        for org in organizations:
            # Fetch form2 records for each organization
            forms2 = Form2.objects.filter(organization=org)
            for form2 in forms2:
                # Fetch form3 records for each form2
                forms3 = Form3.objects.filter(form2=form2)
                for form3 in forms3:
                    form1 = form3.form1
                    row = {
                        'organization_name': 'Итого:',  # From Organization mode
                        'total_young_specialists': form3.distribution_count + form3.target_distribution_count,  # From Form2 model
                        'commission_referred_total': form3.distribution_count + form3.target_distribution_count,  # From Form2 model
                        'commission_referred_target': form3.distribution_count,  # From Form2 model
                        'commission_referred_distribution': form3.target_distribution_count,  # From Form1 model through Form3
                        'total_dismissed_specialists': form3.target_distribution_count,
                        'term_expired_total': form3.target_distribution_count,  # From Form1 model through Form3
                        'term_expired_target': form3.distribution_count,  # From Form3 model
                        'military_service_total': form3.target_distribution_count,  # From Form3 model
                        'military_service_target': form3.target_distribution_count,  # From Form3 model
                        'military_service_distribution': form3.target_distribution_count,  # From Form3 model
                        'education_institution_total': form3.target_distribution_count,  # From Form3 model
                        'education_institution_target': form3.target_distribution_count,  # From Form3 model
                        'education_institution_distribution': form3.target_distribution_count,  # From Form3 model
                        'relocation_total': form3.target_distribution_count,  # From Form3 model
                        'relocation_target': form3.target_distribution_count,  # From Form3 model
                        'relocation_distribution': form3.target_distribution_count,  # From Form3 model
                        'discrediting_circumstances_total': form3.target_distribution_count,  # From Form3 model
                        'discrediting_circumstances_target': form3.target_distribution_count,  # From Form3 model
                        'discrediting_circumstances_distribution': form3.target_distribution_count,  # From Form3 model
                        'housing_absence_total': form3.target_distribution_count,  # From Form3 model
                        'housing_absence_target': form3.target_distribution_count,  # From Form3 model
                        'housing_absence_distribution': form3.target_distribution_count,  # From Form3 model
                    }
                    data.append(row)

        return data

    @staticmethod
    def export_to_excel(data, month='месяц'):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Adding title and subtitle
        worksheet.merge_range('A2:K2', 'Молодые специалисты', workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bold': True, 'font_size': 14}))
        worksheet.merge_range('A3:K3', f'за {month}-{month} 2024 года', workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'italic': True, 'font_size': 12}))

        # Define headers and subheaders as per the provided structure
        headers = [
            ("Наименование организации", 3, 0, 5, 0),  # A4:A6
            ("Общая численность молодых специалистов", 3, 1, 5, 1),  # B4:B6
            ("Направлен комиссией на основании", 3, 2, 3, 4),  # C4:E4
            ("Количество уволенных молодых специалистов", 3, 5, 5, 5),  # F4:F6
            ("Истечение срока обязательной отработки", 3, 6, 3, 8),  # G4:I4
            ("Призыв на срочную службу", 3, 9, 3, 11),  # J4:L4
            ("Поступление в учреждения образования", 3, 12, 3, 14),  # M4:O4
            ("Переезд в другую местность", 3, 15, 3, 17),  # P4:R4
            ("Дискредитирующие обстоятельства", 3, 18, 3, 20),  # S4:U4
            ("Отсутствие жилья", 3, 21, 3, 23),  # V4:X4
        ]

        subheaders = [
            ("Всего", 4, 2, 5, 2),  # C5:C6
            ("Категория, источник приёма на работу", 4, 3, 4, 4),  # D5:E5
            ("Целевое", 5, 3, 5, 3),  # D6:D6
            ("Распределение", 5, 4, 5, 4),  # E6:E6
            ("Всего", 4, 6, 5, 6),  # G5:G6
            ("Категория, источник приёма на работу", 4, 7, 4, 8),  # H5:I5
            ("Целевое", 5, 7, 5, 7),  # H6:H6
            ("Распределение", 5, 8, 5, 8),  # I6:I6
            ("Всего", 4, 9, 5, 9),  # J5:J6
            ("Категория, источник приёма на работу", 4, 10, 4, 11),  # K5:L5
            ("Целевое", 5, 10, 5, 10),  # K6:K6
            ("Распределение", 5, 11, 5, 11),  # L6:L6
            ("Всего", 4, 12, 5, 12),  # M5:M6
            ("Категория, источник приёма на работу", 4, 13, 4, 14),  # N5:O5
            ("Целевое", 5, 13, 5, 13),  # N6:N6
            ("Распределение", 5, 14, 5, 14),  # O6:O6
            ("Всего", 4, 15, 5, 15),  # P5:P6
            ("Категория, источник приёма на работу", 4, 16, 4, 17),  # Q5:R5
            ("Целевое", 5, 16, 5, 16),  # Q6:Q6
            ("Распределение", 5, 17, 5, 17),  # R6:R6
            ("Всего", 4, 18, 5, 18),  # S5:S6
            ("Категория, источник приёма на работу", 4, 19, 4, 20),  # T5:U5
            ("Целевое", 5, 19, 5, 19),  # T6:T6
            ("Распределение", 5, 20, 5, 20),  # U6:U6
            ("Всего", 4, 21, 5, 21),  # V5:V6
            ("Категория, источник приёма на работу", 4, 22, 4, 23),  # W5:X5
            ("Целевое", 5, 22, 5, 22),  # W6:W6
            ("Распределение", 5, 23, 5, 23),  # X6:X6
        ]

        header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        subheader_format = workbook.add_format(
                     {'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

        # Write headers
        for header, row_start, col_start, row_end, col_end in headers:
            worksheet.merge_range(row_start, col_start, row_end, col_end, header, header_format)

        # Write subheaders
        for subheader, row_start, col_start, row_end, col_end in subheaders:
            if row_start == row_end and col_start == col_end:
                 worksheet.write(row_start, col_start, subheader, subheader_format)
            else:
                worksheet.merge_range(row_start, col_start, row_end, col_end, subheader, subheader_format)

        # Adjust start_row to account for header rows
        start_row = 6
        for row_num, row_data in enumerate(data, start_row):
            for col_num, (col_name, col_value) in enumerate(row_data.items()):
                worksheet.write(row_num, col_num, col_value)

        workbook.close()
        output.seek(0)
        return output

# class ExportExcelView(APIView):
#     def get(self, request, format=None):
#         data = list(
#             SpecialistDismissalReport.objects.values(
#                 'organization_name',
#                 'total_young_specialists',
#                 'commission_referred_total',
#                 'total_dismissed_specialists',
#                 'term_expired_total',
#                 'military_service_total',
#                 'education_institution_total',
#                 'relocation_total',
#                 'discrediting_circumstances_total',
#                 'housing_absence_total',
#                 'rep_beg_period',
#                 'rep_end_period'
#             )
#         )
#
#         output = self.export_to_excel(data, month='январь')
#         response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=report.xlsx'
#         return response
#
#     @staticmethod
#     def export_to_excel(data, month='месяц'):
#         output = BytesIO()
#         workbook = xlsxwriter.Workbook(output, {'in_memory': True})
#         worksheet = workbook.add_worksheet()
#
#         # Adding title and subtitle
#         worksheet.merge_range('A2:X2', 'Молодые специалисты', workbook.add_format(
#             {'align': 'center', 'valign': 'vcenter', 'bold': True, 'font_size': 14}))
#         worksheet.merge_range('A3:X3', f'за {month}-{month} 2024 года', workbook.add_format(
#             {'align': 'center', 'valign': 'vcenter', 'italic': True, 'font_size': 12}))
#
#         # Define headers and subheaders as per the provided structure
#         headers = [
#             ("Наименование организации", 3, 0, 5, 0),  # A4:A6
#             ("Общая численность молодых специалистов", 3, 1, 5, 1),  # B4:B6
#             ("Направлен комиссией на основании", 3, 2, 3, 4),  # C4:E4
#             ("Количество уволенных молодых специалистов", 3, 5, 5, 5),  # F4:F6
#             ("Истечение срока обязательной отработки", 3, 6, 3, 8),  # G4:I4
#             ("Призыв на срочную службу", 3, 9, 3, 11),  # J4:L4
#             ("Поступление в учреждения образования", 3, 12, 3, 14),  # M4:O4
#             ("Переезд в другую местность", 3, 15, 3, 17),  # P4:R4
#             ("Дискредитирующие обстоятельства", 3, 18, 3, 20),  # S4:U4
#             ("Отсутствие жилья", 3, 21, 3, 23),  # V4:X4
#         ]
#
#         subheaders = [
#             ("Всего", 4, 2, 5, 2),  # C5:C6
#             ("Категория, источник приёма на работу", 4, 3, 4, 4),  # D5:E5
#             ("Целевое", 5, 3, 5, 3),  # D6:D6
#             ("Распределение", 5, 4, 5, 4),  # E6:E6
#             ("Всего", 4, 6, 5, 6),  # G5:G6
#             ("Категория, источник приёма на работу", 4, 7, 4, 8),  # H5:I5
#             ("Целевое", 5, 7, 5, 7),  # H6:H6
#             ("Распределение", 5, 8, 5, 8),  # I6:I6
#             ("Всего", 4, 9, 5, 9),  # J5:J6
#             ("Категория, источник приёма на работу", 4, 10, 4, 11),  # K5:L5
#             ("Целевое", 5, 10, 5, 10),  # K6:K6
#             ("Распределение", 5, 11, 5, 11),  # L6:L6
#             ("Всего", 4, 12, 5, 12),  # M5:M6
#             ("Категория, источник приёма на работу", 4, 13, 4, 14),  # N5:O5
#             ("Целевое", 5, 13, 5, 13),  # N6:N6
#             ("Распределение", 5, 14, 5, 14),  # O6:O6
#             ("Всего", 4, 15, 5, 15),  # P5:P6
#             ("Категория, источник приёма на работу", 4, 16, 4, 17),  # Q5:R5
#             ("Целевое", 5, 16, 5, 16),  # Q6:Q6
#             ("Распределение", 5, 17, 5, 17),  # R6:R6
#             ("Всего", 4, 18, 5, 18),  # S5:S6
#             ("Категория, источник приёма на работу", 4, 19, 4, 20),  # T5:U5
#             ("Целевое", 5, 19, 5, 19),  # T6:T6
#             ("Распределение", 5, 20, 5, 20),  # U6:U6
#             ("Всего", 4, 21, 5, 21),  # V5:V6
#             ("Категория, источник приёма на работу", 4, 22, 4, 23),  # W5:X5
#             ("Целевое", 5, 22, 5, 22),  # W6:W6
#             ("Распределение", 5, 23, 5, 23),  # X6:X6
#         ]
#
#         header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
#         subheader_format = workbook.add_format(
#             {'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
#
#         # Write headers
#         for header, row_start, col_start, row_end, col_end in headers:
#             worksheet.merge_range(row_start, col_start, row_end, col_end, header, header_format)
#
#         # Write subheaders
#         for subheader, row_start, col_start, row_end, col_end in subheaders:
#             if row_start == row_end and col_start == col_end:
#                 worksheet.write(row_start, col_start, subheader, subheader_format)
#             else:
#                 worksheet.merge_range(row_start, col_start, row_end, col_end, subheader, subheader_format)
#
#         # Adjust start_row to account for header rows
#         start_row = 6
#         for row_num, row_data in enumerate(data, start_row):
#             for col_num, (col_name, col_value) in enumerate(row_data.items()):
#                 worksheet.write(row_num, col_num, col_value)
#
#         workbook.close()
#         output.seek(0)
#         return output
