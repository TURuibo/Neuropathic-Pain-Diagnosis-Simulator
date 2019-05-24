import pandas as pd
import numpy as np


def create_expert_graph_radi_dls():
    """
    Load the graph with edges: DLS -> Radiculopathy
    :return: a pandas dataframe with names Radiculopathy and DLS
    """

    radiculopathy_ = load_radiculopathy_name()
    dls_ = load_dls_names(radiculopathy_)
    radiculopathy = []
    dls = []
    for r, d in zip(radiculopathy_, dls_):
        r_l = 'L ' + r + ' Radikulopati'
        r_r = 'R ' + r + ' Radikulopati'
        radiculopathy.append(r_l)
        radiculopathy.append(r_r)
        dls.append(d)
        dls.append(d)
    ki = ['L C2 Radikulopati', 'L C3 Radikulopati', 'L C4 Radikulopati',
          'R C2 Radikulopati', 'R C3 Radikulopati', 'R C4 Radikulopati']
    for r in ki:
        radiculopathy.append(r)
        dls.append('Kraniocervikal ledskada')

    data = np.array([radiculopathy, dls])
    data = np.transpose(data)

    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['Radiculopathy', 'DLS'])

    # print dataframe.
    print(df)
    df.to_pickle('data/df_radi_dls.pk')
    df.to_csv('result/df_radi_dls.csv', index=True, header=True)
    return df


def create_expert_graph_radi_symp():
    df_g = pd.read_csv('data/symptom_dermatomes_map.csv')
    # Standard name of "reason"
    ColNm = 'reason'
    for i, s in enumerate(df_g.iloc[:][ColNm], start=0):
        print(df_g.loc[i])
        df_g.iloc[i][ColNm] = []
        item = list(filter(str.strip, s.split(';')))
        for it in item:
            df_g.iloc[i][ColNm].append('L ' + it + ' Radikulopati')
            df_g.iloc[i][ColNm].append('R ' + it + ' Radikulopati')

    df_g.to_pickle('data/df_sym_radi.pk')


def load_radiculopathy_name():
    radiculopathy_part = ['C', 'T', 'L', 'S']
    radiculopathy_len = [range(2, 9), range(1, 13), range(1, 6), range(1, 3)]
    radiculopathy = gen_full_data(radiculopathy_part, radiculopathy_len)
    return radiculopathy


def load_dls_names(Radiculopathy):
    """
     Load DiscoLigamentouS injury (DLS) names, e.g. DLS L4_L5 is the cause of Right(R) and Left(L) L5 radiculopathy
    :param Radiculopathy: an ordered name list of radiculopathy names from C0 to S2
    :return: a ordered DLS name
    """
    radiculopathy_lat = [Radiculopathy[i] for i in range(1, len(Radiculopathy))]
    radiculopathy_pre = [Radiculopathy[i] for i in range(len(Radiculopathy) - 1)]

    dls = ['DLS C1-C2']
    for r_p, r_l in zip(radiculopathy_pre, radiculopathy_lat):
        dls.append('DLS ' + r_p + '-' + r_l)
    return dls


def gen_full_data(radiculopathy_part, radiculopathy_len):
    radiculopathy = []
    for p, r_list in zip(radiculopathy_part, radiculopathy_len):
        for r in r_list:
            radiculopathy.append(p + str(r))
    return radiculopathy


def load_expert_graph(graphfile_path):
    """
    Load the expert graph with edges: FirstColumn <- SecondColumn
    :return: a pandas dataframe
    """
    df = pd.read_pickle(graphfile_path)
    return df