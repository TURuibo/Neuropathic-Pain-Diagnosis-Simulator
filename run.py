from source import simulator as sltr

if __name__ == '__main__':
    confounder = False
    with open('models/bnm.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        model = sltr.pickle.load(f)
    columns = sltr.get_columns()
    nun_sample = 100
    if confounder:
        df_sim = sltr.random_sample(model, ['Confounder_DLS_C'] + columns, nun_sample)
    else:
        df_sim = sltr.random_sample(model, columns, nun_sample)
    df_sim.to_csv('result/df_sim_'+str(nun_sample)+'_ex_conf.csv', index=True, header=True)
    print("Congratulation!")
