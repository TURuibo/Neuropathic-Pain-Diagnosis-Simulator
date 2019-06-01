from source import CauAcc as acc


def main():

    # Load the ground-truth causal relations
    dag_GT = acc.load_graph_true_graph()
    acc.causal_acc(dag_GT, dag_GT)

    # Load the R package Pcalg function dag2cpdag result
    cpdag_GT = acc.dag2cpdag()

    # Load the R package Pcalg function dag2pag result
    pag_GT = acc.dag2pag()

    cpdag_pc = acc.txt2edge('example/pc_result_tetrad.txt')

    pag_fci = acc.txt2pag('example/fci_result_tetrad.txt')

    print('Compared with the ground-truth CPDAG, the causal accuracy of PC is ', acc.causal_acc(cpdag_GT, cpdag_pc))
    print('Compared with the ground-truth PAG, the causal accuracy of FCI is ', acc.causal_acc(pag_GT, pag_fci))


if __name__ == '__main__':
    main()


