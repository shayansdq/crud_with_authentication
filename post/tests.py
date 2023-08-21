from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta, datetime

from trip.choices import CustomerType
from trip.models import Trip
from .models import WeeklyIncome, Courier, DailyIncome, IncreaseIncome, DecreaseIncome
from .serializers import WeeklyIncomeSerializer, CourierIncomeSerializer
from .filters import WeeklyIncomeFilter
from .utils.utils import saturday_finder


class WeekRangeListApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some test data for Courier models and trip models to create incomes automatically
        self.courier_1 = Courier.objects.create(first_name='reza',
                                                last_name='miri')
        self.courier_2 = Courier.objects.create(first_name='majid',
                                                last_name='mohammadi')
        self.courier_3 = Courier.objects.create(first_name='alireza',
                                                last_name='rezaie')
        self.initial_trip_1 = Trip.objects.create(courier=self.courier_1,
                                                  cost=50000,
                                                  customer_type=CustomerType.IndividualPerson, )
        self.initial_trip_2 = Trip.objects.create(courier=self.courier_3,
                                                  cost=90000,
                                                  customer_type=CustomerType.Company, )

    def test_increase_decrease_trip_incomes(self):
        """
            Create incomes (trip, increase and decreases incomes) and check them with the weekly and daily incomes
            with assert equals for three couriers
        :return:
        """
        inc_1 = IncreaseIncome.objects.create(courier=self.courier_1,
                                              amount=98000)
        inc_2 = IncreaseIncome.objects.create(courier=self.courier_3,
                                              amount=48000)
        inc_3 = IncreaseIncome.objects.create(courier=self.courier_1,
                                              amount=76000)
        trip_1 = Trip.objects.create(courier=self.courier_3,
                                     cost=29000,
                                     customer_type=CustomerType.Company, )
        dec_1 = DecreaseIncome.objects.create(courier=self.courier_1,
                                              amount=29000)
        dec_2 = DecreaseIncome.objects.create(courier=self.courier_3,
                                              amount=22000)
        inc_4 = IncreaseIncome.objects.create(courier=self.courier_3,
                                              amount=27000)
        trip_2 = Trip.objects.create(courier=self.courier_2,
                                     cost=89000,
                                     customer_type=CustomerType.Company, )
        inc_5 = IncreaseIncome.objects.create(courier=self.courier_2,
                                              amount=35000)
        dec_3 = DecreaseIncome.objects.create(courier=self.courier_1,
                                              amount=34000)
        dec_4 = DecreaseIncome.objects.create(courier=self.courier_3,
                                              amount=12000)
        trip_3 = Trip.objects.create(courier=self.courier_2,
                                     cost=37500,
                                     customer_type=CustomerType.Company, )
        inc_6 = IncreaseIncome.objects.create(courier=self.courier_3,
                                              amount=43000)
        dec_5 = DecreaseIncome.objects.create(courier=self.courier_2,
                                              amount=34000)
        trip_4 = Trip.objects.create(courier=self.courier_1,
                                     cost=40000,
                                     customer_type=CustomerType.Company, )
        trip_5 = Trip.objects.create(courier=self.courier_1,
                                     cost=69000,
                                     customer_type=CustomerType.Company, )
        daily_income_courier_1 = DailyIncome.objects.get(date=inc_1.created.date(),
                                                         courier=self.courier_1)
        weekly_income_courier_1 = WeeklyIncome.objects.get(saturday=saturday_finder(inc_1.created.date()),
                                                           courier=self.courier_1)
        daily_income_courier_2 = DailyIncome.objects.get(date=inc_1.created.date(),
                                                         courier=self.courier_2)
        weekly_income_courier_2 = WeeklyIncome.objects.get(saturday=saturday_finder(inc_1.created.date()),
                                                           courier=self.courier_2)
        daily_income_courier_3 = DailyIncome.objects.get(date=inc_1.created.date(),
                                                         courier=self.courier_3)
        weekly_income_courier_3 = WeeklyIncome.objects.get(saturday=saturday_finder(inc_1.created.date()),
                                                           courier=self.courier_3)

        # Test daily income of couriers
        income_courier_1 = (inc_1.amount + inc_3.amount) - (dec_1.amount + dec_3.amount) + (
                trip_4.cost + trip_5.cost + self.initial_trip_1.cost)
        income_courier_2 = inc_5.amount - dec_5.amount + (trip_2.cost + trip_3.cost)
        income_courier_3 = (inc_2.amount + inc_4.amount + inc_6.amount) - (dec_2.amount + dec_4.amount) + \
                           (trip_1.cost + self.initial_trip_2.cost)
        self.assertEqual(daily_income_courier_1.income, income_courier_1)
        self.assertEqual(daily_income_courier_2.income, income_courier_2)
        self.assertEqual(daily_income_courier_3.income, income_courier_3)

        # Test weekly income of couriers
        self.assertEqual(weekly_income_courier_1.income, income_courier_1)
        self.assertEqual(weekly_income_courier_2.income, income_courier_2)
        self.assertEqual(weekly_income_courier_3.income, income_courier_3)

    def test_week_range_list_api_view(self):
        """
        create an api client and send request to the weekly range api and check that with the database
        :return:
        """
        # Test the WeekRangeListApiView
        url = reverse('supervisor:weekly-range')
        response = self.client.get(url)
        all_weekly_incomes = WeeklyIncome.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), all_weekly_incomes.count())
        expected_data = WeeklyIncomeSerializer(all_weekly_incomes, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_weekly_income_filtering(self):
        """
        create an api client and send request to the weekly range api and check that with the database
        with the filter parameters
        :return:
        """

        # Test filtering using the WeeklyIncomeFilter
        from_date = '2023-08-12'
        to_date = '2023-08-14'
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        filter_data = {
            'to_date': to_date,
            'from_date': from_date,
        }
        weekly_incomes_from_db = WeeklyIncome.objects.filter(saturday__range=(from_date_obj, to_date_obj))
        url = reverse('supervisor:weekly-range')
        response = self.client.get(url, data=filter_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), weekly_incomes_from_db.count())
        expected_data = WeeklyIncomeSerializer(weekly_incomes_from_db, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_filterset(self):
        # Test the WeeklyIncomeFilter
        weekly_incomes: WeeklyIncome = WeeklyIncome.objects.all()
        from_date = '2023-08-12'
        to_date = '2023-08-14'
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        filter_data = {
            'to_date': to_date,
            'from_date': from_date,
        }
        filterset = WeeklyIncomeFilter(data=filter_data)
        self.assertTrue(filterset.is_valid())
        weekly_incomes_from_db = WeeklyIncome.objects.filter(saturday__range=(from_date_obj, to_date_obj))
        filtered_queryset = filterset.filter_queryset(weekly_incomes)
        expected_data_from_db = WeeklyIncomeSerializer(weekly_incomes_from_db, many=True).data
        expected_data_from_filterset = WeeklyIncomeSerializer(filtered_queryset, many=True).data
        self.assertEqual(len(filtered_queryset), weekly_incomes_from_db.count())
        self.assertEqual(expected_data_from_db, expected_data_from_filterset)
