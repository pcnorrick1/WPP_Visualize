# Cleans the Raw WPP data from the UNPD Website to make plotting easier (https://population.un.org/wpp/Download/Standard/MostUsed/)
# Rafactoring into separate script for application speed
from pathlib import Path

import pandas as pd


def get_project_paths():
    root = Path(__file__).resolve().parent.parent  # project root
    data_raw = root / "data" / "raw"
    data_processed = root / "data" / "processed"
    data_processed.mkdir(parents=True, exist_ok=True)
    return data_raw, data_processed


def clean_data():
    data_raw, data_processed = get_project_paths()

    wpp_estimates_2022 = pd.read_csv(
        data_raw / "WPP_2022_Estimates_raw.csv", encoding="latin-1", low_memory=False
    )
    wpp_median_2022 = pd.read_csv(
        data_raw / "WPP_2022_Median_raw.csv", encoding="latin-1", low_memory=False
    )
    wpp_low_2022 = pd.read_csv(
        data_raw / "WPP_2022_Low_raw.csv", encoding="latin-1", low_memory=False
    )

    wpp_estimates_2024 = pd.read_csv(
        data_raw / "WPP_2024_Estimates_raw.csv", encoding="latin-1", low_memory=False
    )
    wpp_median_2024 = pd.read_csv(
        data_raw / "WPP_2024_Median_raw.csv", encoding="latin-1", low_memory=False
    )
    wpp_low_2024 = pd.read_csv(
        data_raw / "WPP_2024_Low_raw.csv", encoding="latin-1", low_memory=False
    )

    wpp_median_2022 = pd.concat([wpp_estimates_2022, wpp_median_2022])
    wpp_low_2022 = pd.concat([wpp_estimates_2022, wpp_low_2022])

    wpp_median_2024 = pd.concat([wpp_estimates_2024, wpp_median_2024])
    wpp_low_2024 = pd.concat([wpp_estimates_2024, wpp_low_2024])

    # Add indicator variable for which variant is used
    wpp_median_2022["Variant"] = "2022 Median"
    wpp_low_2022["Variant"] = "2022 Low"
    wpp_median_2024["Variant"] = "2024 Median"
    wpp_low_2024["Variant"] = "2024 Low"

    # Indicator variable for projection vs estimate
    wpp_median_2022["Projection"] = wpp_median_2022["Year"] > 2021
    wpp_low_2022["Projection"] = wpp_low_2022["Year"] > 2021
    wpp_median_2024["Projection"] = wpp_median_2024["Year"] > 2023
    wpp_low_2024["Projection"] = wpp_low_2024["Year"] > 2023

    # Rename Columns
    wpp_median_2022.rename(
        columns={"Region, subregion, country or area *": "Country"}, inplace=True
    )
    wpp_low_2022.rename(
        columns={"Region, subregion, country or area *": "Country"}, inplace=True
    )
    wpp_median_2024.rename(
        columns={"Region, subregion, country or area *": "Country"}, inplace=True
    )
    wpp_low_2024.rename(
        columns={"Region, subregion, country or area *": "Country"}, inplace=True
    )

    # Clean Data: Convert strings to numeric and drop NaNs
    cols = wpp_median_2022.columns.drop(
        [
            "Index",
            "Variant",
            "Country",
            "Notes",
            "Location code",
            "ISO3 Alpha-code",
            "ISO2 Alpha-code",
            "SDMX code**",
            "Type",
            "Parent code",
            "Year",
            "Variant",
        ]
    )

    wpp_median_2022.replace("...", 0, inplace=True)
    wpp_median_2022[cols] = wpp_median_2022[cols].apply(pd.to_numeric)

    wpp_median_2024.replace("...", 0, inplace=True)
    wpp_median_2024[cols] = wpp_median_2024[cols].apply(pd.to_numeric)

    wpp_low_2022.replace("...", 0, inplace=True)
    wpp_low_2022[cols] = wpp_low_2022[cols].apply(pd.to_numeric)

    wpp_low_2024.replace("...", 0, inplace=True)
    wpp_low_2024[cols] = wpp_low_2024[cols].apply(pd.to_numeric)

    # Drop Notes column
    wpp_median_2022 = wpp_median_2022.drop("Notes", axis="columns")
    wpp_low_2022 = wpp_low_2022.drop("Notes", axis="columns")

    wpp_median_2024 = wpp_median_2024.drop("Notes", axis="columns")
    wpp_low_2024 = wpp_low_2024.drop("Notes", axis="columns")

    wpp_median_2022.to_csv(data_processed / "WPP_2022_Median_clean.csv", index=False)
    wpp_low_2022.to_csv(data_processed / "WPP_2022_Low_clean.csv", index=False)

    wpp_median_2024.to_csv(data_processed / "WPP_2024_Median_clean.csv", index=False)
    wpp_low_2024.to_csv(data_processed / "WPP_2024_Low_clean.csv", index=False)


def main():
    try:
        clean_data()
    except Exception as e:
        print("Error cleaning: {e}")
        raise


if __name__ == "__main__":
    main()
