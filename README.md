# Neuropathic Pain Diagnosis Simulator

The Neuropathic Pain Diagnosis Simulator is a Python package for generating synthetic diagnosis records of neuropathic pain patients. Moreover, for evaluating causal discovery algorithms we provide the ground-true causal relations of the variables involving in the simulator. We also provide options to introduce the practical issues into simulated data such as unknown confounding, selection bias, and missing data.

## Content 

- [Introduction](#Introduction)
- [Installation](#Installation)
- [Structure of Repository](#structure-of-repository)
- [Usage and Examples](#usage-and-examples)

## Introduction

The neuropathic pain diagnosis mainly consists of symptom diagnosis, pattern diagnosis, and pathophysiological diagnosis. The symptom diagnosis describes the discomfort of patients such as lumbago and lateral arm discomfort. The pattern diagnosis identifies nerve roots that lead to symptom patterns. The pathophysiological diagnosis identifies of discoligamentous injuries.

The simulator generates synthetic neuropathic pain diagnosis records in the form of tables of which the row represents different patients and the column represents different diagnostic labels. The diagnostic labels are binary: Taking the value "0" represents that the diagnostic label is not in a patient record; taking the value "1" represents that the diagnostic label is in a patient record. For example, the dataset looks like the following table.

|Patient id 	| DLS C1-C2 	| DLS C2-C3		|...		| L C2 Radiculopathy | R C2 Radiculopathy|...|L neck pain| R neck pain| ...|
| ------------- | ------------- |------------- |------------- |------------- |------------- |------------- |------------- |------------- |------------- |
|1| 1 | 1| ...| 0 |1|...|1| 0| ...|
|2| 0 | 0| ...| 0 |0|...|1| 0| ...|
|3| 0 | 0| ...| 1|0|...|0| 0| ...|
|...| ... | ...| ...| ... |...|...|...| ...| ...|
|n| 1 | 0| ...| 1 |0|...|0| 1| ...|


In the generated dataset, the neuropathic pain diagnosis includes 222 diagnostic labels. More specifically, 143 symptoms such as left arm pain, and right neck pain are in symptom diagnosis; 52 radiculopathies are in the pattern diagnosis; craniocervical junction injury and 26 discoligamentous injuries are in pathophysiological diagnosis. The causal relations in neuropathic pain diagnosis are shown in a [causal graph](https://observablehq.com/@turuibo/the-complete-causal-graph-of-neuropathic-pain-diagnosis). In general, neuropathic pain symptoms in the symptom diagnosis are mainly caused by radiculopathy (Radi) in the pattern diagnosis, and the radiculopathy is mostly caused by discoligamentous injury (DLI) in the pathophysiological diagnosis. 

<img
    src='https://github.com/TURuibo/Neuropathic-Pain-Diagnosis-Simulator/blob/master/example/subset_causal_relations.png'
    height="300">

A typical example of the causal graph is in the above figure. The causal graph consists of three layers: pathophysiological diagnosis layer, pattern diagnosis layer, and symptom diagnosis layer. Nodes in each layer have no connection with each other. Arrows either point from nodes in the pathophysiological diagnosis layer to nodes in the pattern diagnosis layer or from nodes in the pattern diagnosis layer to nodes in the symptom diagnosis layer. 


More details can be found in [the paper [1]](https://arxiv.org/abs/1906.01732). 

## Installation

Please install all the packages in the "requirements.txt"

## Structure of Repository

The directory structure is:

* models: the ground-truth causal graph that can be loaded and used for generating simulated data.  
	
* result: the simulated data are in this folder. 
	* 'id_name.txt': For the convenience of representation, we assign different id numbers for different names. The corresponding numbers of names are in this file. 

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