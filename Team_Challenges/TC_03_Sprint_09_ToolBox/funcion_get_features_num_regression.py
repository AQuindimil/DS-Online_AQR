
"""
Esta función recibe como argumentos un dataframe, el nombre de una de las columnas del mismo (argumento 'target_col'), que debería ser el target de un hipotético modelo de regresión, 
es decir debe ser una variable numérica continua o discreta pero con alta cardinalidad, además de un argumento 'umbral_corr', 
de tipo float que debe estar entre 0 y 1 y una variable float "pvalue" cuyo valor debe ser por defecto "None".
La función debe devolver una lista con las columnas numéricas del dataframe cuya correlación con la columna designada por "target_col" sea superior en valor absoluto al valor dado por "umbral_corr". 
Además si la variable "pvalue" es distinta de None, sólo devolvera las columnas numéricas cuya correlación supere el valor indicado y además supere el test de hipótesis con significación mayor o igual a 1-pvalue.
La función debe hacer todas las comprobaciones necesarias para no dar error como consecuecia de los valores de entrada. 
Es decir hará un check de los valores asignados a los argumentos de entrada y si estos no son adecuados debe retornar None y printar por pantalla la razón de este comportamiento. 
Ojo entre las comprobaciones debe estar que "target_col" hace referencia a una variable numérica continua del dataframe.
"""




def get_features_num_regression(df, target_col, umbral_corr, pvalue=None):
    df_tip=tipifica_variables(df)
    if target_col in df.columns:
        cond_target1=df_tip.nombre_variable == target_col
        cond_target2=(df_tip.tipo_sugerido == "Numérica continua")
        cond_num= (df_tip.tipo_sugerido == "Numérica continua") | (df_tip.tipo_sugerido == "Numérica discreta")
        target_numerico = df_tip.loc[cond_target1 & cond_target2]
        
        if not target_numerico.empty:
            col_num=df_tip.loc[cond_num, "nombre_variable"].tolist()
            matriz_correlacion=df[col_num].corr()
            correlacion_con_target = matriz_correlacion[target_col].abs()
            print(f"La variable {target_col} se puede considerar variable target, ya que es numérica continua.")
            condicion_umbral=(correlacion_con_target > umbral_corr) & (correlacion_con_target < 1.0)
            num_selec1=correlacion_con_target[condicion_umbral].index.tolist()
            num_selec2 = []
            for col in num_selec1:
            # Eliminamos filas con nulos en estas dos columnas para evitar errores en el test
                df_temp = df[[col, target_col]].dropna()
            # Calculamos la correlación y el p-value:
                r_val, p_val = pearsonr(df_temp[col], df_temp[target_col])
            # Si el usuario no definió pvalue, o si el p_val es menor al umbral solicitado
                if pvalue is None or p_val < pvalue:
                    num_selec2.append(col)
                    print(f"Variable '{col}' seleccionada: p-value = {p_val:.4f} (relación estadísticamente significativa).")
                else:
                    print(f"Variable '{col}' descartada: p-value = {p_val:.4f} (relación no significativa).")
            return num_selec2
        else:
            print(f"La variable {target_col} existe, pero no es numérica continua.")
    else:
        print("La variable no está en el dataset.")
