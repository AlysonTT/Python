import pandas as pd
from dash import dash_table, Dash, html

# =============== TD 8 Partie 1.1 ===============
# Lecture de velib et création pour chaque feuille d'une variable
#Version 1
#charge toutes les feuilles dans un dictionnaire
df = pd.read_excel('velib.xlsx', sheet_name=None)

df_util = df['util']
df_noms = df['noms']
df_dates = df['dates']
df_hills = df['hills']

print(df_noms.head())

#Version 2
'''
df_util1 = pd.read_excel('velib.xlsx', sheet_name='util')
df_noms1 = pd.read_excel('velib.xlsx', sheet_name='noms')
df_dates1 = pd.read_excel('velib.xlsx', sheet_name='dates')
df_hills1 = pd.read_excel('velib.xlsx', sheet_name='hills')
'''

# =============== TD 8 Partie 1.2 ===============
#Creation de l'objet
app = Dash(__name__)

#Creation du layout
app.layout = html.Div([
    html.H1("Titre"),

    dash_table.DataTable(
        id='table',
        #colums=[{}],
        data = df_noms.to_dict('records'),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)