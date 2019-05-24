from source import expert_graph as ep
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import numpy as np
from itertools import product
import pickle


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


def get_cpd(var, parent, df_cpd, MAR_CONST=0.05, CONP_CONST=0.1):
    """
    # Add cpd for X
    #          Col1: P1 = 0, P1 = 0, P1 = 1, P1 = 1
    #                P2 = 0, P2 = 1, P2 = 0, P2 = 1
    # Row1: X=0
    # Row2: X=1
    #
    ######Example##########
    # list(get_val_mask((1,2,3),3))
    #
    ######## Example 1########
    # prob_var_pa(1,
    #             (0,1,1,0),
    #             'L Nackbesvär',
    #             ['L C2 Radikulopati','L C3 Radikulopati','L C4 Radikulopati','L C5 Radikulopati'],
    #             df_cpd)
    #
    ######## Example 2########
    # get_cpd('L C2 Radikulopati',
    #         [],
    #         df_cpd)
    #
    ######## Example 3########
    # get_cpd('L Nackbesvär',
    #         ['L C2 Radikulopati','L C3 Radikulopati','L C4 Radikulopati','L C5 Radikulopati'],
    #         df_cpd)
    #
    """
    cpd = [[], []]
    if len(parent) == 0:
        # No parent, then compute marginal distribution
        vl_var = 0
        cpd[vl_var].append(marginal_dis(var, vl_var, df_cpd, MAR_CONST))
        cpd[1-vl_var] = [1 - i for i in cpd[vl_var]]
    else:
        vl_var = 1
        if var_in_dataset(var, df_cpd):
            max_pa_1 = max_var_pa(vl_var, var, parent, df_cpd, CONP_CONST)
            print(var, max_pa_1)
            for vl_pa in list(product([0, 1], repeat=len(parent))):
                p_var_p = prob_var_pa(vl_var, np.array(vl_pa), np.array(max_pa_1), CONP_CONST)
                if p_var_p == 1 - vl_var and np.sum(vl_pa == 1) != 0:
                    cpd[vl_var].append(np.abs(-1 + vl_var + CONP_CONST))
                else:
                    cpd[vl_var].append(p_var_p)
        else:
            # IMPUTATION: if a variable with parents is not in the dataset, we should estimate its CPD
            cpd[vl_var] = list(np.full(2 ** len(parent), MAR_CONST))
            cpd[vl_var][0] = np.abs(-1 + vl_var)
        cpd[1-vl_var] = [1 - i for i in cpd[vl_var]]
    return cpd


def marginal_dis(var, vl_var, df_cpd, PROB_CONST=0.1):
    """
    Pr(var = vl_var) none zero or one guarantee
    :param var:
    :param vl_var:
    :param df_cpd:
    :param PROB_CONST:
    :return: Pr(var = vl_var)
    """

    if var_in_dataset(var, df_cpd):
        # If the variable is in the dataset
        b_var = df_cpd.iloc[:][var] == vl_var  # how many values are equal to our target value
        pr_vl_var = np.sum(b_var) / len(b_var)  # Pr(var = vl_var)
        if pr_vl_var != (1 - vl_var):
            return pr_vl_var
        else:
            # If the Pr(var = 1) = 0 or  Pr(var = 0) = 1
            # Pr(var = 1) = PROB_CONST
            # Pr(var = 0) = 1 - PROB_CONST
            return np.abs(-1 + vl_var + PROB_CONST)
    else:
        # Pr(var = 1) = PROB_CONST
        # Pr(var = 0) = 1 - PROB_CONST
        return np.abs(-1 + vl_var + PROB_CONST)


def var_in_dataset(var, df_cpd):
    return var in list(df_cpd.columns.values)


def max_var_pa(vl_var, var, parent, df_cpd, PROB_CONST=0.01):
    data_parent_ind = [pa in list(df_cpd.columns.values) for pa in parent]
    if np.sum(data_parent_ind) == 0:
        print(var, 'ALL parents not in dataset, treat as no parent')
        max_full_list = [np.abs(-1 + vl_var + PROB_CONST) for _ in data_parent_ind]
        return max_full_list
    parent_ = np.array(parent)
    parent = parent_[data_parent_ind]

    nrow, ncol = df_cpd[parent].shape
    b_var = df_cpd[var] == vl_var
    pa_mask = np.ones((nrow, ncol))
    b_pa = np.array(pa_mask == df_cpd[parent])

    max_list = np.array([np.sum(np.logical_and(b_var, b_pa[:, i])) / np.sum(b_pa[:, i]) for i in range(ncol)])
    max_full_list = []
    i = 0
    for ind in data_parent_ind:
        if ind:
            max_full_list.append(max_list[i])
            i = i + 1
        else:
            # IMPUTATION: Mean impute the missing parents P(symptom|cause),
            if vl_var == 1:
                max_full_list.append(PROB_CONST)
            else:
                max_full_list.append(1 - PROB_CONST)
    return max_full_list


def prob_var_pa(vl_var, vl_pa, max_pa_1, CONP_CONST):
    # Estimat P(Y=1|X_0,...,Xi) with max(P(Y|X_0),...,P(Y|X_i))
    if np.sum(vl_pa == 1) == (1 - vl_var):
        return np.abs(-1 + vl_var)
    else:
        return np.max(max_pa_1[vl_pa == 1])


def ham_dis(v1, v2):
    return np.sum(v1 != v2)


def is_in_col(var, df_cpd):
    col_nm = df_cpd.columns.values
    if var in col_nm:
        return True
    else:
        return False


def get_val_mask(val, nrow):
    x = np.array(val)
    x.shape = (1, len(x))
    return np.repeat(x, nrow, axis=0)


def combinations2group(iterable1, iterable2, ori=0):
    """Combine with the 2 elements in two groups"""
    # combinations2group('ABC','DE'): AD, AE, BD, BE, CD, CE
    pool = tuple(iterable1 + iterable2)
    iter1 = len(iterable1)
    iter2 = len(iterable1) + len(iterable2)

    for ind1 in range(iter1):
        for ind2 in range(iter1, iter2):
            if ori is 0:
                indices = [ind1, ind2]
            else:
                indices = [ind2, ind1]
            yield tuple(pool[i] for i in indices)


def df2tpl(df):
    for x in df.values:
        yield tuple(x)


def load_expert_bayesianmodel(confounder=True, MAR_CONST=0.005, CONP_CONST=0.01):
    df1 = ep.load_expert_graph('data/df_radi_dls.pk')
    df2 = ep.load_expert_graph('data/df_sym_radi.pk')
    df_cpd = pd.read_pickle('data/df_cpd.pk')

    bnm = BayesianModel()
    nrow, ncol = df1.shape

    for i in range(nrow):
        radi_i = df1.iloc[i]['Radiculopathy']
        dls_i = df1.iloc[i]['DLS']
        bnm.add_edges_from([(dls_i, radi_i)])

    nrow, ncol = df2.shape
    for i in range(nrow):
        symp_i = df2.iloc[i]['sv_symp']
        reason_i = df2.iloc[i]['reason']
        bnm.add_edges_from(list(combinations2group([symp_i], list(reason_i), ori=1)))

    # ADD THE CONFOUNER CODE HERE #
    if confounder:
        dsl_c = [ 'DLS C2-C3', 'DLS C3-C4',
                 'DLS C4-C5', 'DLS C5-C6', 'DLS C6-C7', 'DLS C7-C8']

        cfdr = 'Confounder_DLS_C'
        d_cpd_con = attach_confounder(dsl_c, df_cpd, cfdr)

        for d in dsl_c:
            bnm.add_edges_from([(cfdr, d)])

        df_cpd = d_cpd_con


    for var in bnm.nodes():
        pa = bnm.get_parents(var)

        cpd = get_cpd(var, pa, df_cpd, MAR_CONST, CONP_CONST)
        # Associating the parameters with the model structure.
        if len(pa) is 0:
            bnm.add_cpds(TabularCPD(variable=var, variable_card=2, values=cpd))
        else:
            bnm.add_cpds(TabularCPD(variable=var,
                                    variable_card=2,
                                    evidence=pa,
                                    evidence_card=[2] * len(pa),
                                    values=cpd))

    # # Checking if the cpds are valid for the model.
    print(bnm.check_model())

    with open('models/bnm.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(bnm, f, pickle.HIGHEST_PROTOCOL)


def attach_confounder(dsl_c, df_cpd, cfdr):
    df_dls_c = list(df_cpd[dsl_c].any(axis='columns'))
    nrow, ncol = df_cpd.shape
    col = np.array([0] * nrow)
    col[df_dls_c] = 1
    df_cpd[cfdr] = col
    df_cpd[dsl_c+[cfdr]].to_csv('data/d_cpd_con.csv', index=True, header=True)
    return df_cpd


def get_columns():
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
