#!/usr/bin/env python
# coding: utf-8

# # Desafio 6
# 
# Neste desafio, vamos praticar _feature engineering_, um dos processos mais importantes e trabalhosos de ML. Utilizaremos o _data set_ [Countries of the world](https://www.kaggle.com/fernandol/countries-of-the-world), que contém dados sobre os 227 países do mundo com informações sobre tamanho da população, área, imigração e setores de produção.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[31]:


import pandas as pd
import numpy as np
import seaborn as sns
import sklearn as sk
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# In[10]:


# Algumas configurações para o matplotlib.
# %matplotlib inline

from IPython.core.pylabtools import figsize


figsize(12, 8)

sns.set()


# In[11]:


countries = pd.read_csv("countries.csv")


# In[12]:


new_column_names = [
    "Country", "Region", "Population", "Area", "Pop_density", "Coastline_ratio",
    "Net_migration", "Infant_mortality", "GDP", "Literacy", "Phones_per_1000",
    "Arable", "Crops", "Other", "Climate", "Birthrate", "Deathrate", "Agriculture",
    "Industry", "Service"
]

countries.columns = new_column_names

countries.head(5)


# ## Observações
# 
# Esse _data set_ ainda precisa de alguns ajustes iniciais. Primeiro, note que as variáveis numéricas estão usando vírgula como separador decimal e estão codificadas como strings. Corrija isso antes de continuar: transforme essas variáveis em numéricas adequadamente.
# 
# Além disso, as variáveis `Country` e `Region` possuem espaços a mais no começo e no final da string. Você pode utilizar o método `str.strip()` para remover esses espaços.

# ## Inicia sua análise a partir daqui

# In[13]:


# Sua análise começa aqui.
countries.info()


# In[14]:


numerics = ['Pop_density','Coastline_ratio','Net_migration','Infant_mortality','Literacy','Phones_per_1000','Arable','Crops','Other','Climate','Birthrate','Deathrate','Agriculture','Industry','Service']

# ajusta o separador e converte para float
countries[numerics] = countries[numerics].apply(lambda x: x.str.replace(',','.')).astype(float)

countries.info()


# In[15]:


countries.describe()


# In[16]:


countries.shape


# ## Questão 1
# 
# Quais são as regiões (variável `Region`) presentes no _data set_? Retorne uma lista com as regiões únicas do _data set_ com os espaços à frente e atrás da string removidos (mas mantenha pontuação: ponto, hífen etc) e ordenadas em ordem alfabética.

# In[17]:


def q1():
    return sorted([country.strip() for country in countries.Region.unique()])

q1()


# ## Questão 2
# 
# Discretizando a variável `Pop_density` em 10 intervalos com `KBinsDiscretizer`, seguindo o encode `ordinal` e estratégia `quantile`, quantos países se encontram acima do 90º percentil? Responda como um único escalar inteiro.

# In[20]:



def q2():
    discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
    bins = discretizer.fit_transform(countries[["Pop_density"]])
    
    p90 = np.percentile(bins, 90)
    
    return int((bins >= p90).sum())
    
q2()


# # Questão 3
# 
# Se codificarmos as variáveis `Region` e `Climate` usando _one-hot encoding_, quantos novos atributos seriam criados? Responda como um único escalar.

# In[21]:


def q3():
    encoder = OneHotEncoder(sparse=False, dtype=np.int)
    
    region_climate_encoded = encoder.fit_transform(countries[["Region", "Climate"]].dropna())
    return region_climate_encoded.shape[1]

q3()


# ## Questão 4
# 
# Aplique o seguinte _pipeline_:
# 
# 1. Preencha as variáveis do tipo `int64` e `float64` com suas respectivas medianas.
# 2. Padronize essas variáveis.
# 
# Após aplicado o _pipeline_ descrito acima aos dados (somente nas variáveis dos tipos especificados), aplique o mesmo _pipeline_ (ou `ColumnTransformer`) ao dado abaixo. Qual o valor da variável `Arable` após o _pipeline_? Responda como um único float arredondado para três casas decimais.

# In[22]:


test_country = [
    'Test Country', 'NEAR EAST', -0.19032480757326514,
    -0.3232636124824411, -0.04421734470810142, -0.27528113360605316,
    0.13255850810281325, -0.8054845935643491, 1.0119784924248225,
    0.6189182532646624, 1.0074863283776458, 0.20239896852403538,
    -0.043678728558593366, -0.13929748680369286, 1.3163604645710438,
    -0.3699637766938669, -0.6149300604558857, -0.854369594993175,
    0.263445277972641, 0.5712416961268142
]


# In[56]:


def q4():
    
    pipe = Pipeline(steps = [
        ('imputer', SimpleImputer(strategy="median")),
        ('padronizer', StandardScaler())
    ])
    
    numerics = new_column_names[2:]
    
    pipe.fit(countries[numerics])
    
    test = pd.DataFrame([test_country], columns=countries.columns)
    result = pd.DataFrame(pipe.transform(test[numerics]), columns=numerics)
    
    return round(float(result.Arable), 3)

q4()


# ## Questão 5
# 
# Descubra o número de _outliers_ da variável `Net_migration` segundo o método do _boxplot_, ou seja, usando a lógica:
# 
# $$x \notin [Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}] \Rightarrow x \text{ é outlier}$$
# 
# que se encontram no grupo inferior e no grupo superior.
# 
# Você deveria remover da análise as observações consideradas _outliers_ segundo esse método? Responda como uma tupla de três elementos `(outliers_abaixo, outliers_acima, removeria?)` ((int, int, bool)).

# In[58]:


def q5():
    
    q1 = np.percentile(countries.Net_migration.dropna(), 25)
    q3 = np.percentile(countries.Net_migration.dropna(), 75)
    iqr = q3-q1
    
    inf = q1 - 1.5 * iqr
    sup = q3 + 1.5 * iqr
    
    outliers_abaixo = sum(countries.Net_migration < inf)
    outliers_acima = sum(countries.Net_migration > sup)
    removeria = (outliers_abaixo + outliers_acima) / countries.Net_migration.shape[0] < 0.1
    
    return outliers_abaixo, outliers_acima, removeria

q5()


# ## Questão 6
# Para as questões 6 e 7 utilize a biblioteca `fetch_20newsgroups` de datasets de test do `sklearn`
# 
# Considere carregar as seguintes categorias e o dataset `newsgroups`:
# 
# ```
# categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
# newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
# ```
# 
# 
# Aplique `CountVectorizer` ao _data set_ `newsgroups` e descubra o número de vezes que a palavra _phone_ aparece no corpus. Responda como um único escalar.

# In[13]:


def q6():
    # Retorne aqui o resultado da questão 4.
    pass


# ## Questão 7
# 
# Aplique `TfidfVectorizer` ao _data set_ `newsgroups` e descubra o TF-IDF da palavra _phone_. Responda como um único escalar arredondado para três casas decimais.

# In[14]:


def q7():
    # Retorne aqui o resultado da questão 4.
    pass

