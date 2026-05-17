from lifelines import CoxPHFitter
from lifelines import CoxTimeVaryingFitter
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main() -> None:
    df = pd.read_csv('/content / directed_dyadic_war.csv')

    df['war_start'] = pd.to_datetime(df[['warstrtyr', 'warstrtmnth', 'warstrtday']].astype(str).agg('-'.join, axis=1), errors='coerce')

    df['war_end'] = pd.to_datetime(df[['warendyr', 'warendmnth', 'warenday']].astype(str).agg('-'.join, axis=1), errors='coerce')

    df['war_duration_days'] = (df['war_end'] - df['war_start']).dt.daysdf.to_csv('directed_dyadic_war_cleaned.csv', index=False)

    cph.fit(cox_df.drop(columns=['war_end']), duration_col='war_duration_days', event_col='event_observed')

    km_df['event_observed'] = 1

    km_df = km_df.dropna(subset=['war_duration_days', 'warolea'])

    kmf = KaplanMeierFitter()

    kmf.plot_survival_function(ci_show=False)

    plt.xlabel('Days Since War Start')

    plt.ylabel('Proportion of Wars Still Ongoing')

    plt.tight_layout()

    plt.savefig('km_warolea_survival.png')

    plt.show()

    cox_df['event_observed'] = 1

    cox_df = cox_df.dropna()

    cph.fit(cox_df, duration_col='batdths', event_col='event_observed')

    cox_df = df[['batdths', 'war_duration_days', 'statea', 'stateb']].copy()

    cox_df['event_observed'] = 1

    cox_df = cox_df.dropna()

    cph = CoxPHFitter()

    cph.fit(cox_df, duration_col='batdths', event_col='event_observed')

    cph.predict_survival_function(scenarios).plot()

    plt.title('Predicted Survival Curves for Battle Deaths')

    plt.xlabel('Battle Deaths')

    plt.ylabel('Proportion of Wars with ≤ Deaths')

    plt.tight_layout()

    plt.show()

    cph.check_assumptions(cox_df, p_value_threshold=0.05)

    cph.plot_partial_effects_on_outcome(covariates='war_duration_days', values=[100, 300, 600])

    # Assume df is your original DataFrame with one row per war# Create time - varying format: one row per (war, time interval)# Define function to expand war rows into time intervalsdef expand_war_rows(df, duration_col="batdths", interval = 30):records = []for idx, row in df.iterrows():duration = int(row[duration_col])if np.isnan(duration) or duration <= 0:continuesteps = int(np.ceil(duration / interval))for i in range(steps):start = i * intervalstop = min((i + 1) * interval, duration)
    event = int(stop == duration)
    records.append({"id": idx,"start": start,"stop": stop,"event": event,"war_duration_days": row["war_duration_days"],"statea": row["statea"],"stateb": row["stateb"],"month_index": i + 1,  # or log(stop), time since start})return pd.DataFrame(records)# Apply the transformationtv_df = expand_war_rows(df, duration_col="batdths", interval = 30)
    tv_df = tv_df.dropna()# Optional: encode states as categories (or leave numeric if not many)
    tv_df["statea"] = tv_df["statea"].astype("category")
    tv_df["stateb"] = tv_df["stateb"].astype("category")# Convert to dummies if categoricaltv_df = pd.get_dummies(tv_df, columns=["statea", "stateb"], drop_first = True)# Fit time - varying Cox modelctv = CoxTimeVaryingFitter()
    ctv.fit(tv_df, id_col="id", start_col="start", stop_col="stop", event_col="event")
    ctv.print_summary()

    MAX_STEPS = 50  # cap to avoid long wars creating massive rowsdef expand_war_rows(df, duration_col="batdths", interval = 30):records = []for idx, row in df.iterrows():try:duration = int(row[duration_col])except:continueif duration <= 0 or np.isnan(duration):continuesteps = min(MAX_STEPS, int(np.ceil(duration / interval)))for i in range(steps):start = i * intervalstop = min((i + 1) * interval, duration)
    event = int(stop == duration)
    records.append({"id": idx,"start": start,"stop": stop,"event": event,"war_duration_days": row["war_duration_days"],"statea": row["statea"],"stateb": row["stateb"],"month_index": i + 1,})return pd.DataFrame(records)
    df_subset = df[df["batdths"] < 20000].copy()
    tv_df = expand_war_rows(df_subset, duration_col="batdths", interval = 30)

    tv_df.head()

    ctv = CoxTimeVaryingFitter()

    ctv.fit(tv_df, id_col='id', start_col='start', stop_col='stop', event_col='event')

    ctv.print_summary()

    # Drop high - cardinality dummies (optional)
    cols_to_drop = [colfor col in tv_df.columnsif col.startswith("statea_") or col.startswith("stateb_")]tv_df = tv_df.drop(columns = cols_to_drop)

    tv_df_reduced = tv_df[['id', 'start', 'stop', 'event', 'war_duration_days', 'month_index']].copy()

    ctv = CoxTimeVaryingFitter(penalizer=0.01)

    ctv.fit(tv_df_reduced, id_col='id', start_col='start', stop_col='stop', event_col='event')

    ctv.print_summary()

    ctv.plot_partial_effects_on_outcome(covariates='war_duration_days', values=[100, 300, 600])

    plt.title('Effect of War Duration on Survival Curve (Battle Death Hazard)')

    plt.xlabel('Battle Deaths')

    plt.ylabel('Survival Probability')

    plt.tight_layout()

    plt.show()

    # Create hypothetical subjects for predictionscenarios = pd.DataFrame([{"id": 0,"start": 0,"stop": 1,"event": 0,"war_duration_days": 100,"month_index": 1,},{"id": 1,"start": 0,"stop": 1,"event": 0,"war_duration_days": 300,"month_index": 1,},{"id": 2,"start": 0,"stop": 1,"event": 0,"war_duration_days": 600,"month_index": 1,},])# Extend each scenario over time (e.g., 1 to 40 intervals)
    frames = []for idx, row in scenarios.iterrows():for t in range(1, 40):r = row.copy()
    r["start"] = t - 1r["stop"] = tr["month_index"] = tframes.append(r)
    scenario_df = pd.DataFrame(frames)# Predict survival functionsurv = ctv.predict_survival_function(scenario_df, id_col="id")# Plotplt.figure(figsize=(10, 6))for col in surv.columns:plt.plot(surv.index,surv[col],label = f"
    Duration = {int(scenarios.loc[col, 'war_duration_days'])}",)
    plt.title("Predicted Survival Curves by War Duration")
    plt.xlabel("Time Interval (months)")
    plt.ylabel("Probability War Has Not Reached Total Deaths")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Create example subjects at time t = 0
    durations = [100, 300, 600]all_surv = []for i, d in enumerate(durations):subject_rows = []for t in range(1, 41):  # simulate up to 40 monthssubject_rows.append({"id": i,"start": t - 1,"stop": t,"event": 0,"war_duration_days": d,"month_index": t,})
    subject_df = pd.DataFrame(subject_rows)
    subject_df["hazard"] = ctv.predict_partial_hazard(subject_df)
    cum_hazard = subject_df["hazard"].cumsum()
    surv = np.exp(-cum_hazard)
    all_surv.append((subject_df["stop"], surv, f"
    Duration = {d}"))# Plot simulated survival curvesplt.figure(figsize=(10, 6))for t, s, label in all_surv:plt.plot(t, s, label = label)
    plt.title("Simulated Survival Curves by War Duration")
    plt.xlabel("Time Interval (months)")
    plt.ylabel("Survival Probability")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
