import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
import pandas as pd
from src.load_and_process_data import load


def eda():
    chosen_columns = ["LIMIT_RATIO", "PAYMENT_MIN_RATIO", "MONTHLY_AVG_PURCHASE", "MONTHLY_CASH_ADVANCE"]
    data = load()
    X_chosen = pd.DataFrame(data[chosen_columns])

    kmeans = KMeans(n_clusters=5)
    label = kmeans.fit_predict(X_chosen)
    # create a 'cluster' column
    X_chosen['cluster'] = label
    chosen_columns.append('cluster')
    # make a Seaborn pairplot
    sb.countplot(data=X_chosen, hue='cluster', x='cluster')
    sb.pairplot(X_chosen, hue='cluster', vars=chosen_columns)
    plt.show()




    best_cols = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS", "MINIMUM_PAYMENTS"]
    data_final = pd.DataFrame(data[best_cols])
    alg = KMeans(n_clusters=6)
    label = alg.fit_predict(data_final)

    # create a 'cluster' column
    data_final['cluster'] = label
    best_cols.append('cluster')

    # make a Seaborn pairplot
    sb.pairplot(data_final[best_cols], hue='cluster')
    plt.show()

if __name__ == '__main__':
    eda()
