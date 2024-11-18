import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
df = pd.read_csv("daily_stats.csv")
df.drop(columns=['day','min_price','min_price','max_price','price_std','trades_count','avg_return','avg_balance'],inplace=True)

# sns.lineplot(df)
# plt.ylabel('Average Price $')
# plt.xlabel('Day')

# rolling_mean = df.rolling(7).mean()
# rolling_std = df.rolling(7).std()
# plt.plot(df, color="blue",label="Original Price Data")
# plt.plot(rolling_mean, color="red", label="Rolling Mean Stock Price Number")
# plt.plot(rolling_std, color="black", label = "Rolling Standard Deviation in Stock Price")
# plt.title("Stock Price Time Series, Rolling Mean, Standard Deviation")
# plt.legend(loc="best")
# plt.show()

adft = adfuller(df,autolag="AIC")

output_df = pd.DataFrame({"Values":[adft[0],adft[1],adft[2],adft[3], adft[4]['1%'], adft[4]['5%'], adft[4]['10%']]  , "Metric":["Test Statistics","p-value","No. of lags used","Number of observations used", 
                                                        "critical value (1%)", "critical value (5%)", "critical value (10%)"]})
print(output_df)

decompose = seasonal_decompose(df['avg_price'],model='additive', period=7)
decompose.plot()
plt.show()