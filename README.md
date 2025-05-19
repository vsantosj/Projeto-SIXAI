# 🌧️ SIXAI Chatbot 

**Resumo:**  
Este projeto é um **chatbot com inteligência artificial**, desenvolvido em grupo por estudantes da **Escola da Nuvem** com propósitos **educacionais** e voltado para soluções de impacto social.

---

## 👥 Integrantes do Projeto

| Nome               | Atividade Principal              | GitHub                                           |
|--------------------|----------------------------------|--------------------------------------------------|
| Viviane Santos     | Desenvolvimento Back-End        | [@viviane-Santos](https://github.com/vsantos)  |
| Luis Kuklinshi      | Lider de Projeto               | [@Luis-Kuklinshi]()      |
| Jessica Picarelli   |Arquiteta de Software           | [@JessicaPicarelli]() |
| Fábio Rocha          | Scrum Master                  | [@Fabio-Rocha]() |
| Bruno Sampaio       | Arquiteto Cloud                | [@Bruno-Sampaio]() |

## 🎯 Objetivo

O chatbot tem como objetivo **informar a população sobre riscos de fortes chuvas**, emitir **alertas de alagamentos** e **prever inundações** em pontos críticos da cidade, de acordo com os locais informados pelos usuários na conversa.

---

## 🧠 Como Funciona

A aplicação foi projetada para receber mensagens dos usuários e oferecer respostas contextualizadas com base em dados meteorológicos e locais de risco previamente mapeados. Utiliza inteligência artificial generativa para fornecer respostas relevantes e alertas de forma humanizada.


### 🛰️ Fluxo da Aplicação

```plaintext
Usuário → Interface Web (Streamlit - EC2) → Amazon Bedrock → Claude 3.5 Sonnet → Resposta → Interface Web
```
## 🎥 Demonstração

![Demonstração do app](imagens/demo.gif)

## 🧠 Aprendizados
- Como usar LLMs em casos de uso reais e sociais.
- Arquitetura de aplicações em nuvem com EC2 e Bedrock.
- Desenvolvimento colaborativo com foco em impacto comunitário.
- Criação de chatbots com memória de contexto.

## 🛠️ Tecnologias Utilizadas
- Python – Lógica do chatbot e comunicação com API  
- Streamlit – Interface web para interação com o usuário  
- Amazon EC2 – Infraestrutura para hospedagem  
- Amazon Bedrock – Integração com modelos de linguagem  
- Claude 3.5 Sonnet – Modelo de LLM usado para gerar respostas

---

🌱 *Tecnologia a serviço da vida: usamos inteligência artificial para proteger comunidades e promover um futuro mais seguro e sustentável frente às mudanças climáticas.*

👤 Autor
---
Feito com 💜 por Viviane Santos

