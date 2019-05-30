from source import sampling as spl

if __name__ == '__main__':
    confounder = False
    model = spl.load_pgm()
    vars = spl.get_var_nms()
    nun_sample = 100
    
    if confounder:
        df_sim = spl.random_sample(model, ['Confounder_DLS_C'] + vars, nun_sample)
    else:
        df_sim = spl.random_sample(model, vars, nun_sample)

    df_sim.to_csv('result/df_sim_'+str(nun_sample)+'.csv', index=True, header=True)
    print("Congratulation!")
