import pandas as pd from statsmodels.formula.api import ols 
data = pd.read_excel("/content/sample_data/Book1.xlsx")

#Scatter plot 
import seaborn as sns
sns.set_palette('colorblind')
sns.pairplot(data=data, height=3)
<seaborn.axisgrid.PairGrid at 0x7f9616cd7f50>

#Calculating mean
EURUSDm = data['EURUSD'].mean()
DXYm = data['DXY'].mean()
EXYm = data['EXY'].mean()
CXYm = data['CXY'].mean()

EURUSDm, DXYm, EXYm, CXYm
(1.1876579831932772, 92.15105042016803, 109.85218487394968,
79.93163865546217)

#Calculating median
EURUSDmed = data['EURUSD'].median()
DXYmed = data['DXY'].median()
EXYmed = data['EXY'].median()
CXYmed = data['CXY'].median()
EURUSDmed, DXYmed, EXYmed, CXYmed (1.18715, 92.15, 110.58, 79.67)

#Calculating max 
EURUSDmax = data['EURUSD'].max()
DXYmax = data['DXY'].max()
EXYmax = data['EXY'].max()
CXYmax = data['CXY'].max()
EURUSDmax, DXYmax, EXYmax, CXYmax (1.2325, 96.88, 112.12, 83.07)

reg = ols("EURUSD ~ DXY + EXY + CXY", data = data).fit(cov_type = "HC1") 
reg.summary()