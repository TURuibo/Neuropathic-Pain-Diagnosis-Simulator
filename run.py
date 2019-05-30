from source import sampling as spl
import sys

def main(argv):

    sample_size, confounder, selection_bais, missing_data = spl.parse_arg(argv)
    model = spl.load_pgm()
    nms = spl.get_var_nms()
    df_sim = spl.random_sample(model, nms, sample_size)

    df_sim.to_csv('result/df_sim_' + str(sample_size) + '.csv', index=True, header=True)
    print("Congratulation! The simulated dataset has already been in the \'result\' folder.")


if __name__ == '__main__':
    main(sys.argv[1:])


