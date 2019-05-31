from source import sampling as spl
import sys


def main(argv):

    sample_size, confounder, selection_bias, missing_data = spl.parse_arg(argv)
    model = spl.load_pgm()
    nms = spl.get_var_nms()
    df_sim = spl.random_sample(model, nms, sample_size)
    # Name2Num
    df_sim = spl.nam2num(df_sim)

    out_nm = 'SampleSize'+str(sample_size)
    if missing_data:
        # default missingness mechanism is mcar, it can also be mar, or mnar.
        # each mode has its own parameters: mcar_p, mar_p, mnar_p
        df_sim = spl.add_missing_data(df_sim, mode='mcar', seed=10, mcar_p=0.01, mar_p=[0.5, 0.01], mnar_p=[0.5, 0.01])
        out_nm += '_MissingData'

    if selection_bias:
        df_sim = spl.add_selection_bias(df_sim, prob=0.5, seed=10)
        out_nm += '_SelectionBias'

    if confounder:
        df_sim = spl.add_confounder(df_sim)
        out_nm += '_Confounder'

    df_sim.to_csv('result/SimulatedData_' + out_nm + '.csv', index=True, header=True)

    print("Congratulation! The simulated dataset has already been in the \'result\' folder.")


if __name__ == '__main__':
    main(sys.argv[1:])


