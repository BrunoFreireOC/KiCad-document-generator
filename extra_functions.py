import csv

def group_bom(input_csv, output_csv):
    # Lê os cabeçalhos e dados do CSV original
    with open(input_csv, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames  # Cabeçalhos dinâmicos
        rows = list(reader)

    # Verifica campos obrigatórios
    required_fields = {'Refs', 'Value', 'Qty'}
    if not required_fields.issubset(fieldnames):
        raise ValueError("O CSV não possui os campos obrigatórios: 'Refs', 'Value', 'Qty'")

    # Dicionário para agrupamento (chave: Value + Footprint + DNP)
    components = {}
    
    for row in rows:
        # Cria chave de agrupamento (ajuste conforme seus campos relevantes)
        key = (row.get('Value', ''), (row.get('Footprint', '')), (row.get('DNP', '')))
        
        if key not in components:
            # Cria nova entrada mantendo todos os campos originais
            components[key] = row.copy()
            components[key]['Refs'] = [row['Refs']]
            components[key]['Qty'] = int(row['Qty'])
        else:
            # Atualiza referências e quantidade
            components[key]['Refs'].append(row['Refs'])
            components[key]['Qty'] += int(row['Qty'])

    # Prepara dados para escrita
    grouped_rows = []
    for key in components:
        entry = components[key]
        entry['Refs'] = ','.join(entry['Refs'])  # Junta as referências
        entry['Qty'] = str(entry['Qty'])  # Converte Qty para string
        grouped_rows.append(entry)

    # Escreve o novo CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(grouped_rows)
