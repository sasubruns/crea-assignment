# importing required modules
import argparse
from brent import get_brent_dataframe
from ttf import get_ttf_dataframe
from urals import get_urals_dataframe

def get_dataframe(indicator: str):
    if (indicator == "brent"):
        return get_brent_dataframe()
    if (indicator == "urals"):
        return get_urals_dataframe()
    if (indicator == "ttf"):
        return get_ttf_dataframe()

 
# create a parser object
parser = argparse.ArgumentParser(description = "Web scraper CLI for CREA")

# add argument
parser.add_argument("indicator", nargs = 1, type=str,
                     help = "Name of the indicator to scrape. 'brent', 'ttf' or 'urals' are available.")

parser.add_argument("output_file", nargs = 1, type=str,
                     help = "Filename to output the results to")
 
# parse the arguments from standard input
args = parser.parse_args()
 
# check if add argument has any input data.
# If it has, then print sum of the given numbers
df = get_dataframe(args.indicator[0])
print(f"Indicator {args.indicator[0]} scraped successfully. Preview:")
print(df.head())
df.to_csv(args.output_file[0], index=False)
print(f"Data saved successfully to {args.output_file[0]}")

print("Exiting program.")
        


