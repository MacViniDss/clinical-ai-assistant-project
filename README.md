# Assistente de Decisão Clínica com IA

Este projeto foi desenvolvido como trabalho prático para a disciplina de **Introdução à Inteligência Artificial** da Pós-Graduação. O objetivo é apresentar uma prova de conceito (PoC) de um WebApp integrado a Grandes Modelos de Linguagem (LLMs) para auxiliar na interpretação de diretrizes médicas e personalização de tratamentos.

## Situação-Problema

A prática médica envolve um volume massivo de dados. Pacientes e profissionais de saúde frequentemente enfrentam o desafio de tomar decisões de tratamento baseadas em informações complexas, diretrizes em constante atualização e variáveis individuais.

Neste cenário, a sobrecarga de informações pode dificultar a criação de planos de ação claros e acessíveis para o paciente, além de demandar tempo valioso do médico durante a consulta.

## Objetivo do Projeto

Criar uma ferramenta interativa utilizando a API do Google Gemini (ou similar) para fornecer orientações de tratamento personalizadas. O sistema atua como uma ponte entre o jargão técnico e a compreensão do paciente, funcionando da seguinte forma:

1. **Plano Padrão Base:** A IA estrutura uma base de conhecimento com diretrizes gerais atualizadas sobre determinada condição.
2. **Complemento Clínico:** A ferramenta recebe o _input_ específico de um médico (ex: prescrição de medicamentos, restrições do paciente, histórico médico).
3. **Personalização:** O modelo processa essas informações conjuntas e gera um guia de tratamento compreensível, seguro e totalmente adaptado à realidade daquele paciente.

## Arquitetura e Tecnologias

A aplicação utiliza uma arquitetura baseada em Python, focada em manter o contexto da interação do paciente de forma contínua:

* **Interface Web:** Streamlit, permitindo uma interação fluida em formato de chat.
* **Inteligência Artificial:** Integração via API com modelos LLM (ex: Google Gemini 1.5 Flash).
* **Persistência de Dados:** SQLite para armazenar o histórico médico e as sessões de conversa, garantindo que o modelo "lembre" das prescrições e interações passadas.
* **Engenharia de Prompt:** Uso de _System Instructions_ estritas para garantir que a IA assuma o papel de um assistente analítico e seguro, sem ultrapassar os limites da orientação definida pelo médico.
### Prompt utilizado:
```
Você é um médico renomado endocrinologista e trabalha em um hospital com muitos
pacientes.
Um deles é o seguinte paciente:
(dados do paciente fictício)
Forneça um plano de tratamento personalizado que inclua orientações dietéticas,
exercícios e monitoramento da glicose. Use linguagem simples.
Comece com uma breve introdução sobre a importância do tratamento adequado para
pacientes com diabetes e hipertensão.
Em seguida, forneça orientações específicas para a dieta do paciente, incluindo
recomendações sobre alimentos a serem evitados e alimentos benéficos.
Continue com diretrizes para a prática regular de exercícios físicos, detalhando os tipos
de exercícios, a frequência e a duração ideais.
Aborde o monitoramento da glicose, explicando como o paciente deve realizar os
testes, interpretar os resultados e agir de acordo com as leituras.
Detalhe a prescrição médica para o caso desse paciente.
Conclua com uma recapitulação das principais etapas do plano de tratamento e a
importância de seguir as recomendações.
```
## ⚠️ Aviso Legal

**Este é um projeto estritamente acadêmico.** A ferramenta desenvolvida não substitui, sob nenhuma hipótese, o julgamento clínico, o diagnóstico ou a prescrição de um profissional de saúde qualificado. As respostas geradas pela Inteligência Artificial devem ser sempre revisadas e validadas por um médico responsável antes de qualquer aplicação real.

## Demonstração:
![Gif](https://github.com/user-attachments/assets/17cd92de-6e4f-4fc6-bb4a-45d9fd408658)


### Autor
* Marcus Vinicius
