![alt text](https://imgur.com/OCAhIp1.png) 

# predi-home

## Abstract

Predi-Home is a Cloud AI-driven embedded system that trains on the discretized time-series state trajectory of a smart home to predict and autonomously operate various smart features (lights, remote-controlled doors, etc.) of the smart home in real-time via imitation learning on human-computer/appliance interactions, in order to improve the lifestyle, efficiency, and productivity of the resident(s) of the smart home.

In particular, a cloud-based neural net trains on the sequence of states $$\{s_t\}_{t=1}^{N}$$ associated with controllable features of the smart home to determine a predictive decision policy $$\pi(s_t) =  \hat{s}_{t+1}$$ for an autonomous smart home controller with minimal guidance from or interaction with the resident(s) of the smart home. To control the autonomy of the predictive controller, an unsupervised algorithm (i.e., a dynamically-trained k-means classifier) will differentiate a "checkpoint" subset of the past training data for the imitation learning model in order to group together approximately equivalent trajectories into classes that can be flexibly activated or deactivated in the re-training of the predictive controller.

In this project, we design and implement a simulated prototype of Predi-Home that learns to predict the activity of the lights and doors of a smart home in order to autonomously control the smart home in real-time.

## Project Objectives

1) **Imitation Learning** - Design and implement a smart home control algorithm that collects sufficient data on realistically-simulated periodic activities pertaining to controllable features and environment variables in the smart home, iteratively trains an imitation learning model in real-time to learn a predictive control decision policy $$\pi$$ for controllable features in the smart home via trial-and-error, and applies the prediction policy to autonomously control smart features on behalf of resident(s) in the smart home.

2) **Adaptive Control and Performance Metrics** - Optimize the amount of time and computation necessary for the imitation learning model to functionally adapt to changes in activity patterns of various complexity in the smart home. Analyze trade-off between adaptation rate and predictive accuracy of the smart control algorithm, which depends on the learning rate $$\alpha$$ of the neural net.

Time permitting...

3) **Unsupervised Learning/Clustering** - Design and implement an efficient unsupervised learning algorithm that approximately differentiates smart home trajectory data into classes of trajectories for a checkpoint subset of past training data of fixed size N. Such information is summarized for the smart home resident(s), who can manually activate/deactivate specific classes of trajectories in the training data in order to rapidly adjust the training set or control the autonomy of the smart home. Analyze the impact re-training (and necessarily resetting the parameters of) the neural net on a checkpoint subset has on the performance of the imitation decision policy as a function of the memory capacity of the checkpoint training set.

## Project Specifications and Methodology

![alt text](https://imgur.com/7zVWSiT.png)

To design and prototype the system, I utilize [HomeIO](https://realgames.co/home-io/) to simulate and control the features of the smart home.

To communicate data between the smart home simulation on HomeI/O and the machine learning algorithm trained/deployed on the [Amazon Web Services](https://aws.amazon.com/) Cloud, I will program a control and data processing relay via the Python-HomeI/O SDK that executes on a PC (Dell XPS 15) and is connected to [AWS IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below).

To train an adaptive neural network that learns predictive control policies for all the appliances/computers in the smart home on the Cloud, I will utilize [AWS SageMaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below).

Smart home training/test data is retrieved or artificially designed with guidance from the [CASAS Database](http://casas.wsu.edu/datasets/).

**Edge-Cloud Control Loop of the System**

1) Observe the state of the smart home $$s_{t}$$ at the Edge.

2) Send the state $$s_{t}$$ to the trained control policy on the Cloud.

3) Compute the prediction for the following state $$\hat{s}_{t+1}$$ on the Cloud.

4) Send the predicted state $$\hat{s}_{t+1}$$ to the Edge.

5) Actuate the predicted state $$\hat{s}_{t+1}$$ in the smart home at the Edge.

**Imitation Learning** - Training iteratively on periodic batches of episodic data with $$m$$ controllable features in the state-transition form $$\{(s_t, s_{t+1})\}_{t=1}^{N-1} \subset \left(\left\{ 0,1 \right\}^m \times \left\{ 1, \dots, N \right\}\right)^2$$ to learn a predictive control policy $$\pi(s_t) =  \hat{s}_{t+1}$$.

__Imitation Learning Algorithm__
1) Apply current prediction policy at the state $$s_{t}$$ to actuate the predicted state $$\hat{s}_{t+1}$$ for discrete time $$t \in \mathbb{N}$$.
2) Wait until the following time-step $$t+1$$.
3) Observe if the state has been changed from $$\hat{s}_{t+1}$$ to the actual state $$s_{t+1}$$.
4) Compute and backpropagate the error $$e_{t+1} = \hat{s}_{t+1} - s_{t+1}$$ in the neural net to update/train the prediction policy with the binary logistic regression cross-entropy loss $$L$$.
$$
L \left( \hat{s}_t, s_{t} \right) =  - \left( \sum_{k=1}^m s_{t,k} \log [\sigma(\hat{s}_{t,k})] + (1 - s_{t,k}) \log[1 - \sigma(\hat{s}_{t,k})] \right) \qquad \left( \sigma(x) = \frac{1}{1 + e^{-x}} \right)
$$
5) Repeat *ad infinitum* (as necessary to operate the smart home).

Input to the neural net is the smart home state (a mixed-value vector of controllable binary smart home features concatenated with relevant ambient/environmental states like discrete time $$t \in \mathbb{N}$$), while the output to the neural net is the binary smart home feature component of the state vector (as the environment and time are either only controllable in a control-theoretic sense or not controllable by the smart home). Validation of the predictive control policy $\pi$ is computed via integrating the loss function $$L$$ over an episodic test dataset $$V_{\text{test}}$$ randomly sampled from the training distribution in order to compute the prediction error $$E(\pi)$$.
$$
E(\pi) = \sum_{(s_t, s_{t+1}) \in V_{\text{test}}} L \left( \pi_d(s_t), s_{t+1} \right) \right\}
$$
An alternative policy prediction measure can be defined as $$Q(\pi,N) = \frac{mN - \left|\left\{ \text{incorrect prediction of feature $$k$$ at time $$t$$} \right\}\right|}{mN}$$, which computes the prediction accuracy in the episode of length $$N$$.

**Adaptive Control and Performance Metrics** - Analyze the convergence of the policy for abrupt yet persistent changes in resident behavioral policy $$\pi(\gamma_a \to \gamma_b)$$, which can be interpreted as a trajectory/policy-tracking problem as the training distribution changes from $$\gamma_a$$ to $$\gamma_b$$, and optimize the learning rate $$\alpha$$ of the neural net to maximize prediction accuracy with minimal training cycles for the adjusted distribution $$\gamma_b$$. Generate test data on two trivial classes of distributional devations with varying magnitude/distance of policy deviation: either a (small) subset of a constant trajectory deviates, or a constant trajectory switches to another constant trajectory with no policy intersection. Analyze when the policy $$\pi(\gamma)$$ converges to steady state (when the prediction error ceases to improve with further training on the specified distribution $$\gamma$$).

Overall adaptive performance $$P(\alpha,\gamma)$$ of the imitation learning algorithm will be measured as a function of prediction error of a partially-trained policy $$\pi_d(s_t) =  \hat{s}_{t+1}$$ for a test set representing sample state transition data of the changed trajectory $$V_{\text{test}}$$ after a specified number of training cycles $$d \in \mathbb{N}$$ for a test distribution of trajectories $$\gamma$$. Assume that $$\kappa(d,\gamma)$$ is a fixed monotonically increasing delay function that normalizes/evaluates the penalty of training delay as a function of $$d$$, with $$d$$ bounded by the number of training cycles necessary for the (binary) policy to converge $$D(\alpha,\gamma) \in \mathbb{N}$$.
$$
P(\alpha,\gamma) = \max_{d < D(\alpha,\gamma)} \left\{ \kappa(d,\gamma) \cdot \sum_{(s_t, s_{t+1}) \in V_{\text{test}}} L \left( \pi_d(s_t), s_{t+1} \right) \right\}
$$
Observe that smaller $$P(\alpha,\gamma)$$ implies versatile performance of the adaptive imitation learning algorithm, because minimizing the integrated test loss $$\sum L$$ minimizes $$P(\alpha,\gamma)$$ yet the training delay penalty $$\kappa(d,\gamma)$$ penalizes/amplifies the loss if the imitation learning algorithm does not rapidly adapt. $$P(\alpha,\gamma)$$ is a worst-case metric, because it takes the maximum of the performance of all partially-trained policies $$\pi_d(\gamma)$$ as it converges to the optimal policy $$\pi(\gamma)$$.

**Unsupervised Learning** - Clustering on checkpoint training data in the time-series form $$\{s_t\}_{t=1}^{N}$$ to classify state trajectories in an episode or period of time. Construct an index for the classes to the training data, and analyze the performance of the re-trained (or "recovered") policy after removing specified classes of trajectories from the checkpoint training set as a function of the memory capacity of the checkpoint training dataset $$C$$. In particular, validate if the predictive policy has arguably "un-learned" the deactivated activities with minimal degradation in performance for activated activities in controlling the features of the smart home.

## Tech & Resources

**Project Website** - [cspades / predi-home](https://cspades.github.io/predi-home/)

**Amazon Web Services** - [AWS IoT](https://aws.amazon.com/iot-core/?hp=tile&so-exp=below) and [AWS Sagemaker](https://aws.amazon.com/sagemaker/?hp=tile&so-exp=below) with [Sagemaker GitHub Examples](https://github.com/awslabs/amazon-sagemaker-examples)

**AWS-Python SDK** [Python to AWS IoT](https://github.com/aws/aws-iot-device-sdk-python) and [AWS Toolkit for PyCharm](https://github.com/aws/aws-iot-device-sdk-python)

**HomeI/O** - [HomeIO](https://realgames.co/home-io/) and [HomeI/O Documentation w/ Python SDK](https://docs.realgames.co/homeio/en/)

**Smart Home Usage Statistics and Data** - [WSU CASAS Database](http://casas.wsu.edu/datasets/)

**TensorFlow and Keras** - [TensorFlow](https://www.tensorflow.org/) and [Keras](https://www.tensorflow.org/guide/keras)

## Prior Work in Smart Home Automation and Machine Learning

1) [IEEE Review of Smart Homes - Past, Present, and Future (2012)](https://ieeexplore.ieee.org/document/6177682)

2) [CASAS: A Smart Home in a Box (2013)](https://ieeexplore.ieee.org/abstract/document/6313586)

3) [Learning Activity Predictors from Sensor Data: Algorithms, Evaluation, and Applications (2017)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8031060)

4) [An Unsupervised User Behavior Prediction Algorithm Based on Machine Learning and Neural Network For Smart Home (2018)](https://ieeexplore.ieee.org/document/8458105)

These four papers provide a relatively comprehensive overview of smart home technology that are augmented with machine learning algorithms. (3) is practically similar in algorithm design to Predi-Home. Most practical applications of smart home predictive automation utilize unsupervised learning to analyze a dataset for approximately similar trajectories or sequences/patterns that can be applied to smart home control policies. Not many general distinctions/interpretations are made about how such information is used, so we can arbitrarily assume that the implementation of the policy is application-specific, some combination of control dependent on relevant/guiding input from human-computer interfaces, conservative pre-programmed algorithms on a case-by-case basis, and/or autonomously induced and generalized policies through optimization or ambient machine learning. In my project, the supervised component will focus on the third case (via imitation learning), while the unsupervised component will focus on the first case (via data summarization). Note that the second case (smart home programming) is perhaps the most effective, yet it is the least flexible/generalizable, as it is artificially designed through deterministic code by resourceful engineers with large amounts of smart home design experience and application-specific usage data on smart home resident(s) with simplifying assumptions on feature control policies. No machine learning is applied whatsoever, which makes it no different from any other technologically-empowered home. Other research and industry work is centered on the networking, hardware, and security perspectives of computation on the edge and cloud.

## Development Notebook

1) Assuming that the edge computer/controller is limited in memory and compute, assume that machine learning algorithms/models cannot be trained/deployed on the PC. Consequently, we simulate the existence of an embedded system on the edge via training and deploying the machine learning component on the AWS Cloud. (Note: AWS implementation is in-progress, and will not be included in the project.)

2) Opted to have the imitation learning problem search for a state-dependent control policy rather than a single optimal state trajectory, because control policies exceptionally improve the versatility and flexibility of the imitation learning model to sequential decision making and adaptation.

3) Observe that the imitation learning objective focuses on learning a general policy for the smart home, while the adaptive control objective focuses on the convergence of the model to a changed policy. Both are important in the autonomous performance of a smart home, because the former will determine an optimal policy minimize prediction errors for unprecedented sequences of states, while the latter will optimize how quickly such a policy is determined.

4) Simulation datasets will not be painstakingly extracted from HomeI/O. With guidance from the CASAS dataset, I will instead artificially generate the simulation data for the subset of controllable smart home features that the neural net will learn, and exclusively utilize the simulation to analyze/visualize the performance of the predictive control policy $\pi$ in real-time. In reality, the embedded system would be extracting simulation data in each training and prediction cycle, yet instead I will accelerate/automate the training phase of the cycle with larger time-ordered batches of training data that will sequentially/iteratively train the neural net (as if the training data were individually extracted from the simulation). However, deploying the prediction policy will be synchronized in closed loop to emulate the actual operation of the cloud-computed predictive controller.

5) HomeI/O simulation control access is limited to one interface, so it is not (currently) possible to define access privileges and have human override in the loop with the control algorithm.

## Development Timeline

**Week 5** - Initiate setup for the software platform of the system, with tests to communicate between PC (HomeIO) and AWS IoT.

**Week 6** - Debug the software setup, program the smart home controller on Python, and in consideration of the data structures, memory, communication latency, and the simulation API, roughly design the imitation learning algorithm to learn the control policy of the smart home on AWS Sagemaker.

**Week 7** - Design and code the imitation learning algorithm on AWS Sagemaker, and test/visualize it by training on simulated trajectories of the smart home derived/sourced from reputable smart home resident behavioral statistics databases (WSU CASAS). Validate the performance of the imitation learning model on real-time test data sampled from the training distribution.

**Week 8** - Extra time in case of delayed development, as well as prepare for the Demo. 

**Week 9** - Close the loop and program the smart home control algorithm that extracts/processes data from the simulation (HomeI/O), sends it to the Cloud (AWS IoT), retrieves the adaptive/learned policy (AWS Sagemaker), and control the smart home simulation (Python).

**Week 10** - Debug/optimize the control and ML algorithm(s), and prepare auxiliary materials (report, video, website, etc.) for the Project. Study the possibility of applying unsupervised learning and data summarization on the training dataset to extract approximately unique trajectories that the resident uses to customize the autonomy of the smart home.

**Finals Week** - Complete the Project and fork/clone the repo on GitHub.

## Deliverables and Repository Contents

Code/programs and design architecture for Predi-Home, including supporting control, data processing, and communication programs in Python, and the training/deployment code for the neural net on AWS that operates as designed if connected to a computer running HomeI/O or a compatible control API for smart homes.

**predi-home-control.py** is the Python program that executes the smart-home control and machine learning algorithm.

**predi-home-ML.py** is a subset of the previous program utilized to optimize and tune the machine learning component.

**EngineIO.dll**, **Python.Runtime.dll**, and **clr.pyd** are necessary libraries and programs to communicate with HomeI/O.

**home-io-devices-map-en.pdf** is the blueprint of the architecture and features of the smart-home.

**(location)\_sched\_#.mat/txt** are MATLAB matrices and CSV's containing corresponding time-series feature (i.e., lights) data from source (location) utilized for the machine learning component of Predi-Home.

**time_conv.m** and **time_samp.m** converts the 24-hour time to a sample time index and vice versa, in order to manufacture the smart-home feature data from annotations on the CASAS dataset.

**Project Status** - In-Progress!

## Video Presentation on YouTube

TBA

## Future Work

Extend Predi-Home to control all digital and analog features/devices in a modern smart home. Add disruptive noise and compensating filters to the control algorithm. Test on actual smart homes.

Re-training a neural net is not particularly efficient. Is it possible to efficiently un-train a neural net, perhaps via generating data that counteracts the impact of training on a set of data?

**Developed by Cory Ye, for the embedded systems course ECE M202A at UCLA.**
