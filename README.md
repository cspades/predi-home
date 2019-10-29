![alt text](https://imgur.com/OCAhIp1.png)

# predi-home

## Abstract

A Cloud AI-driven embedded system that learns the discretized time-series state trajectory of a smart home to predict and autonomously operate various features included within the smart home via imitation/behavioral learning on human-computer/appliance interactions to improve the lifestyle and productivity of the resident(s) of the smart home.

In particular, a neural net or XGBoost learner trains on the time-domain state trajectory of the controllable features of the smart home, and periodically (depending on the expected frequency bandwidth of the learned trajectory) updates the autonomous smart home controller model to reflect changes in the predicted state trajectory or autonomous policy of the smart home, with minimal guidance from or interaction with the resident(s) of the smart home. To control or limit the predictive autonomy of the smart home, an unsupervised algorithm (i.e., a dynamic k-means classifier) will differentiate the training dataset of the imitation learning algorithm in order to group together approximately equivalent trajectories into classes that can be flexibly activated or deactivated in the training of the smart home controller.

## Project Objectives

1) Design and implement a smart home control algorithm that collects sufficient data on realistically-simulated periodic activities in smart home, trains a machine learning model to predict the probabilistically-optimal trajectory of features in the smart home, and controls the smart home autonomously.

2) Optimize (as a function of the number of controllable features, the temporal granularity, and the distance between heuristically-distinct trajectories) the amount of time and computation necessary for the machine learning model to functionally adapt to changes in activity patterns of various complexity in the smart home. Analyze trade-off between adaptation rate and predictive accuracy (intuitively based on human override/intervention), which are dependent on the capacity/diversity of the training dataset, of the algorithm and controller.

3) Time permitting, design and implement an efficient unsupervised learning algorithm that approximately differentiates smart home trajectory data into classes of trajectories that the smart home resident(s) can activate or deactivate, to rapidly adjust the training set or control the autonomy of the smart home.

## Project Specifications and Methodology

To design and prototype the system, I utilize [HomeIO](https://realgames.co/home-io/) with [ConnectIO](https://docs.realgames.co/connectio/) to simulate the operation and generate data for the trajectories of the smart home.

To control the features of and actuate the predicted trajectory of the smart home, as well as communicate data between the smart home simulation and the Cloud, I will utilize an [STM Nucleo 32F446RE](https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed via [Mbed IDE](https://www.mbed.com/en/) and connected to [Amazon Web Services](https://aws.amazon.com/) to train an adaptive neural network or random forest that learns various time-domain functions for all the appliances/computers in the smart home via [IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below) and [SageMaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below).

## Tech & Resources

**Project Website** - [cspades / predi-home](https://cspades.github.io/predi-home/)

**STM Nucleo 32F446RE Development Board with Mbed OS** - [STM Nucleo 32F446RE](https://os.mbed.com/platforms/NUCLEO-L433RC-P/)

**ARM Mbed** - [ARM Mbed Online IDE](https://www.mbed.com/en/)

**Amazon Web Services** - [AWS IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below) and [AWS Sagemaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below) with [Sagemaker GitHub Examples](https://github.com/awslabs/amazon-sagemaker-examples)

**Connecting the STM Nucleo to AWS IoT** - [Tutorial - Nucleo with Mbed OS and AWS IoT](https://github.com/Klika-Tech/nucleo-aws-iot-demo/blob/master/doc/NUCLEO.md) with the [STM Nucleo WiFi Expansion Board](https://www.digikey.com/product-detail/en/stmicroelectronics/X-NUCLEO-IDW04A1/497-17209-ND/7056814)

**HomeI/O and ConnectI/O** - [HomeIO](https://realgames.co/home-io/) with [ConnectIO](https://docs.realgames.co/connectio/)

**Connecting HomeI/O to STM Nucleo via ConnectI/O** - [Advantech DAQ USB Node](https://buy.advantech.com/I-O-Devices-Communication/USB-IO-Modules-Multifunction-USB-Modules/model-USB-4704-AE.htm) with [Documentation](https://docs.realgames.co/connectio/usb-4704/)

**Smart Home Usage Statistics and Data** - [WSU CASAS Database](http://casas.wsu.edu/datasets/)

**TensorFlow and Keras** - [TensorFlow](https://www.tensorflow.org/) and [Keras](https://www.tensorflow.org/guide/keras)

## Prior Work in Smart Home Automation and Machine Learning

1) [IEEE Review of Smart Homes - Past, Present, and Future (2012)](https://ieeexplore.ieee.org/document/6177682)

2) [CASAS: A Smart Home in a Box (2013)](https://ieeexplore.ieee.org/abstract/document/6313586) - CASAS Activity Recognition and Activity-Specific Predictive Automation

3) [An Unsupervised User Behavior Prediction Algorithm Based on Machine Learning and Neural Network For Smart Home](https://ieeexplore.ieee.org/document/8458105)

These three papers provide a relatively comprehensive overview of smart home technology that are augmented with machine learning algorithms. Most practical applications of smart home predictive automation utilize unsupervised learning to analyze a dataset for approximately similar trajectories or sequences/patterns that can be applied to smart home control policies. Not many general distinctions/interpretations are made about how such information is used, so we can arbitrarily assume that the implementation of the policy is application-specific, some combination of actuation with input from human-computer interfaces, pre-defined programming on a case-by-case basis, and/or autonomously induced and generalized through optimization or machine learning. In my project, the supervised component will focus on the third case, while the unsupervised component will focus on the first case. Note that the second case is perhaps the most pragmatic, yet it is the least flexible/generalizable, as it is artificially designed through deterministic code by engineers with large amounts of application-specific usage data on smart home resident(s).

## Development Notebook

AWS models are not deployable on the Nucleo. Send control commands to the Nucleo via AWS IoT.

## Development Timeline

**Week 5** - Initiate setup for the hardware and software platforms of the system, with tests to communicate between PC (HomeIO/ConnectIO), STM Nucleo, and AWS IoT.

**Week 6** - Complete the software and hardware setup, program the smart home controller on the Nucleo/Mbed, and in consideration of the data structures, memory, communication latency, and the simulation API, roughly design the imitation learning regression algorithm on AWS Sagemaker.

**Week 7** - Design and code the imitation learning regression algorithm on AWS Sagemaker, and test/visualize it by training on simulated/generated trajectories of the smart home derived/sourced from reputable smart home usage databases or behavioral statistics (WSU CASAS).

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo.

**Week 9** - Close the loop and program the smart home control algorithm that collects/processes data from the simulation (Home/Connect-I/O), sends it to the Cloud (AWS IoT), retrieves the adaptive/learned trajectory (AWS Sagemaker), and control the smart home simulation (STM Nucleo).

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning and data summarization on the training dataset to extract approximately unique trajectories that the resident uses to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the GitHub.

**Developed by Cory Ye, for the embedded systems course ECE M202A at UCLA.**
