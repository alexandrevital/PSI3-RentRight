import pandas as pd
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pyarrow.parquet as pq
import shutil

def df_names():
    result = []
    dir_iter = os.scandir('test')
    for f in dir_iter:
        if f.name.endswith('.csv'):
            result.append(f.name[0:-4])
    return sorted(result)

def read_df(df_name, extension='csv', encoding='utf-8', low_memory=False):
    path = f'dataset/{df_name}.{extension}'
    if extension=='csv':
        return __read_csv(path, encoding=encoding, low_memory=low_memory)
    if extension=='parquet':
        return pd.read_parquet(path)
    raise Exception(f"Formato inválido: {extension}")

def __read_csv(path, encoding, low_memory=False):
    try:
        df = pd.read_csv(path, sep=',', encoding=encoding, low_memory=low_memory)
    except:
        df = pd.read_csv(path, sep=';', encoding=encoding, low_memory=low_memory)
    return df

def get_data(filepath):
    dfs = []

    # Iterar sobre os arquivos salvos
    for arquivo in os.listdir('dataset'):
        if arquivo.endswith('.parquet'):  # ou '.csv' para arquivos CSV
            df = pd.read_parquet(os.path.join('dataset', arquivo))  # ou pd.read_csv para CSV
            dfs.append(df)

    # Concatenar todos os dataframes
    df = pd.concat(dfs, ignore_index=True)
    
    categorical_cols = ['type', 'laundry_options', 'parking_options', 'state']  # ajuste conforme necessário

    
    numeric_imputer = SimpleImputer(strategy='mean')

    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_imputer, ['lat', 'long', 'price', 'sqfeet', 'beds', 'baths', 'cats_allowed', 'dogs_allowed', 'smoking_allowed', 'wheelchair_access', 'electric_vehicle_charge', 'comes_furnished']),
            ('cat', categorical_transformer, categorical_cols)
        ])

    
    df_transformed = preprocessor.fit_transform(df)

    
    columns = (['lat', 'long', 'price', 'sqfeet', 'beds', 'baths', 'cats_allowed', 'dogs_allowed', 'smoking_allowed', 'wheelchair_access', 'electric_vehicle_charge', 'comes_furnished'] + 
               preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols).tolist())

    
    df_transformed = pd.DataFrame(df_transformed, columns=columns)

    return df_transformed

def load_data(filepath):
    path = "dataset"
    file = "dataset.csv"
    caminho_completo = os.path.join(path, file)
    
    if os.path.exists(caminho_completo):
        return get_data()
    else:
        make_csv()
        return get_data()

def make_csv():
    df_transformed = get_data('dataset')

    # Salvar como CSV
    csv_filepath = 'dataset.csv'
    df_transformed.to_csv(csv_filepath, index=False)

    # Mover para a pasta 'test'
    destination_folder = 'test'
    os.makedirs(destination_folder, exist_ok=True)  # Cria a pasta 'test' se não existir
    destination_path = os.path.join(destination_folder, csv_filepath)
    shutil.move(csv_filepath, destination_path)
    print(f'Arquivo movido para a pasta {destination_folder}.')
