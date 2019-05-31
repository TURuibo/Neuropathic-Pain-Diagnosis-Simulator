import pandas as pd
import numpy as np
from source import sampling as spl
import pickle


def dag2cpdag(dag_GT):
    return dag_GT


def dag2pag(dag_GT):
    return dag_GT


def causal_acc(gt,g):
    return


def load_graph_true_graph():
    name_dic = spl.get_nam_dic()
    cause = []
    effect = []
    dag = np.zeros((222, 222), dtype=np.int)

    with open('models/bnm.pickle', 'rb') as f:
        model = pickle.load(f)

    for c, e in model.edges():
        cause.append(name_dic[c])
        effect.append(name_dic[e])
        dag[cause, effect] = 1

    return dag


def txt2edge(path):
    """
    Convert the output text file (CPDAG) of PC and GES in Tetrad to the matrix which represent PAG graph
    :param path: path of the output text file of Tetrad
    :return: numpy array which is the representation of CPDAG which follows PCALG (R library) notation.
    """
    cpdag = np.zeros((222, 222), dtype=np.int)
    with open(path, "r") as file:
        # Repeat for each song in the text file
        for i, line in enumerate(file):
            if i > 3:
                fields = line.split(" ")
                if fields[0] == '\n':
                    pass
                else:
                    if ">" in fields[2]:
                        cpdag[int(fields[1]), int(fields[3])] = 1

                    else:
                        cpdag[int(fields[3]), int(fields[1])] = 1
                        cpdag[int(fields[1]), int(fields[3])] = 1

    return cpdag


def sym_num(sym):
    return{'o':  1, '>':  2, '-': 3, '<': 2}[sym]


def txt2pag(path):
    """
    Convert the output text file of FCI methods in Tetrad to the matrix which represent PAG graph
    :param path: path of the output text file of Tetrad
    :return: numpy array which is the representation of PAG which follows PCALG (R library) notation.
    """
    pag = np.zeros((222, 222), dtype=np.int)
    with open(path,"r") as file:
        # Repeat for each song in the text file
        for i, line in enumerate(file):
            if i > 3:
                fields = line.split(" ")
                if fields[0] == '\n':
                    pass
                else:
                    pag[int(fields[1]), int(fields[3])] = int(sym_num(fields[2][2]))
                    pag[int(fields[3]), int(fields[1])] = int(sym_num(fields[2][0]))
    return pag

