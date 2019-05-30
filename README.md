# Neuropathic Pain Diagnosis Simulator

This is a Python project for generating the simulated data in the neuropathic pain diagnosis. The current version only supports to generate one kind of practical issues for one dataset per generation.

The directory structure is:

	|- models: the ground-truth causal graph that can be loaded and used for generating simulated data.  

	|- result: the simulated data are in this folder.  

	|- source: the source codes for creating the ground-truth causal graph and generating the simulated data.  

	run.py: the python file that is used for generating simulated data.  

	requirements.txt: all the necessary packages required for the project.  

	README.md: Introduction about the project.  

## Installation

Please install all the packages in the "requirements.txt"

## Usage
(Please make sure that the current directory is in the project.)

```python run.py -z <sample size: input a integer number> -c <confounder: flag without value> -s <selection bias: flag without value> -m <missing data: flag without value>```

Default setting: sample size 100, no confounder, no selection bias, no missing data 

Example:   
- default setting:   
```python run.py```
  
- sample size 1000, selection bias:   
```python run.py -z 1000 -s```  

- sample size 500, missing data:  
```python run.py -z 500 -m```  

## Result
The simulated dataset is in the "result" folder.

