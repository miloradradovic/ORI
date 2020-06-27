import numpy as np
import pandas as pd
from src.get_insights_from_KPIs import get_insights
from sklearn.preprocessing import StandardScaler

# ignore warnings
import warnings
warnings.filterwarnings(action="ignore")


def load():
    # load the data
    data = pd.read_csv('../data/credit_card_data.csv')
    return process(data)


def process(data):
    # drop the id column
    data = data.drop('CUST_ID', 1)

            # check if there are corrupted inputs in data
            # corruption = data.isna().sum()
            # print(corruption)

    # fill NA with median
    data = data.apply(lambda x: x.fillna(x.mean()), axis=0)
            # double check corrupted inputs
            # corruption = data.isna().sum()
            # print(corruption)

    # deriving new KPI
            # Monthly Average Purchase
    data.insert(len(data.columns), "MONTHLY_AVG_PURCHASE", data['PURCHASES'] / data['TENURE'], True)
            # Monthly Cash Advance
    data.insert(len(data.columns), "MONTHLY_CASH_ADVANCE", data['CASH_ADVANCE'] / data['TENURE'], True)
            # Limit Usage Ratio
    data.insert(len(data.columns), "LIMIT_RATIO", data.apply(lambda x: x['BALANCE'] / x['CREDIT_LIMIT'], axis=1), True)
            # Payment: Min Payment
    data.insert(len(data.columns), "PAYMENT_MIN_RATIO", data.apply(lambda x: x['PAYMENTS'] / x['MINIMUM_PAYMENTS'], axis=1), True)

    get_insights(data)
    data = data.drop('PURCHASE_TYPE', 1)

    # outlier treatment - log transformation
            # data.plot(kind='box')
            # plt.show()
    data = data.applymap(lambda x: np.log(x + 1))
            # data.plot(kind='box')
            # plt.show()

    # scale all values
    scalar = StandardScaler()
    data_scaled = scalar.fit_transform(data.values)
    data = pd.DataFrame(data_scaled, columns=data.columns)

    return data
