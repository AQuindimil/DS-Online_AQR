
"""
Esta función debe recibir como argumento un dataframe y debe devolver una dataframe (describe_df) como el de la imagen (NO el de la imagen). 
Es decir, un dataframe que tenga una columna por cada variable del dataframe original, y como filas los tipos de dichas variables, 
el tanto por ciento de valores nulos o missings, los valores únicos y el porcentaje de cardinalidad.  

"""

def describe_df(df):
    DATA_TYPE=df.dtypes
    MISSINGS=(df.isna().sum()/len(df)*100).sort_values(ascending=False)
    UNIQUE_VALUES=df.nunique()
    CARDIN=UNIQUE_VALUES/len(df)*100
    describe_df=pd.DataFrame([DATA_TYPE, MISSINGS, UNIQUE_VALUES, CARDIN])
    parametros=["DATA_TYPE", "MISSINGS (%)", "UNIQUE_VALUES", "CARDIN (%)"]
    describe_df.insert(0, "COL_N",parametros)
    return describe_df