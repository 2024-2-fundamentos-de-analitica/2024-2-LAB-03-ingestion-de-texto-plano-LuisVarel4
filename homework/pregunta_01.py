import pandas as pd
import re
"""
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
"""
def pregunta_01():
    filepath = 'files/input/clusters_report.txt'

    with open(filepath, "r", encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    current_row = {
        "Cluster": None,
        "Cantidad_de_palabras_clave": None, 
        "Porcentaje_de_palabras_clave": None,
        "Principales_palabras_clave": []
    }

    cluster_start_regex = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%')

    for line in lines:
        line = line.strip()
        if not line:
            continue  

        match = cluster_start_regex.match(line)
        if match:
            if current_row["Cluster"] is not None:
                
                keywords = ' '.join(current_row["Principales_palabras_clave"])
                keywords = re.sub(r'\s+', ' ', keywords)
                keywords = re.sub(r',\s*', ', ', keywords)
                keywords = re.sub(r'\s*,\s*', ', ', keywords)
                keywords = keywords.rstrip('.')
                current_row["Principales_palabras_clave"] = keywords

                data.append(current_row)

            cluster_num = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(',', '.'))

            current_row = {
                "Cluster": cluster_num,
                "Cantidad_de_palabras_clave": cantidad,
                "Porcentaje_de_palabras_clave": porcentaje,
                "Principales_palabras_clave": []
            }

            porcentaje_end = match.end()
            keywords_part = line[porcentaje_end:].strip()
            if keywords_part:
                current_row["Principales_palabras_clave"].append(keywords_part)
        else:
            current_row["Principales_palabras_clave"].append(line)

    if current_row["Cluster"] is not None:
        keywords = ' '.join(current_row["Principales_palabras_clave"])
        keywords = re.sub(r'\s+', ' ', keywords)
        keywords = re.sub(r',\s*', ', ', keywords)
        keywords = re.sub(r'\s*,\s*', ', ', keywords)
        keywords = keywords.rstrip('.')
        current_row["Principales_palabras_clave"] = keywords
        data.append(current_row)

    df = pd.DataFrame(data)

    df.columns = df.columns.map(lambda x: x.strip().lower().replace(" ", "_"))

    return df