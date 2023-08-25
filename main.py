import pandas as pd
import quantstats as qs
import plotille

dados = pd.read_csv('dados_empresas.csv')

dados = dados[dados['volume_negociado'] > 1000000]


dados['retorno'] = dados.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
dados['retorno'] = dados.groupby('ticker')['retorno'].shift(-1)

dados['ranking_ebit_ev'] = dados.groupby('data')['ebit_ev'].rank(ascending=False)
dados['ranking_roic'] = dados.groupby('data')['roic'].rank(ascending=False)

dados['ranking_final'] = dados['ranking_ebit_ev'] + dados['ranking_roic']
dados['ranking_final'] = dados.groupby('data')['ranking_final'].rank()

# print (dados[dados['data'] == '2016-01-31'].sort_values('ranking_final'))

# Carteira de até 10 ações
# print(dados[dados['ranking_final'] <= 10])

# Carteira por data
# print(dados[dados['data'] == '2016-01-31'])

rentabilidade_por_carteiras = dados.groupby('data')['retorno'].mean()
rentabilidade_por_carteiras = rentabilidade_por_carteiras.to_frame()


rentabilidade_por_carteiras['modelo'] = (1 + rentabilidade_por_carteiras['retorno']).cumprod() - 1

rentabilidade_por_carteiras = rentabilidade_por_carteiras.shift(1).dropna()



# dWEGE = dados[dados['ticker'] == 'WEGE3']
# print (dWEGE)


# ---------------------------------------------- IBOVESPA ----------------------------------------------

ibov = pd.read_csv('ibov.csv')

retornos_ibov = ibov['fechamento'].pct_change().dropna()
retornos_ibov_acum = (1 + retornos_ibov).cumprod() - 1

rentabilidade_por_carteiras['ibovespa'] = retornos_ibov_acum.values
rentabilidade_por_carteiras = rentabilidade_por_carteiras.drop('retorno', axis = 1)


qs.extend_pandas()
rentabilidade_por_carteiras.index = pd.to_datetime(rentabilidade_por_carteiras.index)


# print(rentabilidade_por_carteiras)

rentabilidade_ao_ano = (1 + rentabilidade_por_carteiras.loc['2023-06-30', 'modelo']) ** (1/7.5) - 1

print(rentabilidade_ao_ano)


# qs.plots.monthly_heatmap(rentabilidade_por_carteiras['modelo'])
# rentabilidade_por_carteiras['ibov'].plot_monthly_heatmap()
