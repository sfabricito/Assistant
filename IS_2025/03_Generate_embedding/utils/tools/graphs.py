import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv

load_dotenv()
GRAPHS_DIRECTORY = os.getenv('GRAPHS_DIRECTORY')

# Load the data from results.csv
df = pd.read_csv('data/search/results.csv', delimiter=';')
df['Presicion'] = df['Presicion'].astype(str).str.replace(',', '.', regex=False).astype(float)

def averagePrecisionPerModel():
    # Orden deseado de los modelos
    ordered_models = [
        'all-mpnet-base-v2',
        'e5-small-v2',
        'e5-base-v2',
        'e5-large-v2',
        'gte-small',
        'gte-base',
        'gte-large'
    ]


    # Calcular la precisión promedio por modelo
    average_precision = df.groupby('Modelo de Embedding')['Presicion'].mean().reset_index()

    # Aplicar orden personalizado
    average_precision['Modelo de Embedding'] = pd.Categorical(
        average_precision['Modelo de Embedding'],
        categories=ordered_models,
        ordered=True
    )
    average_precision = average_precision.sort_values('Modelo de Embedding').reset_index(drop=True)

    # Crear gráfico de barras
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        x='Modelo de Embedding',
        y='Presicion',
        data=average_precision,
        palette=['lightgrey'] * len(average_precision)
    )

    # Bordes de barras negros
    for bar in ax.patches:
        bar.set_edgecolor('black')
        bar.set_linewidth(1)

    plt.xlabel('Embedding Model')
    plt.ylabel('Average Precision')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardar el gráfico
    plt.savefig(f'{GRAPHS_DIRECTORY}/averagePrecisionPerModel.png')

def averagePrecisionPerQueryType():
    # Calcular la precisión promedio por tipo de query
    average_precision_by_query_type = df.groupby('Tipo de Query')['Presicion'].mean().reset_index()

    # Renombrar los tipos de query de "Tipo X" a "Type X"
    average_precision_by_query_type['Tipo de Query'] = average_precision_by_query_type['Tipo de Query'].str.replace('Tipo', 'Type')

    # Cambiar el nombre de la columna para que se vea mejor en el gráfico
    average_precision_by_query_type.rename(columns={'Tipo de Query': 'Query Type'}, inplace=True)

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        x='Query Type',
        y='Presicion',
        data=average_precision_by_query_type,
        palette=['lightgrey'] * len(average_precision_by_query_type)
    )

    # Aplicar bordes negros a las barras
    for bar in ax.patches:
        bar.set_edgecolor('black')
        bar.set_linewidth(1)

    plt.xlabel('Query Type')
    plt.ylabel('Average Precision')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardar el gráfico
    plt.savefig(f'{GRAPHS_DIRECTORY}/averagePrecisionPerQueryType.png')

def averagePrecisionPerModelAndQueryType():
    # Define the mapping for distance names
    distance_name_mapping = {
        'Euclidean Distance': 'Distancia Euclidiana',
        'Cosine Similiarity': 'Similitud de Coseno'
    }

    # Create a copy of the 'Distancia' column for display, using the mapped names
    df['Distancia_Display'] = df['Distancia'].map(distance_name_mapping)

    # Define the expected display column order
    expected_display_cols = ['Distancia Euclidiana', 'Similitud de Coseno']

    # Create the base pivot table using the display names for columns
    base_pivot = pd.pivot_table(df,
                                values='Presicion',
                                index=['Tipo de Query', 'Modelo de Embedding'],
                                columns='Distancia_Display', # Use the mapped column for pivot
                                aggfunc='mean')

    # Ensure all expected display columns are present in the base_pivot, fill with NaN if not
    for col in expected_display_cols:
        if col not in base_pivot.columns:
            base_pivot[col] = float('nan')

    # Reorder the columns of the base_pivot to match the user's desired order
    base_pivot = base_pivot[expected_display_cols]

    # Calculate the 'Suma total' column for the base pivot table rows (mean of available distance columns)
    base_pivot['Suma total'] = base_pivot[expected_display_cols].mean(axis=1)

    # Initialize a list to hold the rows of the final formatted table
    formatted_output_rows = []

    # Iterate through each Tipo de Query to build the table
    for tipo_query in df['Tipo de Query'].unique():
        # Add the rows for models under the current Tipo de Query
        if tipo_query in base_pivot.index.get_level_values('Tipo de Query'):
            for model_embedding, row_data in base_pivot.loc[tipo_query].iterrows():
                row_dict = {'Tipo de Query': tipo_query, 'Modelo de Embedding': model_embedding}
                for col_name, value in row_data.items():
                    row_dict[col_name] = value
                formatted_output_rows.append(row_dict)

        # Calculate and add the 'Total Tipo X' row
        tipo_query_df = df[df['Tipo de Query'] == tipo_query]
        total_tipo_row_data = {'Tipo de Query': f'Total {tipo_query.replace("Tipo ", "")}', 'Modelo de Embedding': ''}
        for original_dist, display_dist in distance_name_mapping.items():
            total_tipo_row_data[display_dist] = tipo_query_df[tipo_query_df['Distancia'] == original_dist]['Presicion'].mean()

        # Calculate 'Suma total' for 'Total Tipo X' row as the overall mean for that Tipo de Query
        total_tipo_row_data['Suma total'] = tipo_query_df['Presicion'].mean()

    # Calculate and add the 'Suma total' row for the entire table
    overall_total_row_data = {'Tipo de Query': 'Media', 'Modelo de Embedding': ''}
    for original_dist, display_dist in distance_name_mapping.items():
        overall_total_row_data[display_dist] = df[df['Distancia'] == original_dist]['Presicion'].mean()
    overall_total_row_data['Suma total'] = df['Presicion'].mean() # Overall mean of all precision values
    formatted_output_rows.append(overall_total_row_data)

    # Create the final DataFrame from the collected rows
    final_display_df = pd.DataFrame(formatted_output_rows)

    # Define all columns for final display
    final_display_cols = ['Tipo de Query', 'Modelo de Embedding'] + expected_display_cols + ['Suma total']
    final_display_df = final_display_df[final_display_cols]

    # Prepare data for matplotlib table: convert all values to strings with desired formatting
    table_data = []
    current_tipo_query_group = None

    for index, row in final_display_df.iterrows():
        tipo_query_cell = row['Tipo de Query']
        modelo_embedding_cell = row['Modelo de Embedding']
        euclidiana_cell = row['Distancia Euclidiana']
        coseno_cell = row['Similitud de Coseno']
        suma_total_cell = row['Suma total']

        # Special formatting for the very last 'Suma total' row
        if tipo_query_cell == 'Suma total':
            euclidiana_str = f"{euclidiana_cell:.4f}".replace('.', ',') if pd.notna(euclidiana_cell) else ''
            coseno_str = f"{coseno_cell:.4f}".replace('.', ',') if pd.notna(coseno_cell) else ''
            suma_total_str = f"{suma_total_cell:.4f}".replace('.', ',') if pd.notna(suma_total_cell) else ''
            modelo_embedding_cell = '' # Ensure empty for the last total row
        else:
            # Format numerical columns to 2 decimal places and replace '.' with ','
            euclidiana_str = f"{euclidiana_cell:.2f}".replace('.', ',') if pd.notna(euclidiana_cell) else ''
            coseno_str = f"{coseno_cell:.2f}".replace('.', ',') if pd.notna(coseno_cell) else ''
            suma_total_str = f"{suma_total_cell:.2f}".replace('.', ',') if pd.notna(suma_total_cell) else ''

        # Logic to handle empty Tipo de Query for subsequent rows of the same type
        if modelo_embedding_cell != '': # It's a model row
            if tipo_query_cell == current_tipo_query_group:
                tipo_query_cell = ''
            else:
                current_tipo_query_group = tipo_query_cell
        else: # It's a total row ('Total Tipo X' or 'Suma total')
            current_tipo_query_group = None # Reset for next Tipo de Query group

        table_data.append([tipo_query_cell, modelo_embedding_cell, euclidiana_str, coseno_str, suma_total_str])

    # Set up the matplotlib figure and axes for the table
    fig, ax = plt.subplots(figsize=(10, 8)) # Adjust figure size as needed
    ax.axis('off') # Hide axes

    # Define column headers for the matplotlib table
    col_labels = ['Tipo de Query', 'Modelo de Embedding', 'Distancia Euclidiana', 'Similitud de Coseno', 'Suma total']

    # Create the table
    table = ax.table(cellText=table_data,
                    colLabels=col_labels,
                    loc='center',
                    cellLoc='center')

    # Adjust layout and styling
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2) # Scale up the table to make it more readable

    # Add a title if desired
    ax.set_title('AVERAGE de Presicion por Tipo de Query y Modelo de Embedding', fontsize=14, pad=20)

    # Save the table as an image
    plt.savefig(f'{GRAPHS_DIRECTORY}/averagePrecisionPerModelAndQueryType.png')

def averageBestScorePerModelAndQueryType():
    # Define the mapping for distance names
    distance_name_mapping = {
        'Euclidean Distance': 'Distancia Euclidiana',
        'Cosine Similiarity': 'Similitud de Coseno'
    }

    # Create a copy of the 'Distancia' column for display, using the mapped names
    df['Distancia_Display'] = df['Distancia'].map(distance_name_mapping)

    # Define the expected display column order
    expected_display_cols = ['Distancia Euclidiana', 'Similitud de Coseno']

    # Create the base pivot table using the display names for columns
    base_pivot = pd.pivot_table(df,
                                values='Mejor Puntaje Obtenido',
                                index=['Tipo de Query', 'Modelo de Embedding'],
                                columns='Distancia_Display', # Use the mapped column for pivot
                                aggfunc='mean')

    # Ensure all expected display columns are present in the base_pivot, fill with NaN if not
    for col in expected_display_cols:
        if col not in base_pivot.columns:
            base_pivot[col] = float('nan')

    # Reorder the columns of the base_pivot to match the user's desired order
    base_pivot = base_pivot[expected_display_cols]

    # Calculate the 'Suma total' column for the base pivot table rows (mean of available distance columns)
    base_pivot['Suma total'] = base_pivot[expected_display_cols].mean(axis=1)

    # Initialize a list to hold the rows of the final formatted table for display
    table_data = [] # This will be the cellText for plt.table

    current_tipo_query_group = None

    # Iterate through each Tipo de Query to build the table (excluding 'Total Tipo X' rows)
    for tipo_query in df['Tipo de Query'].unique():
        # Flag to determine if it's the first row for the current Tipo de Query group
        is_first_row_in_group = True

        # Add the rows for models under the current Tipo de Query
        if tipo_query in base_pivot.index.get_level_values('Tipo de Query'):
            for model_embedding, row_data in base_pivot.loc[tipo_query].iterrows():
                euclidiana_cell = row_data['Distancia Euclidiana']
                coseno_cell = row_data['Similitud de Coseno']
                suma_total_cell = row_data['Suma total']

                euclidiana_str = f"{euclidiana_cell:.2f}".replace('.', ',') if pd.notna(euclidiana_cell) else ''
                coseno_str = f"{coseno_cell:.2f}".replace('.', ',') if pd.notna(coseno_cell) else ''
                suma_total_str = f"{suma_total_cell:.2f}".replace('.', ',') if pd.notna(suma_total_cell) else ''

                # For model rows, 'Tipo de Query' column should only have the name in the first row of its group
                tipo_query_display = tipo_query if is_first_row_in_group else ''
                is_first_row_in_group = False # Subsequent rows in this group will have empty 'Tipo de Query'

                table_data.append([tipo_query_display, model_embedding, euclidiana_str, coseno_str, suma_total_str])


    # Calculate and add the 'Suma total' row for the entire table
    overall_total_row_data = {'Tipo de Query': 'Suma total', 'Modelo de Embedding': ''}
    for original_dist, display_dist in distance_name_mapping.items():
        overall_total_row_data[display_dist] = df[df['Distancia'] == original_dist]['Mejor Puntaje Obtenido'].mean()
    overall_total_row_data['Suma total'] = df['Mejor Puntaje Obtenido'].mean() # Overall mean of all values

    # Format the 'Suma total' row with 6 decimal places
    euclidiana_total_str = f"{overall_total_row_data['Distancia Euclidiana']:.4f}".replace('.', ',') if pd.notna(overall_total_row_data['Distancia Euclidiana']) else ''
    coseno_total_str = f"{overall_total_row_data['Similitud de Coseno']:.4f}".replace('.', ',') if pd.notna(overall_total_row_data['Similitud de Coseno']) else ''
    suma_total_overall_str = f"{overall_total_row_data['Suma total']:.4f}".replace('.', ',') if pd.notna(overall_total_row_data['Suma total']) else ''

    table_data.append(['Suma total', '', euclidiana_total_str, coseno_total_str, suma_total_overall_str])


    # Set up the matplotlib figure and axes for the table
    fig, ax = plt.subplots(figsize=(12, 10)) # Adjust figure size as needed for better readability
    ax.axis('off') # Hide axes

    # Define column headers for the matplotlib table
    col_labels = ['Tipo de Query', 'Modelo de Embedding', 'Distancia Euclidiana', 'Similitud de Coseno', 'Suma total']

    # Create the table
    table = ax.table(cellText=table_data,
                    colLabels=col_labels,
                    loc='center',
                    cellLoc='center')

    # Apply cell formatting for the header and alignment for numerical columns
    for (row, col), cell in table.get_celld().items():
        if row == 0: # Header row
            cell.set_facecolor("#D3D3D3") # Light gray background for header
            cell.set_text_props(weight='bold', ha='center') # Bold text for header, center align
        elif col >= 2: # Assuming numerical columns start from index 2 (Distancia Euclidiana)
            cell.set_text_props(ha='center') # Center align numbers
        else: # Align text columns to left
            cell.set_text_props(ha='left')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.5) # Scale up the height of rows slightly for better spacing

    # Add a title
    ax.set_title('AVERAGE de Mejor Puntaje Obtenido por Tipo de Query y Modelo de Embedding', fontsize=14, pad=20)

    plt.savefig(f'{GRAPHS_DIRECTORY}/averageBestScorePerModelAndQueryType.png')
    
def expectedResults():
    # Count the occurrences of 'Sí' and 'No' in 'Query Esperado'
    query_esperado_counts = df['Query Esperado'].value_counts()

    # Prepare data for the pie chart
    labels = query_esperado_counts.index.tolist()
    sizes = query_esperado_counts.values.tolist()

    # Create the pie chart
    plt.figure(figsize=(8, 8)) # Set figure size for better appearance
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90) # Add colors
    plt.title('Proporción de Queries con Resultado Esperado')
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot
    plt.savefig(f'{GRAPHS_DIRECTORY}/expectedResults.png')

def modelsInformation():
    # Define the mapping for distance names
    distance_name_mapping = {
        'Euclidean Distance': 'Distancia Euclidiana',
        'Cosine Similiarity': 'Similitud de Coseno'
    }

    # Create a 'Distancia_Display' column using the mapped names
    df['Distancia_Display'] = df['Distancia'].map(distance_name_mapping)

    # Define the expected display column order for distances
    expected_display_cols = ['Distancia Euclidiana', 'Similitud de Coseno']

    # Get unique models
    unique_models = df['Modelo de Embedding'].unique()

    generated_files = []

    for model_name in unique_models:
        # Filter data for the current model
        df_model = df[df['Modelo de Embedding'] == model_name].copy()

        # Create pivot table for the current model
        model_pivot = pd.pivot_table(df_model,
                                    values='Presicion',
                                    index='Tipo de Query',
                                    columns='Distancia_Display',
                                    aggfunc='mean')

        # Ensure all expected display columns are present, fill with NaN if not
        for col in expected_display_cols:
            if col not in model_pivot.columns:
                model_pivot[col] = float('nan')

        # Reorder columns and add 'Suma total'
        model_pivot = model_pivot[expected_display_cols]
        model_pivot['Suma total'] = model_pivot[expected_display_cols].mean(axis=1)

        # Convert pivot table to list of lists for matplotlib table
        table_data = []
        for tipo_query, row_data in model_pivot.iterrows():
            euclidiana_val = row_data['Distancia Euclidiana']
            coseno_val = row_data['Similitud de Coseno']
            suma_total_val = row_data['Suma total']

            euclidiana_str = f"{euclidiana_val:.2f}".replace('.', ',') if pd.notna(euclidiana_val) else ''
            coseno_str = f"{coseno_val:.2f}".replace('.', ',') if pd.notna(coseno_val) else ''
            suma_total_str = f"{suma_total_val:.2f}".replace('.', ',') if pd.notna(suma_total_val) else ''

            table_data.append([tipo_query, euclidiana_str, coseno_str, suma_total_str])

        # Calculate overall 'Suma total' for this model
        overall_model_total = df_model['Presicion'].mean()
        overall_euclidean_total = df_model[df_model['Distancia_Display'] == 'Distancia Euclidiana']['Presicion'].mean()
        overall_cosine_total = df_model[df_model['Distancia_Display'] == 'Similitud de Coseno']['Presicion'].mean()

        # Format overall total for 6 decimal places (as per previous tables)
        overall_euclidean_str = f"{overall_euclidean_total:.4f}".replace('.', ',') if pd.notna(overall_euclidean_total) else ''
        overall_cosine_str = f"{overall_cosine_total:.4f}".replace('.', ',') if pd.notna(overall_cosine_total) else ''
        overall_model_total_str = f"{overall_model_total:.4f}".replace('.', ',') if pd.notna(overall_model_total) else ''

        table_data.append(['Media', overall_euclidean_str, overall_cosine_str, overall_model_total_str])


        # Define column headers for the matplotlib table
        col_labels = ['Tipo de Query', 'Distancia Euclidiana', 'Similitud de Coseno', 'Suma total']

        # Set up the matplotlib figure and axes for the table
        fig, ax = plt.subplots(figsize=(8, 6)) # Adjust size as needed
        ax.axis('off') # Hide axes

        # Create the table
        table = ax.table(cellText=table_data,
                        colLabels=col_labels,
                        loc='center',
                        cellLoc='center')

        # Apply cell formatting for the header and alignment for numerical columns
        for (row, col), cell in table.get_celld().items():
            if row == 0: # Header row
                cell.set_facecolor("#D3D3D3") # Light gray background for header
                cell.set_text_props(weight='bold', ha='center') # Bold text for header, center align
            elif col >= 1: # Assuming numerical columns start from index 1 (Distancia Euclidiana)
                cell.set_text_props(ha='center') # Center align numbers
            else: # Align text columns to left
                cell.set_text_props(ha='left')

        # Adjust table properties
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.0, 1.5) # Scale up the height of rows slightly for better spacing

        # Add a title
        title = f'Precisión por Tipo de Query para Modelo: {model_name}'
        ax.set_title(title, fontsize=14, pad=20)

        # Save the table as an image
        filename = f'{GRAPHS_DIRECTORY}/precision_{model_name.replace("/", "_")}.png'
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close(fig) # Close the figure to free up memory
        f'expectedResults.png'
        generated_files.append(filename)

def precisionPerModelAndQueryType():
    """
    Generates and saves a table displaying the precision for each embedding model and query type,
    categorized by distance metric.
    """
    # Define the mapping for distance names for display purposes
    distance_name_mapping = {
        'Euclidean Distance': 'Distancia Euclidiana',
        'Cosine Similiarity': 'Similitud de Coseno'
    }

    # Create a display column for the distance metric using the mapped names
    df['Distancia_Display'] = df['Distancia'].map(distance_name_mapping)

    # Define the expected order for the distance columns in the output table
    expected_display_cols = ['Distancia Euclidiana', 'Similitud de Coseno']

    # Create a pivot table to structure the precision values
    # The aggregation function is 'mean' since we are displaying the precision which is already calculated.
    # If there were multiple precision values for the same combination, 'mean' would average them.
    pivot_table = pd.pivot_table(df,
                                 values='Presicion',
                                 index=['Tipo de Query', 'Modelo de Embedding'],
                                 columns='Distancia_Display',
                                 aggfunc='mean')

    # Ensure all expected distance columns are present in the pivot table, filling with NaN if one is missing
    for col in expected_display_cols:
        if col not in pivot_table.columns:
            pivot_table[col] = np.nan

    # Reorder the columns to the desired display order
    pivot_table = pivot_table[expected_display_cols]

    # Reset the index to turn the multi-index into columns
    final_df = pivot_table.reset_index()

    # Prepare data for the matplotlib table, including formatting
    table_data = []
    col_labels = ['Tipo de Query', 'Modelo de Embedding'] + expected_display_cols

    # Add the header row to the table data
    table_data.append(col_labels)

    # Populate the table data with the values from the final DataFrame
    for index, row in final_df.iterrows():
        row_data = [row['Tipo de Query'], row['Modelo de Embedding']]
        for col in expected_display_cols:
            # Format the precision values to four decimal places
            precision_value = row[col]
            if pd.notna(precision_value):
                row_data.append(f"{precision_value:.4f}")
            else:
                row_data.append('')  # Append an empty string for missing values
        table_data.append(row_data)

    # Set up the matplotlib figure and axes for the table
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust figure size as needed
    ax.axis('tight')
    ax.axis('off')

    # Create the table using matplotlib
    table = ax.table(cellText=table_data[1:],
                     colLabels=table_data[0],
                     loc='center',
                     cellLoc='center')

    # Adjust table properties for better visualization
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Add a title to the figure
    ax.set_title('Precisión por Modelo de Embedding y Tipo de Query', fontsize=16, pad=20)

    # Save the generated table as a PNG image
    plt.savefig(f'{GRAPHS_DIRECTORY}/precisionPerModelAndQueryType.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

def averagePrecisionPerModelAndQueryTypeSimple():
    """
    Calculates and generates a table of the average precision per embedding model
    and query type, without distinguishing by distance/similarity metric.
    """
    # Calculate the average precision for each combination of Query Type and Embedding Model
    avg_precision = df.groupby(['Tipo de Query', 'Modelo de Embedding'])['Presicion'].mean().reset_index()
    avg_precision.rename(columns={'Presicion': 'Precisión Promedio'}, inplace=True)

    # Initialize a list to hold the structured rows for the final table
    output_rows = []
    
    # Get a unique list of query types to maintain order
    query_types = df['Tipo de Query'].unique()

    # Iterate through each query type to build the table structure
    for query_type in query_types:
        # Get the models corresponding to the current query type
        models_in_type = avg_precision[avg_precision['Tipo de Query'] == query_type]
        for _, model_row in models_in_type.iterrows():
            output_rows.append(model_row.to_dict())

        # Calculate and add the 'Total' row for the current query type
        total_for_type = df[df['Tipo de Query'] == query_type]['Presicion'].mean()
        output_rows.append({
            'Tipo de Query': f'Total {query_type.replace("Tipo ", "")}',
            'Modelo de Embedding': '',
            'Precisión Promedio': total_for_type
        })

    # Calculate and add the final 'Media' (Overall Average) row
    overall_average = df['Presicion'].mean()
    output_rows.append({
        'Tipo de Query': 'Media',
        'Modelo de Embedding': '',
        'Precisión Promedio': overall_average
    })

    # Create the final DataFrame from the structured rows
    final_display_df = pd.DataFrame(output_rows)

    # --- Matplotlib Table Generation ---

    # Prepare data for the matplotlib table, including formatting
    table_data = []
    column_headers = ['Tipo de Query', 'Modelo de Embedding', 'Precisión Promedio']
    current_query_group = None

    for _, row in final_display_df.iterrows():
        query_cell = row['Tipo de Query']
        model_cell = row['Modelo de Embedding']
        precision_val = row['Precisión Promedio']

        # Format the precision value to 4 decimal places, using a comma
        precision_str = f"{precision_val:.4f}".replace('.', ',') if pd.notna(precision_val) else ''

        # Logic to merge cells for the 'Tipo de Query' column
        display_query_cell = query_cell
        if model_cell != '':  # It's a data row for a model
            if query_cell == current_query_group:
                display_query_cell = ''  # Clear the cell if it's the same as the one above
            else:
                current_query_group = query_cell  # Set the new group
        else:  # It's a 'Total' or 'Media' row
            current_query_group = None  # Reset the grouping

        table_data.append([display_query_cell, model_cell, precision_str])

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(8, 6)) # Adjusted size for fewer columns
    ax.axis('off') # Hide the figure axes

    # Create the table
    table = ax.table(cellText=table_data,
                     colLabels=column_headers,
                     loc='center',
                     cellLoc='center')

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.4) # Adjust scale for better readability

    # Style header
    for (i, j), cell in table.get_celld().items():
        if i == 0: # Header row
            cell.set_text_props(weight='bold')
        # Bold the 'Total' and 'Media' rows
        if "Total" in str(table_data[i-1][0]) or "Media" in str(table_data[i-1][0]):
            cell.set_text_props(weight='bold')


    # Add a title to the plot

    # Save the table as a high-resolution image
    # Make sure the GRAPHS_DIRECTORY is defined in your script
    # plt.savefig(f'{GRAPHS_DIRECTORY}/averagePrecisionPerModelAndQueryType_Simple.png', bbox_inches='tight', dpi=300)

        # Save the generated table as a PNG image
    plt.savefig(f'{GRAPHS_DIRECTORY}/1precisionPerModelAndQueryType.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

# To run this function, you would call it like this:
# averagePrecisionPerModelAndQueryTypeSimple()

# To run this function, you would call it as follows:
# precisionPerModelAndQueryType()

def generateAllGraphs():
    averagePrecisionPerModel()
    averagePrecisionPerQueryType()
    averagePrecisionPerModelAndQueryType()
    averageBestScorePerModelAndQueryType()
    expectedResults()
    modelsInformation()
    precisionPerModelAndQueryType()
    averagePrecisionPerModelAndQueryTypeSimple()