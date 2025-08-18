import pandas as pd
from pycaret.classification import *
from pathlib import Path

# ---- Load your processed table (binary target) ----
# Expectation: one row per subject; columns = clinical features; target column = "Cancer_Positive"
df = pd.read_csv("PATH/TO/PROCESSED_TABLE.csv")  # <- replace with your local path

# ---- Setup PyCaret experiment ----
exp = setup(
    data=df,
    target="Cancer_Positive",
    session_id=42,
    train_size=0.8,
    fold=5,                     # 5-fold CV
    normalize=True,
    remove_multicollinearity=True,
    multicollinearity_threshold=0.95,
    feature_selection=True,
    silent=True,
    verbose=False,
)

# ---- Benchmark models ----
best = compare_models(sort="AUC")  # pick by CV AUC

# ---- Tune the best model ----
tuned = tune_model(best, optimize="AUC")

# ---- Evaluate, finalize, and make plots ----
evaluate_model(tuned)               # opens interactive dashboard (optional)
final = finalize_model(tuned)

# Save plots
out_dir = Path("ML"); out_dir.mkdir(exist_ok=True, parents=True)
plot_model(final, plot="auc", save=True)        # saves to ./AUC.png
plot_model(final, plot="feature", save=True)    # saves to ./Feature Importance.png

# Save model (optional)
save_model(final, (out_dir / "final_model").as_posix())
