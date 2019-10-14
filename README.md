# Neuropathic Pain Diagnosis Simulator

This is a Python package for generating the synthetic data in the neuropathic pain diagnosis as shown in [[1]](https://arxiv.org/abs/1906.01732). 

## Content 

- [Introduction](#Introduction)
- [Installation](#Installation)
- [Structure of Repository](#structure-of-repository)
- [Usage and Examples](#usage-and-examples)

## Introduction

__Result: simulated data__

The simulated dataset is in the "result" folder. The dataset contains simulated patient diagnostic records.  

Rows of the simulated dataset represent different patients, and columns represent different diagnose (such as left arm pain, C2-C3 discoligamentous injury, and L C2 Radiculopathy).  

'id_name.txt': For the convenience of representation, we denote different names with numbers and the corresponding numbers of names are in this file. 

## Installation

Please install all the packages in the "requirements.txt"

## Structure of Repository

The directory structure is:

* models: the ground-truth causal graph that can be loaded and used for generating simulated data.  
	
* result: the simulated data are in this folder.  

* source: the source codes for computing causal accuracy and generating the simulated data.  

* exampe: the related files for the demo of computing causal accuracy

## Usage and Examples
__Using command line to generate data__
(Please make sure that the current directory is in the project. The current version only supports to introduce one practical issue to the dataset every time.)

```python run.py -z <sample size: input a integer number> -c <confounder: flag without value> -s <selection bias: flag without value> -m <missing data: flag without value>```

Default setting: sample size 100, no confounder, no selection bias, no missing data 

- default setting:   
```python run.py```
  
- sample size 1000, selection bias:   
```python run.py -z 1000 -s```  

- sample size 500, missing data (MCAR):  
```python run.py -z 500 -m```

__Examples__

A tutorial shows how to simulate data in the [Tutorial 1](https://github.com/TURuibo/Neuropathic-Pain-Diagnosis-Simulator/blob/master/Tutorial1.ipynb).

A tutorial shows how to compute causal accurcay of PC and FCI on the simulation data [Tutorial 2](https://github.com/TURuibo/Neuropathic-Pain-Diagnosis-Simulator/blob/master/Tutorial2.ipynb.).

## Reference
[1] Ruibo Tu, Kun Zhang, Bo Christer Bertilson, Hedvig Kjellstöm, Cheng Zhang. Neuropathic Pain Diagnosis Simulator for Causal Discovery Algorithm Evaluation.

[2] P. Spirtes, C. Glymour, and R. Scheines. The tetrad project: Causal models and statistical data. pittsburgh, 2004.

[3] Kalisch, Markus, et al. "Causal inference using graphical models with the R package pcalg." Journal of Statistical Software 47.11 (2012): 1-26.