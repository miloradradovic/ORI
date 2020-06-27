import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
import pandas as pd
from src.load_and_process_data import load


def eda():
    data = load()
    best_cols = ["MONTHLY_AVG_PURCHASE", "MONTHLY_CASH_ADVANCE", "LIMIT_RATIO", "PAYMENT_MIN_RATIO"]
    data_final = pd.DataFrame(data[best_cols])
    alg = KMeans(n_clusters=6)
    label = alg.fit_predict(data_final)

    # create a 'cluster' column
    data_final['cluster'] = label
    best_cols.append('cluster')

    # make a Seaborn pairplot
    sb.countplot(data=data_final, hue='cluster', x='cluster')
    sb.pairplot(data_final[best_cols], hue='cluster', vars=best_cols, palette= 'Dark2', diag_kind='kde')
    plt.show()

    best_cols1 = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS", "MINIMUM_PAYMENTS"]
    data_final1 = pd.DataFrame(data[best_cols1])
    alg = KMeans(n_clusters=6)
    label = alg.fit_predict(data_final1)

    # create a 'cluster' column
    data_final1['cluster'] = label
    best_cols1.append('cluster')

    # make a Seaborn pairplot
    sb.countplot(data=data_final1, hue='cluster', x='cluster')
    sb.pairplot(data_final1[best_cols1], hue='cluster', vars=best_cols1, palette='Dark2', diag_kind='kde')
    plt.show()


if __name__ == '__main__':
    eda()
