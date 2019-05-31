from source import sampling as spl
from source import CauAcc as acc
import sys


def main(argv):

    # Load the ground-truth causal relations
    dag_GT = acc.load_graph_true_graph()

    # Convert ground-truth dag to cpadag
    cpdag_GT = acc.dag2cpdag(dag_GT)
    # Convert ground-truth dag to pag
    pag_GT = acc.dag2pag(dag_GT)

    cpdag_pc = acc.txt2edge('example/pc_result_tetrad.txt')

    pag_fci = acc.txt2pag('example/fci_result_tetrad.txt')

    print('The causal accuracy of PC is ', acc.causal_acc(cpdag_GT, cpdag_pc))
    print('The causal accuracy of FCI is ', acc.causal_acc(pag_GT, pag_fci))


if __name__ == '__main__':
    main(sys.argv[1:])


