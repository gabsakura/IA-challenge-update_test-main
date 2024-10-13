mes = f"""
WITH dados_filtrados AS (
    SELECT *
    FROM dados
    WHERE strftime('%m', data_registro) = '09' 
    AND strftime('%Y', data_registro) = '2024'
)
SELECT 
    -- Primeiro conjunto: Primeira e última leitura do mês
    (SELECT json_group_array(data_registro) 
     FROM (
         SELECT MIN(data_registro) AS data_registro 
         FROM dados_filtrados 
         UNION ALL 
         SELECT MAX(data_registro) 
         FROM dados_filtrados
     )) AS primeira_ultima_leitura,

    -- Segundo conjunto: Médias de temperatura, corrente e vibrações
    (SELECT json_object(
         'temperatura_media', AVG(temperatura),
         'corrente_media', AVG(corrente),
         'vibracao_base_media', AVG(vibração_base),
         'vibracao_braco_media', AVG(vibracao_braco)
     )
     FROM dados_filtrados) AS medias_dados,

    -- Terceiro conjunto: Dias com dados que passaram do limite (sem duplicação)
    (SELECT json_group_array(DISTINCT strftime('%d/%m/%Y', data_registro)) 
     FROM dados_filtrados 
     WHERE (temperatura > 45 OR corrente > 5 OR vibração_base > 5.5 OR vibracao_braco > 5.5)
    ) AS dias_excedendo_limite;
"""

ranking = f"""
SELECT 
    DATE(data_registro) AS data,
    AVG(temperatura) AS media 
FROM 
    dados 
WHERE 
    strftime('%m', data_registro) = '10' 
    AND strftime('%Y', data_registro) = '2024'
GROUP BY 
    DATE(data_registro) 
ORDER BY 
    media DESC  -- Ordena pela média diária em ordem decrescente
LIMIT 10;  -- Limita os resultados a 10
"""

dia = f"""
SELECT 
    AVG(d.temperatura) AS media_temperatura, 
    AVG(d.corrente) AS media_corrente, 
    AVG(d.vibração_base) AS media_vibracao_base, 
    AVG(d.vibracao_braco) AS media_vibracao_braco,
    MIN(d.data_registro) AS primeira_leitura, 
    MAX(d.data_registro) AS ultima_leitura, 
    l.hora AS hora_limite_excedido, 
    l.dado AS dado_limite_excedido 
FROM 
    dados d 
LEFT JOIN (
    SELECT data_registro AS hora, 'temperatura' AS dado 
    FROM dados 
    WHERE temperatura > 45
    UNION 
    SELECT data_registro AS hora, 'corrente' AS dado 
    FROM dados 
    WHERE corrente > 5
    UNION 
    SELECT data_registro AS hora, 'vibração_base' AS dado 
    FROM dados 
    WHERE vibração_base > 5.5
    UNION 
    SELECT data_registro AS hora, 'vibracao_braco' AS dado 
    FROM dados 
    WHERE vibracao_braco > 5.5
) AS l 
ON DATE(d.data_registro) = DATE(l.hora) 
WHERE DATE(d.data_registro) = '2024-05-21' 
GROUP BY l.hora, l.dado;
"""