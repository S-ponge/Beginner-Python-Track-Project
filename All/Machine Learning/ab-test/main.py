import numpy as np
import pandas as pd
import scipy.stats as st
from statsmodels.stats.power import tt_ind_solve_power
import matplotlib.pyplot as plt

df = pd.read_csv("ab_test.csv", parse_dates=["date"])


def hypothesis_test(sample1, sample2):
    stat, p_value = st.levene(sample1, sample2)
    vars_eq = True if p_value > 0.05 else False
    print("Levene's test")
    print(f"w = {round(stat, 3)}, {'p-value > 0.05' if vars_eq else 'p-value <= 0.05'}")
    print(f"Reject null hypothesis: {'no' if vars_eq else 'yes'}")
    print(f"Variances are equal: {'yes' if vars_eq else 'no'}")

    t_stat, t_p_value = st.ttest_ind(sample1, sample2, equal_var=vars_eq)
    print("\nT-test")
    print(f"t= {round(t_stat, 3)}, {'p-value > 0.05' if t_p_value > 0.05 else 'p-value <= 0.05'}")
    print(f"Reject null hypothesis: {'no' if t_p_value > 0.05 else 'yes'}")
    print(f"Means are equal: {'yes' if t_p_value > 0.05 else 'no'}")


def calculate_sample_size():
    ss = tt_ind_solve_power(0.2, power=0.8, alpha=0.05)
    ss = int(round(ss, -2))
    print(f"Sample size: {ss}")
    cg, eg = df.group.value_counts()
    print(f"Control group: {cg}\nExperimental group: {eg}")


def exp_data_analysis():  # Exploratory data analysis
    df.date = df.date.dt.day
    df.pivot_table(index="date",
                   columns="group",
                   aggfunc="size").plot.bar(xlabel="June", ylabel="Number of sessions")
    plt.show()
    plt.clf()
    df["order_value"].hist(by=df.group)
    plt.show()
    plt.clf()
    df["session_duration"].hist(by=df.group)
    plt.show()
    plt.clf()
    new_df = remove_outliers(df)
    print(f"Mean: {round(new_df.order_value.mean(), 2)}")
    print(f"Standard deviation: {round(new_df.order_value.std(ddof=0), 2)}")
    print(f"Max: {round(new_df.order_value.max(), 2)}")


def mann_whitney_u_test():
    new_df = remove_outliers(df)
    eg, cg = [x for _, x in new_df.groupby(new_df["group"] == "Control")]
    u1, p = st.mannwhitneyu(cg.order_value, eg.order_value)
    p_bool = True if p <= 0.05 else False
    print("Mann-Whitney U test")
    print(f"U1 = {u1}, p-value {'<= 0.05' if p_bool else '> 0.05'}")
    print(f"Reject null hypothesis: {'yes' if p_bool else 'no'}\n"
          f"Distributions are same: {'no' if p_bool else 'yes'}")


def parametric_test():
    new_df = remove_outliers(df)
    plot_data = np.log(new_df.loc[:, "order_value"])
    plot_data.hist(label="log_order_value")
    plt.xlabel("Log order value")
    plt.legend()
    plt.show()
    log_control = np.log(new_df.loc[new_df.group == "Control", "order_value"])
    log_experimental = np.log(new_df.loc[new_df.group == "Experimental", "order_value"])
    hypothesis_test(log_control, log_experimental)


def remove_outliers(dataset):
    order_quantile = dataset["order_value"].quantile(0.99)
    session_quantile = dataset["session_duration"].quantile(0.99)
    return dataset[(dataset.order_value <= order_quantile) & (dataset.session_duration <= session_quantile)]


parametric_test()
