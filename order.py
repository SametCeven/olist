import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        orders = self.data["orders"].copy()
        if is_delivered:
            orders = orders[orders["order_status"] == "delivered"].copy()

        orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
        orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"])
        orders["order_delivered_carrier_date"] = pd.to_datetime(orders["order_delivered_carrier_date"])
        orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
        orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])
        orders["wait_time"] = (
            orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
        ) / np.timedelta64(24, "h")
        orders["expected_wait_time"] = (
            orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
        ) / np.timedelta64(24, "h")
        orders["delay_vs_expected"] = ((
            orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
        ) / np.timedelta64(24, "h")).clip(lower=0)

        return orders[["order_id", "wait_time", "expected_wait_time", "delay_vs_expected", "order_status"]]


    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data["order_reviews"].copy()
        reviews["dim_is_five_star"] = (reviews["review_score"].map(lambda x: x == 5)).astype(int)
        reviews["dim_is_one_star"] = (reviews["review_score"].map(lambda x: x == 1)).astype(int)
        return reviews[["order_id","dim_is_five_star", "dim_is_one_star", "review_score"]]


    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        df_order_items:pd.DataFrame = self.data['order_items'].copy()
        df_order_items_summary:pd.DataFrame = (
            df_order_items
            .groupby("order_id")["product_id"]
            .agg("count")
            .rename("number_of_items")
            .reset_index()
        )
        return df_order_items_summary


    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        df_order_items:pd.DataFrame = self.data['order_items'].copy()
        df_order_items_summary_sellers:pd.DataFrame = (
            df_order_items
            .groupby("order_id")["seller_id"]
            .agg("nunique")
            .rename("number_of_sellers")
            .reset_index()
        )
        return df_order_items_summary_sellers


    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
