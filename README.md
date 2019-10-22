# predi-home

## Project Abstract

An Cloud AI-driven embedded system that learns the discretized time-series state of a smart home to predict and automate sequences of states and actions via reinforcement learning on human-computer/appliance interactions. In particular, a neural net trains on the time-domain state of the smart home either through imitation learning on the behavior of the resident or reinforcement learning driven by minimizing a "control-override" loss function representing differences in the behavior of the resident and the predicted trajectory of the model, and periodically (daily, weekly, or monthly) update the smart home controller to reflect the changes in the smart home.

To design and prototype the system, I utilize either Open Smart Home Simulator (OpenSHS - https://github.com/openshs/openshs) or HomeIO (https://realgames.co/home-io/) with ConnectIO (https://docs.realgames.co/connectio/) to simulate and genenrate data of the trajectories of smart home residents and to control the smart home and process the data on an STM Nucleo (https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed through Mbed (https://www.mbed.com/en/), and Amazon Web Services (https://aws.amazon.com/) to train a real-time adaptive neural network that learns various time-domain functions for all the appliances/computers in the smart home via minimizing the loss of user overrides on aforementioned appliances/computers.

