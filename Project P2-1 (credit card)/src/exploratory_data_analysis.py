import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
import pandas as pd


def eda(data):
    print("Started exploratory data analysis!")
    k_means = KMeans(n_clusters=7)

    cols = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS", "MINIMUM_PAYMENTS"]
    selected = pd.DataFrame(data[cols])

    label = k_means.fit_predict(selected)

    # 'cluster' column
    selected['cluster'] = label
    cols.append('cluster')

    # Seaborn pairplot
    sb.countplot(data=selected, hue='cluster', x='cluster')
    sb.pairplot(selected[cols], hue='cluster', vars=cols, palette='Dark2')
    plt.show()

    cols1 = ["MONTHLY_AVG_PURCHASE", "MONTHLY_CASH_ADVANCE", "LIMIT_RATIO", "PAYMENT_MIN_RATIO"]
    selected1 = pd.DataFrame(data[cols1])

    label1 = k_means.fit_predict(selected1)

    # 'cluster' column
    selected1['cluster'] = label1
    cols1.append('cluster')

    # Seaborn pairplot
    sb.countplot(data=selected1, hue='cluster', x='cluster')
    sb.pairplot(selected1[cols1], hue='cluster', vars=cols1, palette='Dark2')
    plt.show()
