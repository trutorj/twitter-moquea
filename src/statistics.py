import pandas as pd
import datetime as dt

##################################################################################
#                        DO THE STATISTICS                                       #
##################################################################################
# Pipeline to analyze the correlation between tweets and polen levels

# Function to normalize the data
def Normalizador(df, column):
    df["normalized"] = (df[column]-df[column].min())/(df[column].max()-df[column].min())
    return df

# 1. Polen data
# Import the data
polen = pd.read_csv('data/SEAIC_Madrid.csv')

# Calculate the average
polen["mean"] = polen[["Subiza", "Infanta_Leonor"]].mean(axis=1)

# Convert date column to datetime and set it as index
polen["date"] = pd.to_datetime(polen["date"])
polen = polen.set_index('date')

# Subset by year
polen_years = [polen[f'{i}'] for i in range(2017,2021)]

# Normalize the subsets
for e in polen_years:
    Normalizador(e, "mean")

#2. Tweet data
# Import the data
tweet_series = pd.read_csv('data/tweets_series.csv')

# Convert date to datetime and set it as index
tweet_series["date"] = pd.to_datetime(tweet_series["date"])
tweet_series = tweet_series.set_index('date')

# Subset by years
tweet_years = [tweet_series[f'{i}'] for i in range(2017,2021)]

# Normalize the data
for e in tweet_years:
    Normalizador(e, "id")

# 3. Compare both time series and calculate the Pearson correlation
# Change the tweets index to date to allow the join with pollen data
for e in tweet_years:
    e.index = e.index.date

# Join the datasets by date
joined_list = []
for i in range(len(polen_years)):
    joined_list.append(polen_years[i].join(tweet_years[i], how='inner', lsuffix='pol_', rsuffix='twe_'))
    
# Calculate the Pearson correlation for each year
overall_pearson_r = [] 
for i in range(len(joined_list)):
    overall_pearson_r.append(joined_list[i].corr().iloc[3,5])

# Show the Pearson correlation values in a dataframe
pearson = pd.DataFrame(list(zip(list(range(2017,2021)),overall_pearson_r)), columns=["Year","Pearson"])
pearson