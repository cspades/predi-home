# predi-home

## Abstract / Objective

A Cloud AI-driven embedded system that learns the discretized time-series state trajectory of a smart home to predict and autonomously operate various features included within the smart home via behavioral cloning or reinforcement learning on human-computer/appliance interactions to improve the lifestyle and productivity of the resident(s) of the smart home.

In particular, a neural net or random forest trains on the time-domain state trajectory of the smart home through imitation learning on the state of controllable features of the smart home, and periodically (depending on the periodicity or frequency bandwidth of the learned trajectory) update the autonomous smart home controller to reflect changes in the predicted state trajectory or autonomous policy of the smart home, with minimal guidance from or interaction with the active resident(s) of the smart home.

## Project Specifications and Methodology

To design and prototype the system, I utilize HomeIO (https://realgames.co/home-io/) with ConnectIO (https://docs.realgames.co/connectio/) to simulate the operation and generate data for the trajectories of the smart home.

To control the features of and actuate the predicted trajectory of the smart home, as well as communicate data between the smart home simulation and the Cloud, I will utilize an STM Nucleo (https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed via Mbed (https://www.mbed.com/en/) and connected to Amazon Web Services (https://aws.amazon.com/) to train an adaptive neural network or random forest that learns various time-domain functions for all the appliances/computers in the smart home via IoT and SageMaker.

## Resources

**Project Website** - https://cspades.github.io/predi-home/

**Connecting the STM Nucleo to AWS IoT** - https://github.com/Klika-Tech/nucleo-aws-iot-demo/blob/master/doc/NUCLEO.md with the STM Nucleo WiFi Expansion Board (https://www.digikey.com/product-detail/en/stmicroelectronics/X-NUCLEO-IDW04A1/497-17209-ND/7056814)

**HomeI/O and ConnectI/O** - https://realgames.co/home-io/ and https://docs.realgames.co/connectio/

**Connecting HomeI/O to STM Nucleo via ConnectI/O** - Node: https://buy.advantech.com/I-O-Devices-Communication/USB-IO-Modules-Multifunction-USB-Modules/model-USB-4704-AE.htm with Documentation: https://docs.realgames.co/connectio/usb-4704/

**Smart Home Usage Statistics and Data** - TBD

## Development Timeline

**Week 5** - Set up the hardware and software platform for the system, with tests to communicate between PC (HomeIO/ConnectIO), STM Nucleo, and AWS IoT. (Purchase jumper/USB cables, a STM Nucleo WiFi Extension Board, and an Advantech USB node to interface with Home/ConnectI/O.)

**Week 6** - Complete the software and hardware setup, and in consideration of the data structures, memory, latency, and the simulation API, design the imitation learning algorithm on AWS.

**Week 7** - Design and code the ML algorithm on AWS, and test/visualize it by training on simulated/generated trajectories of the smart home derived/sourced from reputable smart home usage databases or behavioral research.

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo.

**Week 9** - Close the loop and code the smart home control algorithm that collects/processes data from the simulation, sends it to the Cloud (AWS), retrieves the adaptive/learned trajectory, and control the smart home simulation. (Note that at this point of the project, I will have experience with communicating data between the simulation environment, the STM Nucleo, and AWS IoT/Sagemaker, and perhaps will have partially completed this step of the Project.)

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning and data summarization on the training dataset to extract approximately unique trajectories that the resident uses to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the GitHub.
