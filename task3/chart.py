import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
locale.setlocale(locale.LC_TIME, 'en_GB.UTF-8')

processed_data = pd.read_csv("processed_data.csv")
processed_data["date"] = pd.to_datetime(processed_data[['year', 'month']].assign(DAY=1))

plot_data = processed_data.pivot(index="date", columns=["country"], values="consumption_m3")

seaborn.set_theme()
seaborn.set_context("talk")
fig, ax = plt.subplots(figsize=(14, 8))
plot = seaborn.lineplot(processed_data, x="date", y="consumption_m3",
                 hue="country", palette="dark")
plot.set(title='Monthly natural gas consumption per country (in billions of cubic meters)')
plot.set(xlabel="Month", ylabel="Consumption")
seaborn.move_legend(plot, "upper left", bbox_to_anchor=(1.05, 1))

locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
plt.show()