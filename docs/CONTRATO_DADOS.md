# Contrato de dados — acidentes em rodovias federais

## Fonte oficial

A fonte primária deste projeto é o portal de Dados Abertos da Polícia Rodoviária Federal (PRF):

- catálogo: https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf
- dicionário de acidentes: https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dicionario-acidentes

A PRF informa que a base BAT (Boletim de Acidente de Trânsito) é atualizada mensalmente e disponibiliza arquivos CSV agrupados por ocorrência, por pessoa e, a partir de 2017, por pessoa com todas as causas e tipos de acidentes.

## Unidade de análise inicial

A primeira camada analítica usará **acidentes agrupados por ocorrência**. Essa escolha evita contar uma mesma ocorrência várias vezes em análises cujo denominador é o número de acidentes. Bases agrupadas por pessoa somente serão usadas quando a pergunta exigir características de vítimas ou envolvidos.

Não é permitido concatenar silenciosamente bases com granularidades diferentes.

## Janela temporal

O catálogo oficial contém séries históricas desde 2007 e arquivos para 2026. O projeto deve registrar, a cada ingestão, os anos efetivamente baixados e a data da coleta. Dados do ano corrente devem ser tratados como potencialmente parciais e não podem ser comparados como ano completo sem ajuste ou ressalva explícita.

## Mudança de sistema de origem

Segundo o dicionário oficial, os registros têm origem em dois sistemas: **BR-Brasil**, utilizado nacionalmente entre 2007 e 2016, e **BAT**, utilizado desde 2017. Portanto, análises temporais que atravessem 2016/2017 devem testar e documentar possíveis quebras de definição, cobertura ou estrutura antes de interpretar tendências.

## Regras mínimas de qualidade

Antes de qualquer estatística ou gráfico publicado, a ingestão deve validar:

1. arquivo não vazio e formato CSV legível;
2. presença das colunas mínimas exigidas pela análise;
3. chave de ocorrência disponível e percentual de duplicidade documentado;
4. datas válidas e coerentes com o ano declarado do arquivo;
5. valores ausentes quantificados por variável;
6. categorias desconhecidas ou inesperadas registradas, nunca descartadas silenciosamente;
7. coordenadas, quando usadas, dentro de limites plausíveis e com ausências explicitadas;
8. variáveis numéricas verificadas quanto a valores impossíveis ou fora de domínio;
9. número de linhas antes e depois de cada filtro registrado;
10. transformações reproduzíveis por código, sem edição manual do dado bruto.

## Camadas de dados

- `raw`: cópia imutável do arquivo obtido da fonte oficial, acompanhada de metadados de coleta e hash quando a ingestão for implementada;
- `processed`: dados tipados, normalizados e derivados exclusivamente por pipeline reproduzível;
- `outputs`: tabelas e agregações aprovadas para consumo pelo dashboard.

Arquivos brutos volumosos não devem ser versionados no Git sem justificativa. O repositório deve preferir scripts de aquisição e metadados reproduzíveis.

## Regras estatísticas

Contagens, taxas e comparações devem declarar unidade de análise, período, filtros e denominador. Diferenças observadas não serão descritas como efeitos causais sem desenho de identificação apropriado. Comparações entre regiões ou anos devem considerar exposição; contagens absolutas de acidentes, isoladamente, não medem risco de circulação.

## Limitações conhecidas

Os registros representam acidentes atendidos/registrados no escopo da PRF em rodovias federais e não equivalem a todos os sinistros de trânsito do Brasil. Mudanças operacionais, de sistema, classificação e cobertura podem afetar comparabilidade. O ano corrente pode estar incompleto devido à atualização mensal.

## Gate para próxima etapa

A engenharia de dados somente poderá liberar resultados para estatística após produzir um relatório automático de qualidade contendo, no mínimo: linhas ingeridas, período, duplicidades, ausências, categorias inesperadas, validações de domínio e resultado geral do gate.
