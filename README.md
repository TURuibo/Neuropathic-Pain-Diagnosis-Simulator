# Neuropathic Pain Diagnosis Simulator
 
This is a Python project for generating the simulated data in the neuropathic pain diagnosis as shown in [1]. The current version only supports to introduce at most one kind of practical issues per generation.

The directory structure is:

	|- models: the ground-truth causal graph that can be loaded and used for generating simulated data.  

	|- result: the simulated data are in this folder.  

	|- source: the source codes for computing causal accuracy and generating the simulated data.  
	
	|- exampe: the related files for the demo of computing causal accuracy

	run.py: the python file that is used for generating simulated data.  
	
	demo_cauacc.py: a demo shows how [1] computes causal accuracies of PC and FCI outputs in Tetrad [2].  

	requirements.txt: all the necessary packages required for the project.  

	README.md: Introduction about the project.  

## Installation

Please install all the packages in the "requirements.txt"

## Usage 
### Generating the simulated data
(Please make sure that the current directory is in the project.)

```python run.py -z <sample size: input a integer number> -c <confounder: flag without value> -s <selection bias: flag without value> -m <missing data: flag without value>```

Default setting: sample size 100, no confounder, no selection bias, no missing data 

Example:   
- default setting:   
```python run.py```
  
- sample size 1000, selection bias (the same setting with the paper [1]):   
```python run.py -z 1000 -s```  

- sample size 500, missing data (MCAR):  
```python run.py -z 500 -m```

### Compute the causal accuracy 
As one of the evaluation metrics in [1], we show a demo which uses the causal accuracy to evaluate PC and FCI in Tetrad. 

1. Load the ground-truth causal graph (DAG)
2. Convert ground-truth DAG to Complete Partially Directed Acyclic Graph (CPDAG) and Partial Ancestral Graph(PAG) with R package pcalg [3].
3. Load the Tetrad output text files of PC and FCI.
4. Compute the causal accuracy of PC and FCI results.
 
```python  demo_cauacc.py```

  
## Result: simulated data
The simulated dataset is in the "result" folder. The dataset contains simulated patient diagnostic records.  

Rows of the simulated dataset represent different patients, and columns represent different diagnose (such as left arm pain, C2-C3 discoligamentous injury, and L C2 Radiculopathy).  

'id_name.txt': For the convenience of representation, we denote different names with numbers and the corresponding numbers of names are in this file. 

## Reference
[1] Ruibo Tu, Kun Zhang, Bo Christer Bertilson, Hedvig Kjellstöm, Cheng Zhang. Neuropathic Pain Diagnosis Simulator for Causal Discovery Algorithm Evaluation.
 
[2] P. Spirtes, C. Glymour, and R. Scheines. The tetrad project: Causal models and statistical data. pittsburgh, 2004.

[3] Kalisch, Markus, et al. "Causal inference using graphical models with the R package pcalg." Journal of Statistical Software 47.11 (2012): 1-26.