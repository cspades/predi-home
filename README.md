![alt text](https://imgur.com/OCAhIp1.png)

# predi-home

## Abstract

A Cloud AI-driven embedded system that trains on the discretized time-series state trajectory of a smart home to predict and autonomously operate various features included within the smart home in real-time via imitation learning on human-computer/appliance interactions to improve the lifestyle, efficiency, and productivity of the resident(s) of the smart home.

In particular, a neural net trains on the sequence of states <img src="/tex/519c52325df920d2512a1dc8ca2b2c44.svg?invert_in_darkmode&sanitize=true" align=middle width=51.54129914999999pt height=27.6567522pt/> of the controllable features of the smart home and updates the autonomous smart home controller model to reflect changes/errors in the prediction of the following state <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/> given the previous state <img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/>, i.e. the control decision policy <img src="/tex/4a0c4241a5269c1a70e5796b918caa76.svg?invert_in_darkmode&sanitize=true" align=middle width=87.47151104999999pt height=24.65753399999998pt/> of the smart home, with minimal guidance from or interaction with the resident(s) of the smart home. To control the predictive autonomy of the smart home, an unsupervised algorithm (i.e., a dynamically-trained/updated k-means classifier) will differentiate a "checkpoint" subset of the past training data for the imitation learning model in order to group together approximately equivalent trajectories into classes that can be flexibly activated or deactivated in the re-training of the autonomous smart home controller.

## Project Objectives

1) **Imitation Learning** - Design and implement a smart home control algorithm that collects sufficient data on realistically-simulated periodic activities in the smart home, trains a imitation learning model in real-time to learn a predictive control decision policy for the state of features in the smart home via trial-and-error with respect to a loss function <img src="/tex/2874d0a4e49b8cb7fdca526541619a7e.svg?invert_in_darkmode&sanitize=true" align=middle width=108.90441704999998pt height=24.65753399999998pt/>, and applies the policy to control the smart home autonomously.

2) **Adaptive Control** - Optimize (as a function of the number of controllable features, the temporal granularity, and the distance between heuristically-distinct trajectories) the amount of time and computation necessary for the imitation learning model to functionally adapt to changes in activity patterns of various complexity in the smart home. Analyze trade-off between adaptation rate and predictive accuracy (calculated via regularly integrating the loss function of the imitation learning model over a fixed interval of time, intuitively based on conflicts between the prediction and human override/intervention), which depends on the learning rate of algorithm and controller.

Time permitting...

3) **Unsupervised Learning/Clustering** - Design and implement an efficient unsupervised learning algorithm that approximately differentiates smart home trajectory data into classes of trajectories for a checkpoint subset of past training data of fixed size N. Such information is summarized for the smart home resident(s), who can manually activate/deactivate specific classes of trajectories in the training data relative to activated/deactivated trajectories in order to rapidly adjust the training set or control the autonomy of the smart home. Analyze the impact re-training (and resetting the parameters of) the imitation learning algorithm on a checkpoint subset has on the performance of the imitation decision policy as a function of the checkpoint training memory N.

## Project Specifications and Methodology

To design and prototype the system, I utilize [HomeIO](https://realgames.co/home-io/) with [ConnectIO](https://docs.realgames.co/connectio/) to simulate the operation and generate data for the trajectories of the smart home.

To control the features of and actuate the predicted trajectory of the smart home, as well as communicate data between the smart home simulation and the Cloud, I will utilize an [STM Nucleo 32F446RE](https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed via [Mbed IDE](https://www.mbed.com/en/) and connected to [Amazon Web Services](https://aws.amazon.com/) to train an adaptive neural network that learns various control policies for all the appliances/computers in the smart home via [IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below) and [SageMaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below).

TODO - Imitation Learning - Training on data (with epoch = 1 and a fixed learning rate) in the state-transition form <img src="/tex/46be24a0d958ee8e99d747a8dd1b6ea5.svg?invert_in_darkmode&sanitize=true" align=middle width=108.63268844999999pt height=29.789954700000024pt/> to learn a control policy.

TODO - Adaptive Control - Analyze convergence of the policy for changes in human behavior, which can be interpreted as a trajectory/policy-tracking problem with sample loss on a stochastic process.

TODO - Unsupervised Learning - Clustering on data in the time-series form <img src="/tex/519c52325df920d2512a1dc8ca2b2c44.svg?invert_in_darkmode&sanitize=true" align=middle width=51.54129914999999pt height=27.6567522pt/> to classify state trajectories.

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

2) [CASAS: A Smart Home in a Box (2013)](https://ieeexplore.ieee.org/abstract/document/6313586)

3) [An Unsupervised User Behavior Prediction Algorithm Based on Machine Learning and Neural Network For Smart Home (2018)](https://ieeexplore.ieee.org/document/8458105)

These three papers provide a relatively comprehensive overview of smart home technology that are augmented with machine learning algorithms. Most practical applications of smart home predictive automation utilize unsupervised learning to analyze a dataset for approximately similar trajectories or sequences/patterns that can be applied to smart home control policies. Not many general distinctions/interpretations are made about how such information is used, so we can arbitrarily assume that the implementation of the policy is application-specific, some combination of control dependent on relevant/guiding input from human-computer interfaces, conservative pre-programmed algorithms on a case-by-case basis, and/or autonomously induced and generalized policies through optimization or ambient machine learning. In my project, the supervised component will focus on the third case (via imitation learning), while the unsupervised component will focus on the first case (via data summarization). Note that the second case (smart home programming) is perhaps the most effective, yet it is the least flexible/generalizable, as it is artificially designed through deterministic code by resourceful engineers with large amounts of smart home design experience and application-specific usage data on smart home resident(s) with simplifying assumptions on feature control policies. No machine learning is applied whatsoever, which makes it no different from any other technologically-empowered home. Other research and industry work is centered on the networking, hardware, and security perspectives of computation on the edge and cloud.

## Development Notebook

AWS models are not deployable on the Nucleo. Send control commands to the Nucleo via AWS IoT.

Opted to have the imitation learning problem search for a state-dependent control policy rather than a single optimal state trajectory, because control policies exceptionally improve the versatility and flexibility of the imitation learning model to sequential decision making and adaptation.

Observe that the imitation learning objective focuses on learning a general policy for the smart home, while the adaptive control objective focuses on the convergence of the model to a changed policy. Both are important in the autonomous performance of a smart home, because the former will determine an optimal policy minimize prediction errors for unprecedented sequences of states, while the latter will optimize how quickly such a policy is determined.

## Development Timeline

**Week 5** - Initiate setup for the hardware and software platforms of the system, with tests to communicate between PC (HomeIO/ConnectIO), STM Nucleo, and AWS IoT.

**Week 6** - Complete the software and hardware setup, program the smart home controller on the Nucleo/Mbed, and in consideration of the data structures, memory, communication latency, and the simulation API, roughly design the imitation learning algorithm to learn the control policy of the smart home on AWS Sagemaker.

**Week 7** - Design and code the imitation learning algorithm on AWS Sagemaker, and test/visualize it by training on simulated/generated trajectories of the smart home derived/sourced from reputable smart home usage databases or behavioral statistics (WSU CASAS). Validate the performance of the imitation learning model on real-time test data sampled from the training distribution.

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo.

**Week 9** - Close the loop and program the smart home control algorithm that collects/processes data from the simulation (Home/Connect-I/O), sends it to the Cloud (AWS IoT), retrieves the adaptive/learned policy (AWS Sagemaker), and control the smart home simulation (STM Nucleo).

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning and data summarization on the training dataset to extract approximately unique trajectories that the resident uses to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the repo on GitHub.

## Future Work

Re-training a neural net is not particularly efficient. Is it possible to efficiently un-train a neural net, perhaps via generating data that counteracts the impact of training on a set of data?

**Developed by Cory Ye, for the embedded systems course ECE M202A at UCLA.**
