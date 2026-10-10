from django.test import TestCase
from django.urls import reverse

from manageCash.models import AddCashModel, ExpenseModel, UserModel


class DashboardDataTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='StrongPass123!'
        )

    def test_dashboard_shows_income_expense_and_balance_after_user_posts(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('addCash_view'),
            {'source': 'Salary', 'amount': 1000, 'description': 'Monthly salary'}
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('expense_view'),
            {'description': 'Rent', 'amount': 300}
        )
        self.assertEqual(response.status_code, 302)

        cash_record = AddCashModel.objects.get(user=self.user)
        expense_record = ExpenseModel.objects.get(user=self.user)

        self.assertEqual(cash_record.amount, 1000)
        self.assertEqual(expense_record.amount, 300)

        response = self.client.get(reverse('dashboard_view', kwargs={'id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1000')
        self.assertContains(response, '300')
        self.assertContains(response, '700')
        self.assertContains(response, 'Salary')
        self.assertContains(response, 'Rent')
