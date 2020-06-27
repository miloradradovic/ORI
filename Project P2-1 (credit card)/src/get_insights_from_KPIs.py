import matplotlib.pyplot as plt


def get_insights(data):
    # Purchase By Type: ONEOFF_ONLY,   INTSTALLMENTS_ONLY,   BOTH_ONEOFF_INSTALL,   NONE_ONEOFF_INSTALL
    # This KPI is done here because of it's none number value and later is dropped
    data["PURCHASE_TYPE"] = data.apply(purchase_type, axis=1)

    pt = data.groupby(by="PURCHASE_TYPE")
    colors = list('rgby')

    pt["MONTHLY_AVG_PURCHASE"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase Type")
    plt.ylabel("Avg monthly purchase")
    plt.show()
            # Average monthly purchase using both oneoff and installments are very high (almost 193)
            # Average monthly purchase using installments only is very low (around 47)


    pt["MONTHLY_CASH_ADVANCE"].mean().plot(kind="bar", color=colors)
    plt.ylabel("Avg monthly cash advance")
    plt.xlabel("Puchase type")
    plt.show()
            # Customers who didn't do either of oneoff or installment purchases take highest monthly cash advance

    # average limit usage by purchase type
    pt["LIMIT_RATIO"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase Type")
    plt.ylabel("Avg limit usage")
    plt.show()
            # Customers with installments only purchases have good balance to credit limit ratio

    # average payments to minimum payment ratio
    pt["PAYMENT_MIN_RATIO"].mean().plot(kind="bar", color=colors)
    plt.xlabel("Purchase type")
    plt.ylabel("Avg payment to minimum payment ratio")
    plt.show()
            # Customers with installments only purchases are paying their dues fast


def purchase_type(x):
   if (x.ONEOFF_PURCHASES > 0) & (x.INSTALLMENTS_PURCHASES <= 0):
      return "ONEOFF_ONLY"
   if (x.ONEOFF_PURCHASES <= 0) & (x.INSTALLMENTS_PURCHASES > 0):
      return "INTSTALLMENTS_ONLY"
   if (x.ONEOFF_PURCHASES > 0) & (x.INSTALLMENTS_PURCHASES > 0):
      return "BOTH_ONEOFF_INSTALL"
   if (x.ONEOFF_PURCHASES <= 0) & (x.INSTALLMENTS_PURCHASES <= 0):
      return "NONE_ONEOFF_INSTALL"
