import pandas as pd
import fixed
import cProfile
from time_test_json import qc_data, rule_list, level_list
import pstats
from pstats import SortKey


def output(qc_data, rule_list, level_list):
    # Create a dictionary to hold dataframes for each level
    level_dataframes = {level: [] for level in range(1, 7)}

    # Process the JSON data and create dataframes
    for item in qc_data:
        for data_entry in item["datas"]:
            level = data_entry["level"]
            index = item["index"]
            value = data_entry.get("value", pd.NA)
            mean = data_entry.get("mean", pd.NA)
            sd = data_entry.get("sd", pd.NA)

            # Create a new dataframe with the required columns
            df_single = pd.DataFrame({
                "level": [level],
                "index": [index],
                "value": [value],
                "mean": [mean],
                "sd": [sd]
            })

            # Convert non-numeric values to NaN
            for column in df_single.columns:
                df_single[column] = pd.to_numeric(df_single[column], errors='coerce')

            # Append the dataframe to the list corresponding to its level
            df_cleaned = df_single.dropna()
            level_dataframes[level].append(df_cleaned)

    # Filter out empty dataframes and concatenate dataframes for each level
    final_dataframes = []
    for level, dfs in level_dataframes.items():
        if dfs:
            level_dataframe = pd.concat(dfs, ignore_index=True)
            final_dataframes.append(level_dataframe)

    # Empty list to store all the result dataframes
    result_store = []

    for dff in final_dataframes:
        if dff.size != 0:
            level_val = dff['level'].iloc[0]
            # Compute the results for the required levels
            if level_val in level_list:
                mean_series = dff['mean'].copy()
                std_series = dff['sd'].copy()
                df_single = dff[['index', 'value']].copy()
                fixed_res = fixed.fixed_comp(df_single, rule_list, mean_series, std_series)
                new_df = pd.concat([fixed_res, dff['level']], axis=1)

                result_store.append(new_df)

    if result_store:
        # Initialize an empty dictionary to store the JSON data
        json_data = {}

        # Reorganize the output the required format
        for i in range(len(result_store)):
            df = result_store[i]
            for index, row in df.iterrows():
                level_info = {
                    "level": row["level"],
                    "spcViolation": row["LevelViolation"]

                }

                if row['Index'] in json_data:
                    existing_levels = [item["level"] for item in json_data[row["Index"]]["result"]]
                    if row["level"] not in existing_levels:
                        json_data[row["Index"]]["result"].append(level_info)
                else:
                    json_data[row["Index"]] = {"index": row["Index"], "result": [level_info]}
    else:
        json_data = {}

    # Convert the final JSON data dictionary to JSON format
    final_json = list(json_data.values())

    return final_json


if __name__ == "__main__":
    cProfile.run("output(qc_data, rule_list, level_list)", 'restats')
    p = pstats.Stats('restats')
    p.sort_stats(SortKey.CUMULATIVE).print_stats(50)
