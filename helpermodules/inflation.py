import pandas as pd
import re

def download_cpi_data(selected_countries = None):
    """
    Download CPI data from a CSV file and process it.

    Parameters:
        selected_country (list): A list of countries for which CPI data is requested. If provided,
            the function will return CPI data only for the selected countries. If not provided,
            data for all countries will be returned.

    Returns:
        pandas.DataFrame: CPI data for the selected countries (if provided) or for all countries.
    """

    cpi_df = pd.read_csv('Consumer_Price_Index_CPI.csv', delimiter=";")
    cpi_df = cpi_df.rename(columns={'Unnamed: 0': 'Country'})

    # Use years as indexes
    cpi_df = cpi_df.set_index('Country').T

    # Remove Russian data
    cpi_df = cpi_df.drop('Russian Federation', axis=1)

    years = list(cpi_df.index.values)
    countries = list(cpi_df.columns.values)


    # Convert "," to "." in the dataframe
    for year in years:
        for country in countries:
            el = str(cpi_df.loc[year].at[country])
            floated_value = float(re.sub(",", ".", el))
            cpi_df = cpi_df.replace(el, floated_value)

    # Return all the dataset or a subset of it
    if selected_countries:
        return cpi_df[selected_countries]
    else:
        return cpi_df


def apply_inflation_on_portfolio(portflio_df, selected_country):
    # date, amount, pct_change
    portfolio_with_inflation = pd.DataFrame()
    cpi_data = download_cpi_data(selected_country)

    dates = list(portflio_df.index())

    #Uso [:4] perchè il formato è YYYY-MM-DD
    start_year = int(dates[0][:4])
    end_year = int(dates[-1][:4])

    for year in range(start_year, end_year+1):
        # Divido per 12 l'inflazione annuale
        montly_inflation = cpi_data[year] / 12

        # Itera tutte le date, ogni volta agisci solo su quella dell'anno di interesse (perchè l'inflazione cambia anno per anno)
        for date in dates:
            if date[:4] == year:
                amount = portflio_df['Amount'][date]
                pct_change = portflio_df['Pct Change'][date]

                portflio_df['Amount'][date] = amount - amount*montly_inflation
                portflio_df['Pct Change'][date] = pct_change - montly_inflation
    
    return portflio_df
