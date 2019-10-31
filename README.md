![alt text](https://imgur.com/OCAhIp1.png)

# predi-home

## Abstract

Predi-Home is a Cloud AI-driven embedded system that trains on the discretized time-series state trajectory of a smart home to predict and autonomously operate various smart features (lights, remote-controlled doors, etc.) of the smart home in real-time via imitation learning on human-computer/appliance interactions, in order to improve the lifestyle, efficiency, and productivity of the resident(s) of the smart home.

In particular, a neural net trains on the sequence of states <img src="/tex/519c52325df920d2512a1dc8ca2b2c44.svg?invert_in_darkmode&sanitize=true" align=middle width=51.54129914999999pt height=27.6567522pt/> associated with controllable features of the smart home to determine a predictive decision policy <img src="/tex/877989f4305367f4d75870f7748bf343.svg?invert_in_darkmode&sanitize=true" align=middle width=87.47151104999999pt height=24.65753399999998pt/> for an autonomous smart home controller with minimal guidance from or interaction with the resident(s) of the smart home. To control the autonomy of the predictive controller, an unsupervised algorithm (i.e., a dynamically-trained k-means classifier) will differentiate a "checkpoint" subset of the past training data for the imitation learning model in order to group together approximately equivalent trajectories into classes that can be flexibly activated or deactivated in the re-training of the predictive controller.

In this project, we design and implement a simulated prototype of Predi-Home that learns to predict the activity of the lights and doors of a smart home in order to autonomously control the smart home in real-time.

## Project Objectives

1) **Imitation Learning** - Design and implement a smart home control algorithm that collects sufficient data on realistically-simulated periodic activities pertaining to controllable features and environment variables in the smart home, iteratively trains an imitation learning model in real-time to learn a predictive control decision policy <img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/> for controllable features in the smart home via trial-and-error, and applies the prediction policy to autonomously control smart features on behalf of resident(s) in the smart home.

2) **Adaptive Control and Performance Metrics** - Optimize the amount of time and computation necessary for the imitation learning model to functionally adapt to changes in activity patterns of various complexity in the smart home. Analyze trade-off between adaptation rate and predictive accuracy of the smart control algorithm, which depends on the learning rate <img src="/tex/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode&sanitize=true" align=middle width=10.57650494999999pt height=14.15524440000002pt/> of the neural net.

Time permitting...

3) **Unsupervised Learning/Clustering** - Design and implement an efficient unsupervised learning algorithm that approximately differentiates smart home trajectory data into classes of trajectories for a checkpoint subset of past training data of fixed size N. Such information is summarized for the smart home resident(s), who can manually activate/deactivate specific classes of trajectories in the training data in order to rapidly adjust the training set or control the autonomy of the smart home. Analyze the impact re-training (and necessarily resetting the parameters of) the neural net on a checkpoint subset has on the performance of the imitation decision policy as a function of the memory capacity of the checkpoint training set.

## Project Specifications and Methodology

To design and prototype the system, I utilize [HomeIO](https://realgames.co/home-io/) with [ConnectIO](https://docs.realgames.co/connectio/) to simulate the operation and generate data for the trajectories of the smart home.

To control the features of and actuate the predicted trajectory of the smart home, as well as communicate data between the smart home simulation and the Cloud, I will utilize an [STM Nucleo 32F446RE](https://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-mpu-eval-tools/stm32-mcu-mpu-eval-tools/stm32-nucleo-boards/nucleo-f446re.html#overview) programmed via [Mbed IDE](https://www.mbed.com/en/) and connected to [Amazon Web Services](https://aws.amazon.com/) to train an adaptive neural network that learns various control policies for all the appliances/computers in the smart home via [IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below) and [SageMaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below).

Smart home training/test data is retrieved or artificially designed with guidance from the [CASAS Database](http://casas.wsu.edu/datasets/).

**Imitation Learning** - Training iteratively on periodic batches of episodic data with <img src="/tex/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode&sanitize=true" align=middle width=14.433101099999991pt height=14.15524440000002pt/> controllable features in the state-transition form <img src="/tex/148bffe43630fdd86a4c3baa1d20561c.svg?invert_in_darkmode&sanitize=true" align=middle width=299.65779855pt height=33.14169870000001pt/> to learn a predictive control policy <img src="/tex/877989f4305367f4d75870f7748bf343.svg?invert_in_darkmode&sanitize=true" align=middle width=87.47151104999999pt height=24.65753399999998pt/>.

__Imitation Learning Algorithm__
1) Apply current prediction policy at the state <img src="/tex/4389550a116a2af0c3833b5131a6032a.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/> to actuate the predicted state <img src="/tex/006a3a9f529ab70dbe376ea324a8cb10.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=22.831056599999986pt/> for discrete time <img src="/tex/ffda4ec1e0671a575ef3fb5d5d09f18e.svg?invert_in_darkmode&sanitize=true" align=middle width=37.89941429999999pt height=22.648391699999998pt/>.
2) Wait until the following time-step <img src="/tex/628783099380408a32610228991619a8.svg?invert_in_darkmode&sanitize=true" align=middle width=34.24649744999999pt height=21.18721440000001pt/>.
3) Observe if the state has been changed from <img src="/tex/006a3a9f529ab70dbe376ea324a8cb10.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=22.831056599999986pt/> to the actual state <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/>.
4) Compute and backpropagate the error <img src="/tex/30810a549b7da85c0af38504267da7a7.svg?invert_in_darkmode&sanitize=true" align=middle width=131.54682914999998pt height=22.831056599999986pt/> in the neural net to update/train the prediction policy with the binary logistic regression cross-entropy loss <img src="/tex/ddcb483302ed36a59286424aa5e0be17.svg?invert_in_darkmode&sanitize=true" align=middle width=11.18724254999999pt height=22.465723500000017pt/>.
5) Repeat *ad infinitum* (as necessary to operate the smart home).

<p align="center"><img src="/tex/6d7650d652d761a1e075d5c955bc6038.svg?invert_in_darkmode&sanitize=true" align=middle width=596.43933195pt height=49.315569599999996pt/></p>

Input to the neural net is the smart home state (a mixed-value vector of controllable binary smart home features concatenated with relevant ambient/environmental states like discrete time <img src="/tex/ffda4ec1e0671a575ef3fb5d5d09f18e.svg?invert_in_darkmode&sanitize=true" align=middle width=37.89941429999999pt height=22.648391699999998pt/>), while the output to the neural net is the binary smart home feature component of the state vector (as the environment and time are either only controllable in a control-theoretic sense or not controllable by the smart home). Validation of the predictive control policy <img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/> via integrating the loss function <img src="/tex/ddcb483302ed36a59286424aa5e0be17.svg?invert_in_darkmode&sanitize=true" align=middle width=11.18724254999999pt height=22.465723500000017pt/> over a fixed episode/interval is computed over a test dataset randomly sampled from the training distribution.

**Adaptive Control and Performance Metrics** - Analyze the convergence of the policy for abrupt yet persistent changes in resident behavioral policy <img src="/tex/0a6644d8bd5d5fbd9ebfbfd64fa32457.svg?invert_in_darkmode&sanitize=true" align=middle width=79.89243404999999pt height=24.65753399999998pt/>, which can be interpreted as a trajectory/policy-tracking problem as the training distribution changes from <img src="/tex/16a38dbae81080cba27462ddc8d7d479.svg?invert_in_darkmode&sanitize=true" align=middle width=15.64102484999999pt height=14.15524440000002pt/> to <img src="/tex/aae1b6feeafd7e3ec5d4332582602094.svg?invert_in_darkmode&sanitize=true" align=middle width=14.29147829999999pt height=14.15524440000002pt/>, and optimize the learning rate <img src="/tex/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode&sanitize=true" align=middle width=10.57650494999999pt height=14.15524440000002pt/> of the neural net to maximize prediction accuracy with minimal training cycles for the adjusted distribution <img src="/tex/aae1b6feeafd7e3ec5d4332582602094.svg?invert_in_darkmode&sanitize=true" align=middle width=14.29147829999999pt height=14.15524440000002pt/>. Generate test data on two trivial classes of distributional devations with varying magnitude/distance of policy deviation: either a (small) proper subset of a constant trajectory deviates, or the trajectory persistently and abruptly changes into a different trajectory. Analyze when the policy <img src="/tex/68835ccb2379f41f2127d9c77ceecb21.svg?invert_in_darkmode&sanitize=true" align=middle width=32.16938339999999pt height=24.65753399999998pt/> converges to steady state (when the prediction error ceases to improve with further training for the specified distribution of trajectories <img src="/tex/11c596de17c342edeed29f489aa4b274.svg?invert_in_darkmode&sanitize=true" align=middle width=9.423880949999988pt height=14.15524440000002pt/>).

Overall adaptive performance <img src="/tex/36a8d573a1a3a200c5ff4ca44a210c03.svg?invert_in_darkmode&sanitize=true" align=middle width=52.92844754999998pt height=24.65753399999998pt/> of the imitation learning algorithm will be measured as a function of prediction error of a partially-trained policy <img src="/tex/5b44b4d5916aef26e5557864111f088c.svg?invert_in_darkmode&sanitize=true" align=middle width=94.54673084999997pt height=24.65753399999998pt/> for a test set representing sample state transition data of the changed trajectory <img src="/tex/9024f6031e0880224d0d7d07c31df83f.svg?invert_in_darkmode&sanitize=true" align=middle width=30.91566224999999pt height=22.465723500000017pt/> after a specified number of training cycles <img src="/tex/d32114988d174e858ef6e95ba6f471f0.svg?invert_in_darkmode&sanitize=true" align=middle width=40.519280999999985pt height=22.831056599999986pt/> for a test distribution of trajectories <img src="/tex/11c596de17c342edeed29f489aa4b274.svg?invert_in_darkmode&sanitize=true" align=middle width=9.423880949999988pt height=14.15524440000002pt/>. Assume that <img src="/tex/5425a59e2cd537c97632a635c655ca4c.svg?invert_in_darkmode&sanitize=true" align=middle width=47.542256849999994pt height=24.65753399999998pt/> is a fixed monotonic delay function that normalizes/evaluates the penalty of training delay as a function of <img src="/tex/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55596444999999pt height=22.831056599999986pt/>, with <img src="/tex/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55596444999999pt height=22.831056599999986pt/> bounded by the number of training cycles necessary for the policy to converge <img src="/tex/50bbc0f7c2f4476038cdc21186d410dc.svg?invert_in_darkmode&sanitize=true" align=middle width=86.12122364999999pt height=24.65753399999998pt/>.

<p align="center"><img src="/tex/ffcb9f515fd48a0e8d45f9da52d075c1.svg?invert_in_darkmode&sanitize=true" align=middle width=422.40551099999993pt height=59.178683850000006pt/></p>

Observe that smaller <img src="/tex/36a8d573a1a3a200c5ff4ca44a210c03.svg?invert_in_darkmode&sanitize=true" align=middle width=52.92844754999998pt height=24.65753399999998pt/> implies versatile performance of the adaptive imitation learning algorithm, because minimizing the test set loss minimizes <img src="/tex/36a8d573a1a3a200c5ff4ca44a210c03.svg?invert_in_darkmode&sanitize=true" align=middle width=52.92844754999998pt height=24.65753399999998pt/> yet the delay from the number of training epochs <img src="/tex/5425a59e2cd537c97632a635c655ca4c.svg?invert_in_darkmode&sanitize=true" align=middle width=47.542256849999994pt height=24.65753399999998pt/> penalizes/amplifies the loss if the imitation learning algorithm does not rapidly adapt. <img src="/tex/36a8d573a1a3a200c5ff4ca44a210c03.svg?invert_in_darkmode&sanitize=true" align=middle width=52.92844754999998pt height=24.65753399999998pt/> is a worst-case metric, because it takes the maximum of the performance of all partially-trained policies <img src="/tex/b34e5205a9ded8ac4bd36719aeddc8ff.svg?invert_in_darkmode&sanitize=true" align=middle width=39.24460319999999pt height=24.65753399999998pt/> as it converges to the optimal policy <img src="/tex/68835ccb2379f41f2127d9c77ceecb21.svg?invert_in_darkmode&sanitize=true" align=middle width=32.16938339999999pt height=24.65753399999998pt/>.

**Unsupervised Learning** - Clustering on checkpoint training data in the time-series form <img src="/tex/519c52325df920d2512a1dc8ca2b2c44.svg?invert_in_darkmode&sanitize=true" align=middle width=51.54129914999999pt height=27.6567522pt/> to classify state trajectories in an episode or period of time. Construct an index for the classes to the training data, and analyze the performance of the re-trained (or "recovered") policy after removing specified classes of trajectories from the checkpoint training set as a function of the memory capacity of the checkpoint training dataset <img src="/tex/9b325b9e31e85137d1de765f43c0f8bc.svg?invert_in_darkmode&sanitize=true" align=middle width=12.92464304999999pt height=22.465723500000017pt/>. In particular, validate if the predictive policy has arguably "un-learned" the deactivated activities with minimal degradation in performance for activated activities in controlling the features of the smart home.

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

These three papers provide a relatively comprehensive overview of smart home technology that are augmented with machine learning algorithms. Most practical applications of smart home predictive automation utilize unsupervised learning to analyze a dataset for approximately similar trajectories or sequences/patterns that can be applied to smart home control policies. Not many general distinctions/interpretations are made about how such information is used, so we can arbitrarily assume that the implementation of the policy is application-specific, some combination of control dependent on relevant/guiding input from human-computer interfaces, conservative pre-programmed algorithms on a case-by-case basis, and/or autonomously induced and generalized policies through optimization or ambient machine learning. In my project, the supervised component will focus on the third case (via imitation learning), while the unsupervised component will focus on the first case (via data summarization). Note that the second case (smart home programming) is perhaps the most effective, yet it is the least flexible/generalizable, as it is artificially designed through deterministic code by resourceful engineers with large amounts of smart home design experience and application-specific usage data on smart home resident(s) with simplifying assumptions on feature control policies. No machine learning is applied whatsoever, which makes it no different from any other technologically-empowered home. Other research and industry work is centered on the networking, hardware, and security perspectives of computation on the edge and cloud. Due to the lack of existing advanced smart homes and unsolved challenges in security/privacy, Predi-Home is a hypothetical yet groundbreaking application of machine imitation learning in smart homes.

## Development Notebook

AWS models are not deployable on the Nucleo. Send control commands to the Nucleo via AWS IoT.

Opted to have the imitation learning problem search for a state-dependent control policy rather than a single optimal state trajectory, because control policies exceptionally improve the versatility and flexibility of the imitation learning model to sequential decision making and adaptation.

Observe that the imitation learning objective focuses on learning a general policy for the smart home, while the adaptive control objective focuses on the convergence of the model to a changed policy. Both are important in the autonomous performance of a smart home, because the former will determine an optimal policy minimize prediction errors for unprecedented sequences of states, while the latter will optimize how quickly such a policy is determined.

Simulation data will not be painstakingly extracted from the simulation via ConnectI/O. With guidance from the CASAS dataset, I will instead artificially generate the simulation data for the subset of controllable smart home features that the neural net will learn, and utilize the simulation to analyze/visualize the performance of the predictive control policy <img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/>. In reality, the embedded system would be extracting simulation data in each training cycle, but I will accelerate/automate the training with larger time-ordered batches of training data that will iteratively train the neural net (as if the training data were individually extracted from the simulation).

## Development Timeline

**Week 5** - Initiate setup for the hardware and software platforms of the system, with tests to communicate between PC (HomeIO/ConnectIO), STM Nucleo, and AWS IoT.

**Week 6** - Complete the software and hardware setup, program the smart home controller on the Nucleo/Mbed, and in consideration of the data structures, memory, communication latency, and the simulation API, roughly design the imitation learning algorithm to learn the control policy of the smart home on AWS Sagemaker.

**Week 7** - Design and code the imitation learning algorithm on AWS Sagemaker, and test/visualize it by training on simulated/generated trajectories of the smart home derived/sourced from reputable smart home usage databases or behavioral statistics (WSU CASAS). Validate the performance of the imitation learning model on real-time test data sampled from the training distribution.

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo. 

**Week 9** - Close the loop and program the smart home control algorithm that collects/processes data from the simulation (Home/Connect-I/O), sends it to the Cloud (AWS IoT), retrieves the adaptive/learned policy (AWS Sagemaker), and control the smart home simulation (STM Nucleo).

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning and data summarization on the training dataset to extract approximately unique trajectories that the resident uses to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the repo on GitHub.

## Deliverables

Code/programs and design architecture for the STM Nucleo, ConnectI/O, and AWS that executes as designed if connected to a computer running HomeI/O or a compatible control API for smart homes.

## Future Work

Extend Predi-Home to control all digital and analog features/devices in a modern smart home. Add disruptive noise and compensating filters to the control algorithm. Test on actual smart homes.

Re-training a neural net is not particularly efficient. Is it possible to efficiently un-train a neural net, perhaps via generating data that counteracts the impact of training on a set of data?

**Developed by Cory Ye, for the embedded systems course ECE M202A at UCLA.**
