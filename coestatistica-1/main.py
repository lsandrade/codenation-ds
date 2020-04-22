import pandas as pd
import json

df = pd.read_csv('desafio1.csv', delimiter=',')

print(df.shape)

print(df.head())

print(df.tail())

print(df.info())

print(df.estado_residencia.unique())

#media
print('media')
mean = df.groupby('estado_residencia').pontuacao_credito.apply(pd.DataFrame).mean()
print(mean)

#mediana
print('mediana')
median = df.groupby('estado_residencia').pontuacao_credito.apply(pd.DataFrame).median()
print(median)

#moda
print('moda')
mode = df.groupby('estado_residencia').pontuacao_credito.apply(pd.DataFrame).mode().T[0]
print(mode)

#desvio padrao
print('desvio padrao')
std = df.groupby('estado_residencia').pontuacao_credito.apply(pd.DataFrame).std()
print(std)

print('***')
result = pd.DataFrame([mode, median, mean, std], index=['moda', 'mediana', 'media', 'desvio_padrao'])
print(result)

# result.to_csv('out.csv')

print('to_dict')
result_to_json = result.to_dict()
print(result_to_json)

with open('submission.json', 'w') as outfile:
    json.dump(result_to_json, outfile)
