#-----------------------------------------------------------------------------------------------------------------
# ICFES PROJECT
# Leyton Jean Piere Castro Clavijo
# Universidad Autónoma de occidente
#-----------------------------------------------------------------------------------------------------------------
import sys
sys.path.append('/utils/__init__.py')
import utils

import pandas as pd
import numpy as np
import seaborn as sns
# Save a palette to a variable:
palette = sns.color_palette("bright")
sns.set_palette(palette)

import matplotlib.pyplot as plt 
from matplotlib.ticker import ScalarFormatter

sns.set(color_codes=True)

# Machine learning
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn import metrics
from xgboost import XGBRegressor

#-----------------------------------------------------------------------------------------------------------------
# Load Dataset
df_2019_2 = pd.read_csv("datasets\Saber_11__2019-2.csv")
df_2020_1 = pd.read_csv("datasets\Saber_11__2020-1.csv")
df_2020_2 = pd.read_csv("datasets\Saber_11__2020-2.csv")

# A unique variable
df_2019_2["ANIO_PR"] = 201902
df_2020_1["ANIO_PR"] = 202001
df_2020_2["ANIO_PR"] = 202002

# Concat and copy
df = pd.concat([df_2019_2, df_2020_1, df_2020_2])
df_copy = df.copy()
#-----------------------------------------------------------------------------------------------------------------
# Encoding
to_encode = ['ESTU_NACIONALIDAD', 'ESTU_GENERO', 
        'ESTU_FECHANACIMIENTO', 'PERIODO',
       'ESTU_CONSECUTIVO', 'ESTU_ESTUDIANTE', 'ESTU_TIENEETNIA',
       'ESTU_PAIS_RESIDE', "DESEMP_INGLES",
       'ESTU_ETNIA', 'ESTU_DEPTO_RESIDE', 'ESTU_COD_RESIDE_DEPTO', 
       'ESTU_MCPIO_RESIDE', 
       'ESTU_COD_RESIDE_MCPIO','FAMI_ESTRATOVIVIENDA', 
       'FAMI_PERSONASHOGAR', 'FAMI_CUARTOSHOGAR',
       'FAMI_EDUCACIONPADRE', 'FAMI_EDUCACIONMADRE', 
       'FAMI_TRABAJOLABORPADRE', 'FAMI_TRABAJOLABORMADRE', 
       'FAMI_TIENEINTERNET', 'FAMI_TIENESERVICIOTV',
       'FAMI_TIENECOMPUTADOR', 'FAMI_TIENELAVADORA', 
       'FAMI_TIENEHORNOMICROOGAS', 'FAMI_TIENEAUTOMOVIL',
       'FAMI_TIENEMOTOCICLETA', 'FAMI_TIENECONSOLAVIDEOJUEGOS', 
       'FAMI_NUMLIBROS', 'FAMI_COMELECHEDERIVADOS',
       'FAMI_COMECARNEPESCADOHUEVO', 'FAMI_COMECEREALFRUTOSLEGUMBRE', 'ESTU_TIPODOCUMENTO',
       'FAMI_SITUACIONECONOMICA', 'ESTU_DEDICACIONLECTURADIARIA', 
       'ESTU_DEDICACIONINTERNET', 'ESTU_HORASSEMANATRABAJA',
       'ESTU_TIPOREMUNERACION', 'COLE_CODIGO_ICFES', 'COLE_COD_DANE_ESTABLECIMIENTO', 
       'COLE_NOMBRE_ESTABLECIMIENTO',
       'COLE_GENERO', 'COLE_NATURALEZA', 'COLE_CALENDARIO', 'COLE_BILINGUE', 
       'COLE_CARACTER', 'COLE_COD_DANE_SEDE', 'COLE_NOMBRE_SEDE',
       'COLE_SEDE_PRINCIPAL', 'COLE_AREA_UBICACION', 'COLE_JORNADA', 
       'COLE_COD_MCPIO_UBICACION', 'COLE_MCPIO_UBICACION',
       'COLE_COD_DEPTO_UBICACION', 'COLE_DEPTO_UBICACION', 'ESTU_PRIVADO_LIBERTAD', 
       'ESTU_COD_MCPIO_PRESENTACION',
       'ESTU_MCPIO_PRESENTACION', 'ESTU_DEPTO_PRESENTACION', 'ESTU_COD_DEPTO_PRESENTACION',
       'ESTU_INSE_INDIVIDUAL', 'ESTU_NSE_INDIVIDUAL', 'ESTU_NSE_ESTABLECIMIENTO', 
       'ESTU_ESTADOINVESTIGACION', 'ESTU_GENERACION-E']

lista_enc, df = utils.freqEcondeList(df, to_encode)

df["PERCENTIL_GLOBAL"] = df["PERCENTIL_GLOBAL"].replace({"-": 0})
df["PERCENTIL_GLOBAL"].unique()
df["PERCENTIL_GLOBAL"] = df["PERCENTIL_GLOBAL"].fillna(0)
df["PERCENTIL_GLOBAL"] = df["PERCENTIL_GLOBAL"].astype(int)

df = df.fillna(0)

#-----------------------------------------------------------------------------------------------------------------
# Machine Learning
X = df[['ESTU_TIPODOCUMENTO', 'ESTU_NACIONALIDAD', 'ESTU_GENERO',
       'ESTU_FECHANACIMIENTO', 'PERIODO', 'ESTU_CONSECUTIVO',
       'ESTU_ESTUDIANTE', 'ESTU_TIENEETNIA', 'ESTU_PAIS_RESIDE', 'ESTU_ETNIA',
       'ESTU_DEPTO_RESIDE', 'ESTU_COD_RESIDE_DEPTO', 'ESTU_MCPIO_RESIDE',
       'ESTU_COD_RESIDE_MCPIO', 'FAMI_ESTRATOVIVIENDA', 'FAMI_PERSONASHOGAR',
       'FAMI_CUARTOSHOGAR', 'FAMI_EDUCACIONPADRE', 'FAMI_EDUCACIONMADRE',
       'FAMI_TRABAJOLABORPADRE', 'FAMI_TRABAJOLABORMADRE',
       'FAMI_TIENEINTERNET', 'FAMI_TIENESERVICIOTV', 'FAMI_TIENECOMPUTADOR',
       'FAMI_TIENELAVADORA', 'FAMI_TIENEHORNOMICROOGAS', 'FAMI_TIENEAUTOMOVIL',
       'FAMI_TIENEMOTOCICLETA', 'FAMI_TIENECONSOLAVIDEOJUEGOS',
       'FAMI_NUMLIBROS', 'FAMI_COMELECHEDERIVADOS',
       'FAMI_COMECARNEPESCADOHUEVO', 'FAMI_COMECEREALFRUTOSLEGUMBRE',
       'FAMI_SITUACIONECONOMICA', 'ESTU_DEDICACIONLECTURADIARIA',
       'ESTU_DEDICACIONINTERNET', 'ESTU_HORASSEMANATRABAJA',
       'ESTU_TIPOREMUNERACION', 'COLE_CODIGO_ICFES',
       'COLE_COD_DANE_ESTABLECIMIENTO', 'COLE_NOMBRE_ESTABLECIMIENTO',
       'COLE_GENERO', 'COLE_NATURALEZA', 'COLE_CALENDARIO', 'COLE_BILINGUE',
       'COLE_CARACTER', 'COLE_COD_DANE_SEDE', 'COLE_NOMBRE_SEDE',
       'COLE_SEDE_PRINCIPAL', 'COLE_AREA_UBICACION', 'COLE_JORNADA',
       'COLE_COD_MCPIO_UBICACION', 'COLE_MCPIO_UBICACION',
       'COLE_COD_DEPTO_UBICACION', 'COLE_DEPTO_UBICACION',
       'ESTU_PRIVADO_LIBERTAD', 'ESTU_ESTADOINVESTIGACION',
       'ESTU_GENERACION-E']]
# Variable a predecir
y = df['PUNT_GLOBAL']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Modelo XGB
xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
df_xg = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})
#-----------------------------------------------------------------------------------------------------------------
# Database export
conn = utils.bd_conn()
cur = utils.bd_cursor(conn)
engine = utils.bd_engine()

df.to_sql('df', engine, if_exists='replace')
df_copy.to_sql('df_copy', engine, if_exists='replace')
df_xg.to_sql('df_xg', engine, if_exists='replace')