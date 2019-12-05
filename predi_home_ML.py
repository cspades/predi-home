import time
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier

# Sampling + Control Frequency in Seconds
# NOTE: T should preferably divide 60*60*24 to optimize
# performance and efficiency of prediction/adaptation.
# It is not crucially necessary, because the machine learning
# model will interpolate the temporal predictions.
T = 60 * 10
t_intervals = np.arange(0, 86400, T)

# Import training/history data.
df = pd.read_csv('milan_sched_1.txt', header=None)

# Construct training data.
X_train = df.copy()
X_train["Time"] = np.arange(t_intervals.shape[0])
Y_train = df.copy().iloc[np.arange(1-len(df), 1)]
Y_train.index = np.arange(len(df))

# Initialize Pre-Trained MLP Classifier
model = MLPClassifier(hidden_layer_sizes=(45, 45, 45), activation='relu', solver='adam', learning_rate_init=0.0047,
					  tol=0.5, max_iter=20000, n_iter_no_change=16400, random_state=0)

# Overfit.
t0 = time.time()
model.fit(X_train, Y_train)
t1 = time.time()
print("Training Time = ", t1 - t0)

# Re-calibrate model parameters for adaptation mode.
mlp_params = {
	'learning_rate_init': 0.0047,
	'max_iter': 100,
	'n_iter_no_change': 10,
	'warm_start': True,
	'verbose': False
}
model.set_params(**mlp_params)

# Adaptive run.
t0 = time.time()
X_train.iloc[40, 2] = 1
Y_train.iloc[40, 2] = 1
model.fit(X_train, Y_train)
t1 = time.time()
print("Adaptive Training Time = ", t1 - t0)

# Test.
preds = pd.DataFrame(model.predict(X_train))
print(((Y_train - preds) != 0).sum().sum())
pd.DataFrame(model.predict(X_train)).to_csv('temp', ',')
