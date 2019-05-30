import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import numpy as np
from itertools import product
import pickle
import sys
import getopt

def parse_arg(argv):
    """
    Parse the input
    -z  sample size
    -c  confounder
    -s  selection bias
    -m  missing data
    --sample_size val
    --confounder
    --selection_bias
    --missing_data
    """
    sample_size = 100
    confounder = False
    selection_bais = False
    missing_data = False

    try:
        opts, args = getopt.getopt(argv, "z:csm", ['sample_size=',
                                                   'confounder=',
                                                   'selection_bias=',
                                                   'missing_data='])
    except getopt.GetoptError:
        print('Please use the simulator with: \n\'run.py ',
              '-z <sample size: a integer number> ',
              '-c <confounder> -s <selection bias> ',
              '-m <missing data>',
              '(--sample_size val',
              '--confounder',
              '--selection_bias',
              '--missing_data)\''
              )
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('run.py -z <sample size: a integer number> -c <confounder> -s <selection bias> -m <missing data>')
            sys.exit()
        elif opt in ("-z", "--sample_size"):
            try:
                val = int(arg)
                sample_size = val
            except ValueError:
                print("SAMPLE SIZE is not integer.")
                print('Please use the simulator with: \n\'run.py ',
                      '-z <sample size: a integer number> ',
                      '-c <confounder> -s <selection bias> ',
                      '-m <missing data>',
                      '(--sample_size val',
                      '--confounder',
                      '--selection_bias',
                      '--missing_data)\''
                      )
                sys.exit(2)
        elif opt in ("-c", "--confounner"):
            confounder = True
        elif opt in ("-s", "--selection_bias"):
            selection_bais = True
        elif opt in ("-m", "--missing_data"):
            missing_data = True

    print('SAMPLE SIZE = ', str(sample_size), ',',
          'CONFOUNDER = ', str(confounder), ',',
          'SELECTION BIAS = ', str(selection_bais), ',',
          'MISSING DATA = ', str(missing_data))
    return sample_size, confounder, selection_bais, missing_data


def load_pgm(path='models/bnm.pickle'):
    """
    Load the simulator which is saved in the default path 'models/bnm.pickle'.
    return a pgmpy "BaysianModel"
    """
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

def random_sample(bn, orderd_nodes=None, n=10, seed=7):
    '''
    ******************
    Random Sample Code
    ******************
    Generate a random sample dataset from a known Bayesian Network,
    with or without evidence.

    The function is used for pgmpy "BayesianModel" class

    Adapt the same function in https://github.com/ncullen93/pyBN
    ( Nicholas Cullen <ncullen.th@dartmouth.edu> )

    ******************
    Parameters
        bn: "BayesianModel" class in pgmpy
        orderd_nodes: generate sample for variables with a certain order
        n: Number of samples
    ******************
    Return:
        A numpy 2D array:
            row  different samples,
            column different variables

    '''
    np.random.seed(seed)
    if orderd_nodes is not None:
        nodes = orderd_nodes
    else:
        nodes = bn.nodes()
    sample = np.zeros((n, len(nodes)), dtype=np.int)

    rv_map = dict([(rv, idx) for idx, rv in enumerate(nodes)])

    for i in range(n):
        while np.sum(sample[i]) == 0:
            for rv in nodes:
                f = bn.get_cpds(rv).copy()
                f.reduce([(p, sample[i][rv_map[p]]) for p in f.get_evidence()])
                choice_vals = f.variable_card
                choice_probs = f.values
                chosen_val = np.random.choice(choice_vals, p=choice_probs)
                sample[i][rv_map[rv]] = chosen_val
    df = pd.DataFrame(np.array(sample), columns=list(orderd_nodes))
    return df

def get_var_nms():
    name= ['DLS C1-C2', 'DLS C2-C3', 'DLS C3-C4', 'DLS C4-C5', 'DLS C5-C6', 'DLS C6-C7', 'DLS C7-C8', 'DLS C8-T1',
     'DLS L1-L2', 'DLS L2-L3', 'DLS L3-L4', 'DLS L4-L5', 'DLS L5-S1', 'DLS S1-S2', 'DLS T1-T2', 'DLS T10-T11',
     'DLS T11-T12', 'DLS T12-L1', 'DLS T2-T3', 'DLS T3-T4', 'DLS T4-T5', 'DLS T5-T6', 'DLS T6-T7', 'DLS T7-T8',
     'DLS T8-T9', 'DLS T9-T10', 'Kraniocervikal ledskada', 'L C2 Radikulopati', 'R C2 Radikulopati',
     'L C3 Radikulopati', 'R C3 Radikulopati', 'L C4 Radikulopati', 'R C4 Radikulopati', 'L C5 Radikulopati',
     'R C5 Radikulopati', 'L C6 Radikulopati', 'R C6 Radikulopati', 'L C7 Radikulopati', 'R C7 Radikulopati',
     'L C8 Radikulopati', 'R C8 Radikulopati', 'L T1 Radikulopati', 'R T1 Radikulopati', 'L T2 Radikulopati',
     'R T2 Radikulopati', 'L T3 Radikulopati', 'R T3 Radikulopati', 'L T4 Radikulopati', 'R T4 Radikulopati',
     'L T5 Radikulopati', 'R T5 Radikulopati', 'L T6 Radikulopati', 'R T6 Radikulopati', 'L T7 Radikulopati',
     'R T7 Radikulopati', 'L T8 Radikulopati', 'R T8 Radikulopati', 'L T9 Radikulopati', 'R T9 Radikulopati',
     'L T10 Radikulopati', 'R T10 Radikulopati', 'L T11 Radikulopati', 'R T11 Radikulopati', 'L T12 Radikulopati',
     'R T12 Radikulopati', 'L L1 Radikulopati', 'R L1 Radikulopati', 'L L2 Radikulopati', 'R L2 Radikulopati',
     'L L3 Radikulopati', 'R L3 Radikulopati', 'L L4 Radikulopati', 'R L4 Radikulopati', 'L L5 Radikulopati',
     'R L5 Radikulopati', 'L S1 Radikulopati', 'R S1 Radikulopati', 'L S2 Radikulopati', 'R S2 Radikulopati', 'IBS',
     'L Nackbesvär', 'Nackbesvär', 'R Nackbesvär', 'L Tinnitus', 'L Ögonbesvär', 'L Öronbesvär', 'R Tinnitus',
     'R Ögonbesvär', 'R Öronbesvär', 'Huvudvärk', 'L Käkbesvär', 'L Pannhuvudvärk', 'Munbesvär', 'Pannhuvudvärk',
     'R Pannhuvudvärk', 'R PFS', 'Svalgbesvär', 'R Käkbesvär', 'Bakhuvudvärk', 'R Bakhuvudvärk', 'L Nyckelbensbesvär',
     'R Nyckelbensbesvär', 'Central bröstsmärta', 'L Central bröstsmärta', 'L Centrala bröstbesvär',
     'R Främre Axelbesvär', 'L Axel impingement', 'R Axel impingement', 'L Axelbesvär', 'L Skulderbesvär',
     'R Axelbesvär', 'R Skulderbesvär', 'L Övre armsbesvär', 'L Övre armbågsbesvär', 'Interskapulära besvär',
     'L Interskapulära besvär', 'R Interskapulära besvär', 'L Laterala armbågsbesvär', 'L Laterala armsbesvär',
     'R Laterala armbågsbesvär', 'L Armbågsbesvär', 'R Armbågsbesvär', 'L Armbesvär', 'L Tumbesvär', 'R Tumbesvär',
     'L Handledsbesvär', 'R Handledsbesvär', 'L Under armsbesvär', 'R Under armsbesvär', 'L Handbesvär', 'R Handbesvär',
     'L Armvecksbesvär', 'R Armbesvär', 'R Armvecksbesvär', 'L Mediala armbågsbesvär', 'R Mediala armbågsbesvär',
     'L Fingerbesvär', 'R Fingerbesvär', 'L Lillfingerbesvär', 'R Lillfingerbesvär', 'L Ljumskbesvär',
     'L Mediala ljumskbesvär', 'L Laterala ljumskbesvär', 'Centrala Ljumskbesvär', 'R Laterala ljumskbesvär',
     'R Ljumskbesvär', 'L Adduktortendalgi', 'R Adduktortendalgi', 'L Höftbesvär', 'L Bakhuvudvärk', 'Ryggsbesvär',
     'L Lumbago', 'Lumbago', 'R Lumbago', 'L Främre lårbesvär', 'R Främre lårbesvär', 'R Lårbesvär', 'L Benbesvär',
     'L Lårbesvär', 'R Benbesvär', 'R Mediala vadbesvär', 'L PFS', 'L Höftkamsbesvär', 'R Höftbesvär',
     'R Höftkamsbesvär', 'L Mediala knäledsbesvär', 'L Främre knäbesvär', 'R Mediala knäledsbesvär',
     'R Främre knäbesvär', 'L Tibiaperialgi', 'R Tibiaperialgi', 'L Laterala vadbesvär', 'L Knäbesvär', 'R Knäbesvär',
     'L Tåledbesvär', 'L Stortårbesvär', 'R Stortårbesvär', 'L Fotbesvär', 'L Fotledsbesvär', 'R Fotledsbesvär',
     'L Fotvalvsbesvär', 'R Fotvalvsbesvär', 'R Mortonbesvär', 'R Tåledbesvär', 'L Ischias', 'R Ischias',
     'L Skinkbesvär', 'L Vadbesvär', 'R Skinkbesvär', 'L Tårbesvär', 'R Fotbesvär', 'R Tårbesvär', 'R Vadbesvär',
     'R Dorsala knäledsbesvär', 'L Dorsala knäledsbesvär', 'L Laterala knäbesvär', 'R Laterala knäbesvär',
     'L Lilltåbesvär', 'L Laterala Fotbesvär', 'R Laterala Fotbesvär', 'R Hälbesvär', 'Hälbesvär', 'L Hälbesvär',
     'Coccydyni', 'L Bakre lårbesvär', 'R Bakre lårbesvär', 'L Achillesbesvär', 'L Achillestendalgi', 'L Achillodyni',
     'R Achillesbesvär', 'R Achillestendalgi', 'R Achillodyni', 'Bröstryggsbesvär', 'Bröstbesvär', 'L Bröstbesvär',
     'R Bröstbesvär', 'Torakal Dysfunktion', 'Övre bukbesvär', 'Laterala bukbesvär', 'Bukbesvär', 'L Nedre bukbesvär',
     'Nedre bukbesvär']
    return name
