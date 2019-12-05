import time
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier

def df_diff(df1, df2):
	return (df1 != df2).astype(int).sum().sum()

T = 60 * 10
t_intervals = np.arange(0, 86400, T)

# Import training/history data synchronized to T.
df = pd.read_csv('milan_sched_1.txt', header=None)

# Adaptation Test - Override Training Data
df_override = pd.read_csv('kyoto_sched_1.txt', header=None)
adapt_test = True
err_graph = [] # Errors relative to adaptive dataset.
div_graph = [] # Errors relative to pre-trained dataset.

# Construct training data.
X_train = df.copy()
X_train["Time"] = np.arange(t_intervals.shape[0])
Y_train = df.copy().iloc[np.arange(1-len(df), 1)]
Y_train.index = np.arange(len(df))

X_adapt = df_override.copy()
X_adapt["Time"] = np.arange(t_intervals.shape[0])
Y_adapt = df_override.copy().iloc[np.arange(1-len(df_override), 1)]
Y_adapt.index = np.arange(len(df_override))

# Initialize Pre-Trained MLP Classifier for Reinforcement/Imitation Learning
mlp_params = {
	"hidden_layer_sizes": (45, 45, 45),
	"activation": 'relu',
	"solver": 'adam',
	"learning_rate_init": 0.002,
	"max_iter": 24000,
	"n_iter_no_change": 20000,
	"shuffle": True,
	"warm_start": True,
	"verbose": False,
	"random_state": 2589
}
model = MLPClassifier(**mlp_params)

# Overfit.
print("Pre-Training Phase.")
t0 = time.time()
model.fit(X_train, Y_train)
t1 = time.time()
print("Training Time = ", t1 - t0)

# Compute Prediction Error.
preds = [pd.DataFrame(model.predict(X_train[X_train["Time"] == 0]))]
preds[0]["Time"] = 1
for t in range(2, t_intervals.shape[0]):
	preds.append(pd.DataFrame(model.predict(preds[-1])))
	preds[-1]["Time"] = t
df_preds = pd.concat(preds, ignore_index=True)
df_preds.index = np.arange(1, t_intervals.shape[0])

# Compute (propagated) error in predictions.
error = df_diff(df_preds.drop(["Time"], axis=1), X_train.iloc[1:].drop(["Time"], axis=1))
print("Optimal Error =", error)

print("Adaptation Phase.")
for k in range(100):

	# Adapt.
	model.fit(X_adapt, Y_adapt)

	# Test.
	preds = [pd.DataFrame(model.predict(X_adapt[X_adapt["Time"] == 0]))]
	preds[0]["Time"] = 1
	for t in range(2, t_intervals.shape[0]):
		preds.append(pd.DataFrame(model.predict(preds[-1])))
		preds[-1]["Time"] = t
	df_preds = pd.concat(preds, ignore_index=True)
	df_preds.index = np.arange(1, t_intervals.shape[0])

	# Compute (propagated) error in predictions.
	discrep = df_diff(df_preds.drop(["Time"], axis=1), X_adapt.iloc[1:].drop(["Time"], axis=1))
	diverge = df_diff(df_preds.drop(["Time"], axis=1), X_train.iloc[1:].drop(["Time"], axis=1))
	err_graph.append(discrep)
	div_graph.append(diverge)
	print('Prediction Error = %d for cycle %d.' % (discrep, k))
	print('Divergence Measure = %d for cycle %d' % (diverge, k))

# Output predictions and error stats.
pd.DataFrame(model.predict(X_adapt)).to_csv('preds', ',')
pd.DataFrame(err_graph).to_csv('error_data', ',', index=False)
pd.DataFrame(div_graph).to_csv('divergence_data', ',', index=False)
print("Test completed.")
