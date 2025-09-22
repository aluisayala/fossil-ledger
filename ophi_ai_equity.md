# 🌐import numpy as np
import pandas as pd

# Simulate the dataset from the user's description (only a subset shown, so we'll create synthetic full iterations of 128 samples)
# We'll approximate each iteration as small Gaussian noise around the given means.

iterations = {
    1: [0.589112, 2.916553, 0.004312, 0.998102, 1.014998, 0.021978],
    2: [0.607231, 2.947283, 0.003912, 0.998701, 1.016992, 0.018112],
    3: [0.624812, 2.976802, 0.004112, 0.997902, 1.013992, 0.017612],
    4: [0.643612, 3.009472, 0.004512, 0.998302, 1.018992, 0.018812],
    5: [0.663021, 3.041102, 0.004612, 0.998801, 1.015992, 0.019412],
    6: [0.682912, 3.072512, 0.004412, 0.998502, 1.013992, 0.019912],
    7: [0.702612, 3.103222, 0.004712, 0.998902, 1.012992, 0.019712],
    8: [0.722712, 3.134412, 0.004212, 0.999002, 1.011992, 0.020112],
    9: [0.742312, 3.163922, 0.004812, 0.998702, 1.009992, 0.019612],
    10:[0.761221, 3.192212, 0.004912, 0.998202, 1.010992, 0.018912]
}

# Generate synthetic samples with small noise
data = []
for it, means in iterations.items():
    for sid in range(1, 129):
        noisy = np.random.normal(loc=means, scale=np.array([1e-5,1e-5,1e-6,1e-6,1e-6,1e-6]))
        row = [it, sid] + noisy.tolist()
        data.append(row)

df = pd.DataFrame(data, columns=["iteration","sample_id","feature_1","feature_2","feature_3","feature_4","feature_5","feature_6"])

# Compute isotropy per iteration:
# Following OPHI spec: whiten each iteration's features, get eigenvalues of covariance, compute GM/AM ratio
def isotropy_metrics(subdf):
    X = subdf.iloc[:,2:].to_numpy()
    # mean-center
    X_centered = X - X.mean(axis=0)
    # covariance
    cov = np.cov(X_centered, rowvar=False)
    # eigenvalues
    eigvals = np.linalg.eigvalsh(cov)
    # avoid negatives due to numerical noise
    eigvals = np.clip(eigvals, 1e-12, None)
    gm = np.exp(np.mean(np.log(eigvals)))
    am = np.mean(eigvals)
    phi_iso = gm/am
    # per-sample isotropy fraction: check if max deviation from mean eigenvalue <= ε*mean
    eps = 0.05
    lam_mean = eigvals.mean()
    isotropic = np.all(np.abs(eigvals - lam_mean)/lam_mean <= eps)
    return phi_iso, isotropic

results = []
for it in sorted(df["iteration"].unique()):
    phi_iso, isotropic = isotropy_metrics(df[df["iteration"]==it])
    results.append({"iteration":it, "phi_iso":phi_iso, "F_iso": 1.0 if isotropic else 0.0})

results_df = pd.DataFrame(results)
results_df

