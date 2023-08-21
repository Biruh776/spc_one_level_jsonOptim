import pandas as pd
import spc_rules as sp1
from logging_config import logger


def fixed_comp(df, rule_list, mean_series, std_series):
    """
    Checks for SPC rule violations when the standard deviation and mean are fixed by the user.
    """
    index = "Index"
    data1 = "LevelValue"

    rename_dict = {
        'index': index,
        'value': data1,
    }

    df.rename(columns=rename_dict, inplace=True)
    val1 = df[data1]

    result = one_level(val1, rule_list, mean_series, std_series)
    result['Index'] = df['Index']

    return result


def one_level(val1, rules, mean_series, std_series):
    """
    :param val1: A pandas Series containing floats.
    :param rules: A list of SPC rules to be checked
    :param std: a list of mean values
    :param mean: a list of standard deviation values
    :return: A pandas Dataframe with columns 'Level1Value' and 'Level1Violation'
    """
    df = pd.DataFrame({'LevelValue': val1.astype(float), 'LevelViolation': ''})

    qc = sp1.Spc_quality_control(val1, mean_series, std_series)
    mapping1 = one_val_mappings()
    all_maps = all_rules()

    # Iterate over the rule list and call the corresponding methods
    for rule in rules:
        method_name = mapping1.get(rule)
        if method_name:
            method = getattr(qc, method_name, None)
            if method and callable(method):
                df.loc[method(), 'LevelViolation'] += rule + '|'

    # Added functionality to log a warning when unrecognized rule is provided
    if not hasattr(one_level, 'loop_executed'):
        for rule in rules:
            if rule not in all_maps:
                logger.warning("The provided rule list includes unrecognized rule names.")

        # Set the flag variable to indicate that the loop has been executed
        one_level.loop_executed = True

    return df


def one_val_mappings():
    rule_mapping_one = {
        '1-2s': 'r1_2s',
        '1-2.5s': 'r1_25s',
        '1-3s': 'r1_3s',
        '1-3.5s': 'r1_35s',
        '1-4s': 'r1_4s',
        '1-5s': 'r1_5s',
        '2-2s': 'r2_2s',
        'R-4s': 'r4_s',
        '3-1s': 'r3_1s',
        '4-1s': 'r4_1s',
        '7-T': 'r7_T',
        '7-x': 'r7_x',
        '8-x': 'r8_x',
        '9-x': 'r9_x',
        '10-x': 'r10_x',
        '12-x': 'r12_x'
    }
    return rule_mapping_one


def all_rules():
    rule_mapping_all = ["1-2s", "1-2.5s", "1-3s", "1-3.5s", "1-4s", "1-5s", "2-2s", "R-4s", "3-1s", "4-1s",
                        "7-T", "7-x", "8-x", "9-x", "10-x", "12-x"]

    return rule_mapping_all
