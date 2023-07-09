import pandas as pd

input_data = pd.read_csv("assignment_flows.csv")

# Convert date to datetime from string
input_data["date"] = pd.to_datetime(input_data["date"], format="%Y-%m-%d")
input_data["year"] = input_data["date"].dt.year
input_data["month"] = input_data["date"].dt.month

# Create a dictionary for iso code to country conversion.
# This enables processing with only iso codes, country names can be added back later.
# I'm assuming country names are unique but just to be safe.

dict_from_origins = pd.Series(input_data["commodity_origin_country"].values,
                             index=input_data["commodity_origin_iso2"]).to_dict()
dict_from_destinations = pd.Series(input_data["commodity_destination_country"].values,
                             index=input_data["commodity_destination_iso2"]).to_dict()

iso_country_dict = {**dict_from_origins, **dict_from_destinations} # Use x | y syntax? Only works in python 3.9 or greater

# Separate cross border and production data
crossborder = input_data[input_data["type"] == "crossborder"]
production = input_data[input_data["type"] == "production"]

# Get monthly gross exports, gross imports and production per commodity type, country and month

monthly_gross_exports = crossborder.groupby(["commodity_origin_iso2", "commodity", "year", "month"],
                                            as_index=False).sum()
monthly_gross_exports.rename(columns={"value_m3": "gross_exports_m3", "commodity_origin_iso2": "iso2"},
                             inplace=True)

monthly_gross_imports = crossborder.groupby(["commodity_destination_iso2", "commodity", "year", "month"],
                                            as_index=False).sum()
monthly_gross_imports.rename(columns={"value_m3": "gross_imports_m3", "commodity_destination_iso2": "iso2"},
                             inplace=True)

monthly_production = production.groupby(["commodity_origin_iso2", "commodity", "year", "month"],
                                            as_index=False).sum()
monthly_production.rename(columns={"value_m3": "production_m3", "commodity_origin_iso2": "iso2"},
                             inplace=True)

# Merge export, import and production dataframes
merged_data = pd.merge(monthly_gross_exports, monthly_gross_imports, on=["iso2", "commodity", "year", "month"])
merged_data = pd.merge(merged_data, monthly_production, on=["iso2", "commodity", "year", "month"])

# Calculate net imports (gross imports - gross exports)
merged_data["net_imports_m3"] = merged_data["gross_imports_m3"] - merged_data["gross_exports_m3"]

# Calculate consumption (production + net imports)
merged_data["consumption_m3"] = merged_data["production_m3"] + merged_data["net_imports_m3"]

# Latest datapoints are from first of May. Ignoring data from this day since the task is
# to estimate monthly consumption and this amount of data is not enough to estimate
# consumption for the whole of May.
merged_data = merged_data[merged_data["month"] < 5]

# Get a suitable subset of columns and export data to a new csv
merged_data["country"] = merged_data["iso2"].apply(lambda iso: iso_country_dict[iso])
output_data = merged_data[["iso2", "country", "year", "month", "commodity", "net_imports_m3", "production_m3", "consumption_m3"]]
output_data.to_csv("processed_data.csv", sep=",", index=False)