# predi-home

## Abstract / Objective

A Cloud AI-driven embedded system that learns the discretized time-series state trajectory of a smart home to predict and automate sequences of states and actions via behavioral cloning or reinforcement learning on human-computer/appliance interactions. In particular, a neural net trains on the time-domain state of the smart home either through imitation learning on the actions of the resident, or alternatively/time permitting, (inverse) reinforcement learning to learn a state-action control policy (via RL) driven by minimizing a "control-override" loss function representing differences in the autonomous policy and learned behavior of the resident (generated via imitation for inverse RL), and periodically (depending on the periodicity or frequency of the learned trajectory) update the smart home controller to reflect changes in the predicted state trajectory or autonomous policy of the smart home.

## Project Specifications and Methodology

To design and prototype the system, I utilize either Open Smart Home Simulator (OpenSHS - https://github.com/openshs/openshs) or HomeIO (https://realgames.co/home-io/) with ConnectIO (https://docs.realgames.co/connectio/) to simulate and generate data of the trajectories of smart home residents.

To control/actuate the predictive model of the smart home and communicate data between the smart home simulation and the Cloud, I will utilize an STM Nucleo (https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed through Mbed (https://www.mbed.com/en/) and connected to Amazon Web Services (https://aws.amazon.com/) to train an adaptive neural network that learns various time-domain functions or policies for all the appliances/computers in the smart home.

## Resources

**Project Website** - https://cspades.github.io/predi-home/

**Connecting the STM Nucleo to AWS IoT** - https://github.com/Klika-Tech/nucleo-aws-iot-demo/blob/master/doc/NUCLEO.md with the STM Nucleo WiFi Expansion Board (https://www.st.com/content/st_com/en/products/ecosystems/stm32-open-development-environment/stm32-nucleo-expansion-boards/stm32-ode-connect-hw/x-nucleo-idw01m1.html#sample-and-buy)

**Connecting HomeI/O to STM Nucleo via ConnectI/O** - Node: https://buy.advantech.com/I-O-Devices-Communication/USB-IO-Modules-Multifunction-USB-Modules/model-USB-4704-AE.htm with Documentation: https://docs.realgames.co/connectio/usb-4704/

**Apprenticeship Learning via Inverse RL** - https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf (Note: Educational motivation, and only if I choose to use RL, which in this context is the less optimal algorithm compared to imitation learning. I will not be referencing the paper with complete generality of loss/reward function for inverse RL, since I have particular knowledge about the loss function I want to learn - the difference between the learned optimal trajectory and the trained policy-driven trajectory, which can be learned by canonical imitation learning. However, it covers some insightful topics pertaining to the relationship between inverse RL and RL.)

## Development Timeline

**Week 5** - Set up the hardware and software platform for the system, with tests to communicate between PC (HomeIO/ConnectIO/OpenSHS), STM Nucleo, and AWS. (Purchase WiFi board and potentially a USB node from Advantech depending on choice of OpenSHS or HomeI/O, in addition to pin and USB cables. Verify that the STM Nucleo is sufficient, since it is the weakest link of the project. EDIT: Verified!)

**Week 6** - Complete the software and hardware setup, and in consideration of the data structures, memory, latency, and the simulation API, design the imitation learning and/or reinforcement learning algorithm on AWS.

**Week 7** - Design and code the ML algorithm on AWS, and test/visualize it by training on simulated/generated trajectories of the smart home.

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo.

**Week 9** - Close the loop and code the smart home control algorithm that collects/processes data from the simulation, sends it to the Cloud (AWS), retrieves the adaptive/learned model, and control the smart home simulation.

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning on the training dataset to extract approximately unique smart home trajectories that the resident can use to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the GitHub.
