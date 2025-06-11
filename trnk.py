from collections import defaultdict
from scipy import stats
import numpy as np
import math
import pandas as pd
import sys

def calc_median(arr):
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    
    if n == 0:
        return None
        
    if n % 2 == 0:
        mid_right = n // 2
        mid_left = mid_right - 1
        return (sorted_arr[mid_left] + sorted_arr[mid_right]) / 2
    else:
        return sorted_arr[n // 2]

def get_ranked_list(arr, rank_for=None):
    if rank_for is None:
        rank_for = arr
    arr = sorted(arr)
    value_positions = defaultdict(list)
    for i, value in enumerate(arr, 1):
        value_positions[value].append(i)

    rank_dict = {}
    for value, positions in value_positions.items():
        rank_dict[value] = calc_median(positions)

    return [rank_dict[value] for value in rank_for]

def get_df_ranked_list(df, rank_for_df):
    values = sorted(df.iloc[:, 1])
    value_positions = defaultdict(list)
    for i, value in enumerate(values, 1):
        value_positions[value].append(i)

    rank_dict = {}
    for value, positions in value_positions.items():
        rank_dict[value] = calc_median(positions)

    rank_for_df['rank'] = [rank_dict[value] for value in rank_for_df.iloc[:, 1]]
    return rank_for_df

def effect_size_interpretation(effect_size):
    if effect_size < 0.20:
        return "Trivial"
    elif effect_size < 0.50:
        return "Small"
    elif effect_size < 0.80:
        return "Medium"
    elif effect_size < 1.30:
        return "Large"
    else:
        return "Very Large"

def trnk2(df1, df2, common):
    nA = len(df1[~df1.iloc[:, 0].isin(common)])
    nB = len(df2[~df2.iloc[:, 0].isin(common)])
    nC = len(common)
    n1 = len(df1)
    n2 = len(df2)

    combined_df = pd.concat([df1, df2], ignore_index=True)
    df1 = get_df_ranked_list(combined_df, df1)
    df2 = get_df_ranked_list(combined_df, df2)

    X1 = sum(df1['rank']) / len(df1)
    X2 = sum(df2['rank']) / len(df2)

    # XA = sum(df1[~df1.iloc[:, 0].isin(common)].iloc[:, 1]) / nA
    # XB = sum(df2[~df2.iloc[:, 0].isin(common)].iloc[:, 1]) / nB
    # X1C = sum(df1[df1.iloc[:, 0].isin(common)].iloc[:, 1]) / nC
    # X2C = sum(df2[df2.iloc[:, 0].isin(common)].iloc[:, 1]) / nC
    S1_2 = stats.tvar(df1['rank'])
    S2_2 = stats.tvar(df2['rank'])
    S1 = math.sqrt(S1_2)
    S2 = math.sqrt(S2_2)
    # SA_2 = stats.tvar(df1[~df1.iloc[:, 0].isin(common)].iloc[:, 1])
    # SB_2 = stats.tvar(df2[~df2.iloc[:, 0].isin(common)].iloc[:, 1])
    # S1C_2 = stats.tvar(df1[df1.iloc[:, 0].isin(common)].iloc[:, 1])
    # S2C_2 = stats.tvar(df2[df2.iloc[:, 0].isin(common)].iloc[:, 1])
    # S12 = np.cov(df1[df1.iloc[:, 0].isin(common)].iloc[:, 1], 
    #             df2[df2.iloc[:, 0].isin(common)].iloc[:, 1])[0, 1]
    
    # v1 = (nA - 1) + ((nA + nB + nC - 1)/(nA + nB + 2 * nC)) * (nA + nB)
    gamma = (S1_2 / n1 + S2_2 / n2) ** 2 / ((S1_2 / n1) ** 2 / (n1 - 1) + (S2_2 / n2) ** 2 / (n2 - 1))
    v2 = (nC - 1) + ((gamma - nC + 1) / (nA + nB + 2 * nC)) * (nA + nB)


    a = df1[df1.iloc[:, 0].isin(common)].iloc[:, 1]
    b = df2[df2.iloc[:, 0].isin(common)].iloc[:, 1]
    r = stats.pearsonr(get_ranked_list(a), get_ranked_list(b))[0]

    trnk2 = (X1 - X2) / np.sqrt(S1_2 / n1 + S2_2 / n2 - 2*r * (S1 * S2 * nC) / (n1 * n2)) 
    p_two_tailed = stats.t.sf(abs(trnk2), v2) * 2
    effect_size = trnk2 * 2 / math.sqrt(v2)

    return trnk2, p_two_tailed, effect_size_interpretation(effect_size)

if __name__ == "__main__":
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[2])
    common = list(set(df1.iloc[:, 0]).intersection(set(df2.iloc[:, 0])))

    ### Shapiro-Wilk test
    statistic1, p_value1 = stats.shapiro(df1.iloc[:, 1])
    statistic2, p_value2 = stats.shapiro(df2.iloc[:, 1])
    if p_value1 < 0.05:
        print(f"Shapiro-Wilk test | df1: not normally distributed | {p_value1}")
    else:
        print(f"Shapiro-Wilk test | df1: {p_value1}")
        
    if p_value2 < 0.05:
        print(f"Shapiro-Wilk test | df2: not normally distributed | {p_value2}")
    else:
        print(f"Shapiro-Wilk test | df2: {p_value2}")


    ### Anderson-Darling test
    statistic_ad1, critical_values1, significance_levels1 = stats.anderson(df1.iloc[:, 1])
    statistic_ad2, critical_values2, significance_levels2 = stats.anderson(df2.iloc[:, 1])
    if statistic_ad1 > critical_values1[2]:
        print(f"Anderson-Darling test | df1: not normally distributed | {statistic_ad1}")
    else:
        print(f"Anderson-Darling test | df1: {statistic_ad1}")
        
    if statistic_ad2 > critical_values2[2]:
        print(f"Anderson-Darling test | df2: not normally distributed | {statistic_ad2}")
    else:
        print(f"Anderson-Darling test | df2: {statistic_ad2}")


    ### Levene's test
    statistic, p_value = stats.levene(df1.iloc[:, 1], df2.iloc[:, 1])
    if p_value < 0.05:
        print(f"Levene's test | Significantly different variances | {p_value}")
    else:
        print(f"Levene's test | Not significantly different variances | {p_value}")

    print("TRNK2:")
    print(trnk2(df1, df2, common))
