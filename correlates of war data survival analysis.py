"""Survival analysis demo on synthetic war-duration data."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter


def main() -> None:
    rng = np.random.default_rng(42)
    n = 200
    duration = rng.exponential(300, size=n)
    event = rng.binomial(1, 0.7, size=n)
    battle_deaths = rng.poisson(50, size=n) + duration / 10
    df = pd.DataFrame(
        {
            "war_duration_days": duration,
            "batdths": battle_deaths,
            "event_observed": event,
        }
    )
    kmf = KaplanMeierFitter()
    kmf.fit(df["war_duration_days"], event_observed=df["event_observed"])
    kmf.plot_survival_function(ci_show=False)
    plt.xlabel("Days since war start")
    plt.ylabel("Survival probability")
    plt.title("Kaplan–Meier survival (synthetic)")
    plt.tight_layout()
    plt.savefig("km_survival.png", dpi=150)
    plt.show()
    cph = CoxPHFitter()
    cph.fit(df, duration_col="war_duration_days", event_col="event_observed")
    cph.print_summary()


if __name__ == "__main__":
    main()
