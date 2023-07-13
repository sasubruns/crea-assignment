import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import numpy
import locale
locale.setlocale(locale.LC_TIME, 'en_GB.UTF-8')

# Uncomment one of the following to choose which variable to use for grouping

category_variable = "region"
# category_variable = "origin country"

# Uncomment one of the following to choose whether to visualize euros or tonnes

# num_variable = "value_eur"
num_variable = "value_tonne"

category_column = None
ylabel = None
units = None

if category_variable == "region":
    category_column = "Region"
if category_variable == "origin country":
    category_column = "Origin country"

if num_variable == "value_eur":
    ylabel = "Value in EUR"
    units = "EUR"
if num_variable == "value_tonne":
    ylabel = "Tonnes"
    units = "tonnes"

commodity_prettyprint_dict = {"oil_or_chemical": "Oil or chemical",
                              "crude_oil": "Crude oil",
                              "lng": "LNG",
                              "oil_products": "Oil products",
                              "coal": "Coal"}

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

seaborn.set_theme()

for i, commodity in enumerate(commodities):
    fig, ax = plt.subplots(figsize=(20, 9))
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    plot_data = completed_voyages[voyages["commodity"] == commodity]
    plot_data = plot_data.rename(columns={"commodity_destination_region": "Region",
                                          "commodity_origin_iso2": "Origin country",
                                          "commodity_destination_iso2": "Destination country"})
    
    plot_data = plot_data.pivot_table(index="arrival_date_utc", columns=category_column, values=num_variable,
                                        aggfunc=numpy.sum)
    plot_data = plot_data[plot_data.columns[::-1]]
    plot_data.plot.area(ax=ax)

    ax.set_title(f"Completed imports by {category_variable} in {units} ({commodity_prettyprint_dict[commodity]})")
    ax.set_xlabel("Import arrival month")
    ax.set_ylabel(ylabel)

plt.show()