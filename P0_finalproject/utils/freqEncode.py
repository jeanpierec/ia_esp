def freqEcondeList(df, to_encode):
    class Lista(object):
        pass

    i = 0
    lista_enc = Lista()
    for elemento in to_encode:
        fe = df.groupby(to_encode[i]).size()/len(df)
        setattr(lista_enc, to_encode[i], fe)
        df[to_encode[i]] = df[to_encode[i]].map(fe)
        i = i + 1
    
    return lista_enc, df