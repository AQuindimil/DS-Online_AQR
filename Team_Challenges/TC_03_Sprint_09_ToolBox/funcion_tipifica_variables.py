"""
Esta función debe recibir como argumento un dataframe, un entero (`umbral_categoria`) y un float (`umbral_continua`).
La función debe devolver un dataframe con dos columnas "nombre_variable", "tipo_sugerido" que tendrá tantas filas como columnas el dataframe. 
En cada fila irá el nombre de una de las columnas y una sugerencia del tipo de variable. 
Esta sugerencia se hará siguiendo las siguientes pautas:
+ Si la cardinalidad es 2, asignara "Binaria"
+ Si la cardinalidad es menor que `umbral_categoria` asignara "Categórica"
+ Si la cardinalidad es mayor o igual que `umbral_categoria`, entonces entra en juego el tercer argumento:
    * Si además el porcentaje de cardinalidad es superior o igual a `umbral_continua`, asigna "Numerica Continua"
    * En caso contrario, asigna "Numerica Discreta"

"""


def tipifica_variables(df,umbral_categoria=6, umbral_continua=10):
    Tipo=df.dtypes
    Card=df.nunique()
    Card_rel=Card/len(df)*100
    df_tipificacion=pd.DataFrame([df.columns, Tipo, Card, Card_rel]).T.rename(columns = {0: "nombre_variable", 1: "Tipo", 2: "Card", 3: "Card_rel"})
    df_tipificacion["tipo_sugerido"]="sin categoría" 
    df_tipificacion.loc[df_tipificacion.Card == 2, "tipo_sugerido"] = "Binaria"
    es_numerica = ((df_tipificacion.Tipo == "float64") | (df_tipificacion.Tipo == "int64")) 
    #df_tipificacion.loc[df_tipificacion.Tipo == "datetime64[ns]", "Clasificada_como"] = "Fecha"
    df_tipificacion.loc[(df_tipificacion.Card > 2) & (df_tipificacion.Card < umbral_categoria), "tipo_sugerido"] = "Categórica"
    df_tipificacion.loc[(df_tipificacion.Card > umbral_categoria) & es_numerica & (df_tipificacion.Card_rel < umbral_continua), "tipo_sugerido"] = "Numérica discreta"
    df_tipificacion.loc[(df_tipificacion.Card > umbral_categoria) & es_numerica &  (df_tipificacion.Card_rel > umbral_continua), "tipo_sugerido"] = "Numérica continua"

    return df_tipificacion[["nombre_variable", "tipo_sugerido"]]