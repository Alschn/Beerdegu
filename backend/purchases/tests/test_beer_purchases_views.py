from rest_framework.test import APITestCase


class BeerPurchasesViewsTests(APITestCase):

    def test_list_purchases(self):
        pass

    def test_list_purchases_not_authenticated(self):
        pass

    def test_list_purchases_other_user(self):
        pass

    def test_list_purchases_filter_beer(self):
        pass

    def test_list_purchases_filter_multiple_beers(self):
        pass

    # todo: test other filters

    def test_retrieve_purchase(self):
        pass

    def test_retrieve_purchase_not_authenticated(self):
        pass

    def test_retrieve_purchase_other_user(self):
        pass

    def test_retrieve_purchase_not_found(self):
        pass

    def test_create_purchase(self):
        pass

    def test_create_purchase_not_authenticated(self):
        pass

    def test_create_purchase_invalid_data(self):
        pass
