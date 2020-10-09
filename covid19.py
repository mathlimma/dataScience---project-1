#start by installing python through pyenv (use version 3.5.6 for scipy sake)=> https://realpython.com/intro-to-pyenv/
#scipy and other packages => https://www.scipy.org/install.html#pip-install

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas import DataFrame
from scipy import stats

covid = pd.read_csv(r'caso.csv', encoding = "utf-8")

#primeiro ordenaremos pela data de forma ascendente (primeiro dia ao ultimo)
covidRecife = covid[covid.city == 'Recife'].sort_values(by=['date'], ascending=True)

#resetaremos o índice da tabela original e apresentaremos o índice da tabela almejada
covidRecife.reset_index(inplace=True, drop=True)
covidRecife.tail()

#apresentação do gráfico da quantidade de mortes total do dia
plt.plot(covidRecife['order_for_place'], (covidRecife['deaths']))

#first try with a for loop
def sub_column_value(newcolumn, subcolumn, table):
    table[newcolumn] = 0
    for index, i in enumerate(subcolumn):
        if index > 0:
            table[newcolumn][index] = (subcolumn[index] - subcolumn[index-1])

sub_column_value('deaths_per_day', covidRecife.deaths, covidRecife)
         
covidRecife.tail()

#death_per_day bar graph
covidRecife['deaths_per_day'].plot.bar(figsize=(30,10))

# covid in São Paulo
covidSP = covid[covid.city == 'São Paulo'].sort_values(by=['date'], ascending=True)
covidSP.reset_index(inplace=True, drop=True)
covidSP.tail()

# new column deaths_per_day in SP
sub_column_value('deaths_per_day', covidSP.deaths, covidSP)
covidSP.tail()

# graph of deaths in SP
plt.plot(covidSP['order_for_place'], (covidSP['deaths']))

# bar graph of deaths per day in SP
covidSP['deaths_per_day'].plot(kind="bar", figsize=(30,10))

# deaths comparison graph between Recife and São Paulo
plt.plot(covidRecife['order_for_place'], covidRecife['deaths'], label="line 1")
plt.plot(covidSP['order_for_place'], covidSP['deaths'], label="line 2")
# linha azul => recife / linha laranja => SP

# comparison graph of deaths per day between Recife and São Paulo
plt.plot(covidRecife['order_for_place'], covidRecife['deaths_per_day'], label="line 1")
plt.plot(covidSP['order_for_place'], covidSP['deaths_per_day'], label="line 2")
# linha azul => recife / linha laranja => SP

# deaths per day per 1 million inhabitants function without for loop 
def deaths_per_day_per_1kk(newcolumn, table):
    population_per_1kk = table.estimated_population_2019[0] / 1000000
    table[newcolumn] = table.deaths_per_day / population_per_1kk
    return table

deaths_per_day_per_1kk('deaths_per_day_per_1kk_inhabitants', covidRecife)

deaths_per_day_per_1kk('deaths_per_day_per_1kk_inhabitants', covidSP)

# comparison graph of deaths per day per 1 million inhabitants between Recife and São Paulo
plt.plot(covidRecife['order_for_place'], covidRecife['deaths_per_day_per_1kk_inhabitants'], label="line 1")
plt.plot(covidSP['order_for_place'], covidSP['deaths_per_day_per_1kk_inhabitants'], label="line 2")
# linha azul => recife / linha laranja => SP

# statistical data about covidRecife
covidRecife.describe()

# statistical data about covidSP
covidSP.describe()

# boxplot
plt.boxplot([covidRecife.deaths_per_day_per_1kk_inhabitants, covidSP.deaths_per_day_per_1kk_inhabitants], labels=['Recife', 'São Paulo'])

# here i gathered the informations about deaths per day from both cities
crec_dp1kk = covidRecife.deaths_per_day_per_1kk_inhabitants[0:136:1]
csp_dp1kk = covidSP.deaths_per_day_per_1kk_inhabitants[0:136:1]

# here i concatenate both DataFrames and change the name of the tables using keys
df_rec_sp = pd.concat([crec_dp1kk, csp_dp1kk], axis=1, keys=['deaths_per_day_per_1kk_in_Recife', 'deaths_per_day_per_1kk_in_Sao_Paulo'])

df_rec_sp.describe()

df_rec_sp.plot(kind='line', figsize=[10, 5])
df_rec_sp.plot(kind='box', figsize=[10, 5])

# check if the difference follows the gaussian
df_rec_sp['dpdp1kk_difference'] = df_rec_sp['deaths_per_day_per_1kk_in_Recife'] - df_rec_sp['deaths_per_day_per_1kk_in_Sao_Paulo']

# histogram
df_rec_sp['dpdp1kk_difference'].plot(kind='hist')

# Shapiro-Wilk normality test (value, p-value). Null hypothesis: the deaths in recife are not normally distributed.
stats.shapiro(df_rec_sp['dpdp1kk_difference'])
# a p-value less than the critical value shapiro => return (critical value, p-value) indicates that the null hypothesis was rejected

# executing the t-test
stats.ttest_rel(df_rec_sp['deaths_per_day_per_1kk_in_Recife'], df_rec_sp['deaths_per_day_per_1kk_in_Sao_Paulo'])

# checking symmetry
df_rec_sp['dpdp1kk_difference'].plot(kind='box')

# wilcoxon test
stats.wilcoxon(df_rec_sp['deaths_per_day_per_1kk_in_Recife'], df_rec_sp['deaths_per_day_per_1kk_in_Sao_Paulo'])