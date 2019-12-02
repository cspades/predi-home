import sys
import time
import clr
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier

clr.AddReference('EngineIO')

from EngineIO import *

def compute_sec(s, m, h):
	return h * 3600 + m * 60 + s

print("Predi-Home is initializing...")

# Construct simulation control variables for HomeIO.
sim_output = {k: MemoryMap.Instance.GetBit(k, MemoryType.Output) for k in range(195)}
sim_time = MemoryMap.Instance.GetDateTime(0, MemoryType.Input)

# Sampling + Control Frequency in Seconds
# NOTE: T should preferably divide 60*60*24 to optimize
# performance and efficiency of prediction/adaptation.
# It is not crucially necessary, because the machine learning
# model will interpolate the temporal predictions.
T = 60 * 10
t_intervals = np.arange(0, 86400, T)

# Set Learned/Predicted Simulation Variable Index
var_index = [0, # A (0)
			 19, # B1 (1)
			 20, # B2 (2)
			 40, # D1 (3)
			 41, # D2 (4)
			 54, # E (5)
			 68, # F1 (6)
			 69, # F2 (7)
			 83, # G (8)
			 97, # H (9)
			 110, # I1 (10)
			 111, # I2 (11)
			 122, # J (12)
			 135, # K (13)
			 146, # L (14)
			 159, # M (15)
			 172, # N1 (16)
			 173, # N2 (17)
			 174, # N3 (18)
			 187, # O1 (19)
			 188, # O2 (20)
			 189, # OP (21)
			 190, # OG (22)
			 191] # OE (23)

# Import training/history data.
df = pd.read_csv('milan_sched_1.txt', header=None)

print("Maching Learning Pre-Training & Setup Phase Initiated.")

# Construct training data.
X_train = df.copy()
X_train["Time"] = np.arange(t_intervals.shape[0])
Y_train = df.copy().iloc[np.arange(1-len(df), 1)]
Y_train.index = np.arange(len(df))

# Initialize Pre-Trained MLP Classifier
model = MLPClassifier(hidden_layer_sizes=(45, 45, 45), activation='relu', solver='adam', learning_rate_init=0.0047,
					  tol=0.5, max_iter=20000, n_iter_no_change=16400)
# Overfit.
model.fit(X_train, Y_train)

# Re-calibrate model parameters for adaptation mode.
mlp_params = {
	'learning_rate_init': 0.0047,
	'max_iter': 100,
	'n_iter_no_change': 10,
	'warm_start': True,
	'verbose': False
}
model.set_params(**mlp_params)

# Construct adaptation data cache.
obs_hist = pd.DataFrame()

# Synchronize Timer & Initialize (Consistent) Smart-Home Variables
MemoryMap.Instance.Update()
t_sim = compute_sec(sim_time.Value.Second,
				sim_time.Value.Minute,
				sim_time.Value.Hour)
t_step = int(np.floor(t_sim / T)) + 1
for k in range(len(var_index)):
	sim_output[var_index[k]].Value = df.iloc[t_step - 1, k]
MemoryMap.Instance.Update()

print("Simulation control interface initiated.")

# Simulated Smart-Home Adaptive Control Algorithm
try:
	# Adaptive Sample + Control
	while True:
		# Extract Data from Simulation.
		MemoryMap.Instance.Update()
		# Update simulation time.
		t_sim = compute_sec(sim_time.Value.Second,
						sim_time.Value.Minute,
						sim_time.Value.Hour)
		# Periodic Sample + Control Delay @ Frequency 1/T
		# NOTE: Communication uncertainty interval of 20 seconds.
		if abs(t_sim - t_intervals[t_step]) > 10:
			# Insufficient time has passed. Skip.
			continue

		# Debug: Display Simulation Time
		print(sim_time.Value.ToString("HH:mm:ss"))

		# Extract simulation variables.
		obs_var = pd.DataFrame(data={k: [int(sim_output[var_index[k]].Value)] for k in range(len(var_index))})
		obs_var['Time'] = t_step
		obs_hist.append(obs_var, ignore_index=True)

		# Predict smart-home state with ML.
		pred_var = model.predict(obs_var)
		print("Time = ", t_step, "Predictions = ", pred_var)

		# Apply the predictive model to adjust the control variables of the simulation.
		for k in range(len(var_index)):
			sim_output[var_index[k]].Value = bool(np.array(pred_var)[0, k])

		# Control the simulation.
		MemoryMap.Instance.Update()
		print("Smart-Home Controller Actuated.")

		# Update the timer/CLK.
		t_step += 1
		if t_step >= t_intervals.size:
			# Reset timer/CLK.
			t_step = 0

			# Machine Learning - Partial/Warm Training and Adaptation
			# WARNING: Partial training delay requires sufficiently low control frequency,
			# or else the timer/CLK will lag by the excess training delay per cycle.
			print("Partial Training Initiated.")

			# Avoid training on corrupted data.
			if len(obs_hist) == t_intervals.shape[0]:

				# Construct training data.
				X_adapt = obs_hist.copy()
				Y_adapt = obs_hist.copy().iloc[np.arange(1 - len(df), 1)]
				Y_adapt.index = np.arange(len(df))

				# Train on recent data.
				model.fit(X_adapt, Y_adapt)

			# Clear the training cache.
			obs_hist = pd.DataFrame()

			print("Partial Training Completed.")

except KeyboardInterrupt:
	print("Simulation Terminated.")
	MemoryMap.Instance.Dispose()
	print("Memory Map Disposed.")
	time.sleep(3)