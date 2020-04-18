#!/usr/bin/env python
# coding: utf-8

# # Desafio 1
# 
# Para esse desafio, vamos trabalhar com o data set [Black Friday](https://www.kaggle.com/mehdidag/black-friday), que reúne dados sobre transações de compras em uma loja de varejo.
# 
# Vamos utilizá-lo para praticar a exploração de data sets utilizando pandas. Você pode fazer toda análise neste mesmo notebook, mas as resposta devem estar nos locais indicados.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Set up_ da análise

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


black_friday = pd.read_csv("black_friday.csv")


# ## Inicie sua análise a partir daqui

# In[3]:


black_friday.head()


# 

# In[6]:


black_friday.describe()


# 

# In[7]:


black_friday.info()


# 
# ## Questão 1
# 
# Quantas observações e quantas colunas há no dataset? Responda no formato de uma tuple `(n_observacoes, n_colunas)`.

# In[36]:


def q1():
    return black_friday.shape

q1()


# ## Questão 2
# 
# Há quantas mulheres com idade entre 26 e 35 anos no dataset? Responda como um único escalar.

# In[25]:


def q2():
    condicoes = (black_friday['Gender'] == 'F')                & (black_friday['Age'] == '26-35')
    
    return len(black_friday[condicoes])

q2()


# ## Questão 3
# 
# Quantos usuários únicos há no dataset? Responda como um único escalar.

# In[31]:


def q3():
    return int(black_friday.nunique().User_ID)

q3()


# ## Questão 4
# 
# Quantos tipos de dados diferentes existem no dataset? Responda como um único escalar.

# In[41]:


def q4():
    return len(pd.unique(black_friday.dtypes))


q4()


# ## Questão 5
# 
# Qual porcentagem dos registros possui ao menos um valor null (`None`, `ǸaN` etc)? Responda como um único escalar entre 0 e 1.

# In[49]:


def q5():
    is_na = black_friday[black_friday.isna().any(1)].shape[0]
    total_registries = black_friday.shape[0]
    return is_na / total_registries

q5()


# ## Questão 6
# 
# Quantos valores null existem na variável (coluna) com o maior número de null? Responda como um único escalar.

# In[57]:


def q6():
    is_na = black_friday.isna().sum()
    return max(is_na)

q6()


# ## Questão 7
# 
# Qual o valor mais frequente (sem contar nulls) em `Product_Category_3`? Responda como um único escalar.

# In[5]:


def q7():
    return black_friday.Product_Category_3.mode()[0]

q7()


# ## Questão 8
# 
# Qual a nova média da variável (coluna) `Purchase` após sua normalização? Responda como um único escalar.

# In[20]:


def q8():
    purchase = black_friday.Purchase
    purchase_norm = (purchase - purchase.min())                     / (purchase.max() - purchase.min())
    return float(purchase_norm.mean())

q8()


# ## Questão 9
# 
# Quantas ocorrências entre -1 e 1 inclusive existem da variáel `Purchase` após sua padronização? Responda como um único escalar.

# In[30]:


def q9():
    purchase = black_friday.Purchase
    purchase_st = (purchase - purchase.mean())                     / (purchase.max() - purchase.min())
    
    conditions = (purchase_st >= -1) & (purchase_st <= 1)
    return int(purchase_st[conditions].count())
    

q9()


# ## Questão 10
# 
# Podemos afirmar que se uma observação é null em `Product_Category_2` ela também o é em `Product_Category_3`? Responda com um bool (`True`, `False`).

# In[42]:


def q10():
    return bool((black_friday.Product_Category_2.isna() ==
           black_friday.Product_Category_3.isna()).all())
    

q10()

