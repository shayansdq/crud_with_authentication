from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta, datetime

from authenticate.models import CustomUser


class WeekRangeListApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # intialize some users
        register_url = reverse('authenticate:register')
        response = self.client.get(register_url, data={'username': 'shayan20', 'password': '123'})
        print(response)
        # login_url = reverse('authenticate:login')

    def test_register_urls(self):
        pass


    # def test_week_range_list_api_view(self):
    #     """
    #     create an api client and send request to the weekly range api and check that with the database
    #     :return:
    #     """
    #     # Test the WeekRangeListApiView
    #     url = reverse('supervisor:weekly-range')
    #     response = self.client.get(url)
    #     all_weekly_incomes = WeeklyIncome.objects.all()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), all_weekly_incomes.count())
    #     expected_data = WeeklyIncomeSerializer(all_weekly_incomes, many=True).data
    #     self.assertEqual(response.data, expected_data)

    # def test_weekly_income_filtering(self):
    #     """
    #     create an api client and send request to the weekly range api and check that with the database
    #     with the filter parameters
    #     :return:
    #     """
    #
    #     # Test filtering using the WeeklyIncomeFilter
    #     from_date = '2023-08-12'
    #     to_date = '2023-08-14'
    #     from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
    #     to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
    #     filter_data = {
    #         'to_date': to_date,
    #         'from_date': from_date,
    #     }
    #     weekly_incomes_from_db = WeeklyIncome.objects.filter(saturday__range=(from_date_obj, to_date_obj))
    #     url = reverse('supervisor:weekly-range')
    #     response = self.client.get(url, data=filter_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), weekly_incomes_from_db.count())
    #     expected_data = WeeklyIncomeSerializer(weekly_incomes_from_db, many=True).data
    #     self.assertEqual(response.data, expected_data)
    #
    # def test_filterset(self):
    #     # Test the WeeklyIncomeFilter
    #     weekly_incomes: WeeklyIncome = WeeklyIncome.objects.all()
    #     from_date = '2023-08-12'
    #     to_date = '2023-08-14'
    #     from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
    #     to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
    #     filter_data = {
    #         'to_date': to_date,
    #         'from_date': from_date,
    #     }
    #     filterset = WeeklyIncomeFilter(data=filter_data)
    #     self.assertTrue(filterset.is_valid())
    #     weekly_incomes_from_db = WeeklyIncome.objects.filter(saturday__range=(from_date_obj, to_date_obj))
    #     filtered_queryset = filterset.filter_queryset(weekly_incomes)
    #     expected_data_from_db = WeeklyIncomeSerializer(weekly_incomes_from_db, many=True).data
    #     expected_data_from_filterset = WeeklyIncomeSerializer(filtered_queryset, many=True).data
    #     self.assertEqual(len(filtered_queryset), weekly_incomes_from_db.count())
    #     self.assertEqual(expected_data_from_db, expected_data_from_filterset)
