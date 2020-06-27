import matplotlib.pyplot as plt


def get_insights(data):
    # Purchase By Type: ONEOFF_ONLY,   INTSTALLMENTS_ONLY,   BOTH_ONEOFF_INSTALL,   NONE_ONEOFF_INSTALL
    # This KPI is done here because of it's none number value and later is dropped
    data["PURCHASE_TYPE"] = data.apply(purchase_type, axis=1)

    pt = data.groupby(by="PURCHASE_TYPE")
    colors = list('rgby')

    pt["MONTHLY_AVG_PURCHASE"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase Type")
    plt.ylabel("Average monthly purchase")
    plt.show()

    pt["MONTHLY_CASH_ADVANCE"].mean().plot(kind="bar", color=colors)
    plt.ylabel("Average monthly cash advance")
    plt.xlabel("Puchase type")
    plt.show()

    # average limit usage by purchase type
    pt["LIMIT_RATIO"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase Type")
    plt.ylabel("Average limit usage")
    plt.show()

    # average payments to minimum payment ratio
    pt["PAYMENT_MIN_RATIO"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase type")
    plt.ylabel("Average payment to minimum payment ratio")
    plt.show()


def purchase_type(x):
   if (x.ONEOFF_PURCHASES > 0) & (x.INSTALLMENTS_PURCHASES <= 0):
      return "ONEOFF_ONLY"
   if (x.ONEOFF_PURCHASES <= 0) & (x.INSTALLMENTS_PURCHASES > 0):
      return "INTSTALLMENTS_ONLY"
   if (x.ONEOFF_PURCHASES > 0) & (x.INSTALLMENTS_PURCHASES > 0):
      return "BOTH_ONEOFF_INSTALL"
   if (x.ONEOFF_PURCHASES <= 0) & (x.INSTALLMENTS_PURCHASES <= 0):
      return "NONE_ONEOFF_INSTALL"
