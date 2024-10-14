manual_instrucoes = """
Manual de Instruções para Motores de Braço Robótico
1. Introdução
Este manual contém informações sobre a operação segura e eficiente dos motores utilizados em um braço robótico. Ele fornece orientações para minimizar os riscos associados a fatores como temperatura, corrente e vibrações excessivas, garantindo a longevidade dos componentes do sistema.

2. Especificações dos Motores
Tipo de Motor: Motor de passo
Faixa de Temperatura de Operação: 0°C a 45°C
Corrente Nominal: 5 A
Nível Máximo de Vibração Tolerada: 5.5 mm/s²

3. Riscos de Operação
3.1 Riscos de Temperatura Elevada
Perigo: Temperaturas elevadas acima dos níveis operacionais recomendados (acima de 45°C) podem causar o seguinte:

Danos aos componentes internos do motor, como isolamento dos enrolamentos.
Aumento da resistência elétrica, levando a um aquecimento adicional.
Falha prematura dos rolamentos devido à dilatação térmica.
Desgaste acelerado dos materiais e perda de precisão no controle de movimento.
Consequências:

O desempenho do braço robótico será comprometido.
Há um risco elevado de falhas catastróficas que podem causar a interrupção total das operações.
Medidas de Correção:

Instale sensores de temperatura próximos aos motores para monitoramento contínuo.
Utilize dissipadores de calor ou sistemas de refrigeração (ventiladores, radiadores) para dissipar o calor.
Certifique-se de que o ambiente de operação do braço robótico tenha ventilação adequada ou controle de temperatura.
Reduza a carga operacional do braço robótico para diminuir o esforço do motor e, consequentemente, a geração de calor.

3.2 Riscos de Corrente Elevada
Perigo: Correntes acima do limite nominal (5 A) resultam em:

Sobrecarga nos enrolamentos dos motores, causando aumento significativo da temperatura.
Queima dos enrolamentos, resultando em curto-circuitos ou falha total do motor.
Redução drástica da vida útil do motor devido à degradação acelerada dos componentes.
Consequências:

Danos permanentes ao motor, necessitando substituição.
Falha completa do braço robótico, com riscos de acidentes operacionais.
Medidas de Correção:

Use drivers de motor com proteção contra sobrecorrente para limitar o fluxo de corrente excessiva.
Ajuste os parâmetros de controle do motor (corrente de fase, microstepping) para operar dentro dos limites seguros.
Verifique periodicamente as fontes de alimentação para garantir que forneçam correntes estáveis.
Distribua a carga entre múltiplos motores, se possível, para evitar sobrecarga em um único componente.

3.3 Riscos de Vibração Excessiva
Perigo: Vibrações muito elevadas (acima de 5.5 mm/s²) podem resultar em:

Desgaste acelerado dos rolamentos e eixos do motor.
Perda de precisão no controle de posicionamento, causando movimentos erráticos ou imprecisos do braço robótico.
Afrouxamento de componentes mecânicos, que podem comprometer toda a estrutura do sistema.
Consequências:

Redução da precisão operacional e perda de eficiência.
Danos progressivos aos motores, eixos e engrenagens, aumentando os custos de manutenção.
Medidas de Correção:

Instale amortecedores de vibração entre os motores e a estrutura do braço robótico.
Realize inspeções regulares dos rolamentos e do alinhamento mecânico do sistema.
Reduza as velocidades de operação e acelerações, para diminuir o impacto de vibrações.
Certifique-se de que o braço robótico esteja montado em uma superfície estável e livre de outras fontes de vibração.

4. Manutenção Preventiva
Para garantir a vida útil prolongada dos motores e a eficiência do braço robótico, siga estas práticas de manutenção preventiva:

Verificações diárias de temperatura durante a operação.
Inspeção mensal dos rolamentos para verificar folgas ou desgastes.
Monitoramento semanal da corrente de operação para garantir que está dentro do especificado.
Lubrificação dos componentes móveis do braço conforme especificado no manual de manutenção.

5. Procedimentos de Emergência
Em caso de falhas ou operação anormal:

Desligue imediatamente o braço robótico.
Verifique as leituras de temperatura e corrente para identificar possíveis causas.
Inspecione visualmente os motores e rolamentos em busca de sinais de desgaste ou danos.
Substitua qualquer motor danificado ou sobreaquecido antes de retomar as operações.
"""

formato_pdf = f"""
[Não exiba essa linha. Caso o usuário peça esse relatório em outro idioma, traduza o relatório para esse idioma]
Relatório Técnico
Data do Relatório: [Dia de hoje, no formato dia/mês/ano]
Empresa/Organização: FIAP em parceria com a Reply
Nome do Técnico ou Engenheiro Responsável: [Seu nome] + Grupo Failguard
1. Identificação da Máquina
Nome/Modelo da Máquina: BR-FGRF
Número de Série: 2512A
Localização: Linha de Montagem
2. Resumo Executivo
- Objetivo do Relatório: [Descreva o objetivo do relatório, considerando o período de tempo analisado (diário, semanal, mensal ou anual), o desempenho da máquina e possíveis desvios nos limites operacionais. Quanto mais próximos os dados estiverem dos limites, mais relevante será o detalhamento das ocorrências e mais leituras ultrapassaram o limite.]
- Principais Constatações: [Descreva as principais constatações sobre o desempenho da máquina no período em questão. Destaque dias ou ciclos em que os limites foram ultrapassados, observando a frequência e a gravidade dessas ocorrências.]
3. Descrição Técnica da Máquina
Especificações Técnicas: 
3.1. Estrutura Mecânica
- Eixos: 3 eixos controlados individualmente por motores de passo.
- Material: Estrutura de plástico.
- Capacidade de carga: Entre 1 kg a 5 kg.
3.2. Motores de Passo
Quantidade: 4 motores de passo controlados pelo CNC Shield.
Drivers: DRV8825 ou A4988 para controle dos motores.
Resolução: 1,8° por passo, com microstepping configurável.
Tensão de operação: 12V a 24V.
Corrente nominal: Dependendo do motor, entre 1.2A e 2.8A por fase.
3.3. Sensores
Sensor de Corrente (ACS712):
Faixa de medição: ±5A, ±20A ou ±30A, conforme o modelo.
Precisão: ±1.5%.
Interface: Analógica, leitura via Arduino Mega.
Sensor de Vibração (MPU6050):
Tipo: Acelerômetro e giroscópio.
Faixa de medição (acelerômetro): ±2g, ±4g, ±8g, ±16g.
Faixa de medição (giroscópio): ±250, ±500, ±1000, ±2000 °/s.
Interface: I2C, conectado ao ESP32.
Sensor de Temperatura (AMG8833):
Tipo: Matriz de sensores de infravermelho.
Faixa de medição: 0°C a 80°C.
Precisão: ±2.5°C.
Interface: I2C, conectado ao ESP32
3.4. Microcontroladores
Controle do Braço:
Microcontrolador: Arduino Mega.
Controle dos motores: Através de CNC Shield, utilizando drivers para motores de passo.
Envio de Dados:
Microcontrolador: ESP32.
Comunicação: Wi-Fi para enviar os dados coletados dos sensores para o banco de dados.
Interface com sensores: I2C e analógico.
3.5. Fonte de Alimentação
Tensão de operação: 12V a 24V.
Corrente: 5A a 10A (variável conforme os motores e sensores).
3.6. Software
 - Controle dos motores: Através de bibliotecas de controle de CNC ou motor de passo no Arduino Mega.
 - Coleta de Dados: O Arduino Mega coleta os dados dos sensores e envia para o ESP32.
 - Envio para o banco de dados: O ESP32 transmite os dados via Wi-Fi.
Componentes Principais:
    Câmera térmica para monitoramento da temperatura - AMG88xx
    Sensores de vibração - MPU6050
    Sensor de corrente elétrica - ACS712
    Controlador de movimento - Arduino Mega / CNC Shield
    Sistema de comunicação - Esp32
4. Histórico de Operação
Horas de Trabalho: 117 Horas
Ciclos de Operação: 12.037 Ciclos
Condições de Operação:
Temperatura ambiente média: 25°C
Temperatura média do braço: [Temperatura do braço]
Corrente média dos motores: [Corrente média]
Vibração da base: [Média da vibração na base]
Vibração do braço: [Média da vibração no braço]
Dias ou Ciclos com limites de leitura ultrapassados:
[Listar as datas ou ciclos em que os limites operacionais foram ultrapassados, em ordem crescente. Caso os dias ou ciclos em sequência sejam maiores que 4, agrupe-os.
Exemplo:
07/10/2024
18/10/2024...20/10/2024
Se o período de tempo for 'Diário', troque essa lista pela lista com as horas que um dado passou do limite. Por exemplo: 
Corente - 08:00
Temeperatura - 08:15
Vibração da base - 08:30 
]
5. Procedimentos de Inspeção ou Manutenção
Métodos Utilizados: Os dados de temperatura, corrente e vibração foram monitorados continuamente em intervalos de tempo regulares durante a operação da máquina.
Ferramentas e Instrumentos: 
    Câmera térmica para monitoramento da temperatura
    Sensores de vibração (3 pontos do braço)
    Sensor de corrente elétrica para medição da corrente dos motores
    Critérios de Avaliação: Os limites de operação para temperatura, corrente e vibração foram baseados no manual de instruções do braço robótico.
Critérios de Avaliação: Os limites de operação para temperatura, corrente e vibração são delimitados segundoo manual de instruções do braço robótico.
6. Diagnóstico e Condição da Máquina
Desempenho Atual: [Descreva o desempenho geral da máquina durante o período, com base nos dados coletados e nos dias/ciclos em que os limites foram ultrapassados.]
Análise de Vibrações, Ruídos, etc.: [Descreva observações sobre possíveis vibrações, ruídos ou desvios durante a operação com base nos dados coletados e nos dias/ciclos em que os limites foram ultrapassados.]
Desgaste e Danos: [Informe se foram observados desgastes ou danos nos componentes principais.]
7. Recomendações
Reparos Necessários: [Descreva se há necessidade de reparos imediatos ou se a máquina está operando corretamente.]
Manutenção Preventiva: [Recomendações de manutenção preventiva, como verificação de motores, sensores ou ajustes no ciclo de operação para evitar sobrecargas.]
Ações Corretivas: [Informe se há necessidade de ações corretivas no momento ou se apenas a manutenção preventiva é suficiente.]
8. Conclusão
Resumo das Condições: [Faça um resumo das condições operacionais da máquina no período, considerando os dados coletados e os dias/ciclos com desvios.]
Prognóstico: [Descreva a expectativa de desempenho da máquina, com base nas condições observadas, e se procedimentos de manutenção preventiva forem seguidos.]
"""
