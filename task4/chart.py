import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import numpy

voyages = pd.read_csv('voyages.csv')
voyages["departure_date_utc"] = pd.to_datetime(voyages["departure_date_utc"])
voyages["arrival_date_utc"] = pd.to_datetime(voyages["arrival_date_utc"])
voyages = voyages.groupby([pd.Grouper(key="arrival_date_utc", freq="M"),
                           "status",
                           "commodity_origin_iso2",
                           "commodity_destination_iso2",
                           "commodity_destination_region",
                           "commodity"]).sum().reset_index()
completed_voyages = voyages[voyages["status"] == "completed"]

commodities = list(completed_voyages["commodity"].unique())
print(commodities)
for i, commodity in enumerate(commodities):
    fig, ax = plt.subplots(figsize=(20, 9))
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plot_data = completed_voyages[voyages["commodity"] == commodity]
    plot_data = plot_data.rename(columns={"commodity_destination_region": "Region"})
    plot_data = plot_data.pivot_table(index="arrival_date_utc", columns="Region", values="value_eur",
                                        aggfunc=numpy.sum)
    plot_data = plot_data[plot_data.columns[::-1]]
    plot_data.plot.area(ax=ax)
    ax.set_title(f"Completed imports by region in billions EUR ({commodity})")
    ax.set_xlabel("Import arrival month")
    ax.set_ylabel("Value in EUR")

plt.show()