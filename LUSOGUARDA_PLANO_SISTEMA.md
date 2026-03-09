# PROJETO LUSOGUARDA — Sistema Integrado (Administrativo, Comercial e Operacional)

## 1) Objetivo do sistema
Criar uma plataforma única para controlar toda a operação da empresa familiar de logística em Portugal, com foco em:
- controlo administrativo e financeiro;
- gestão comercial (clientes, propostas, contratos e faturação);
- operação logística diária (coletas, rotas, entregas, motoristas, viaturas e ocorrências);
- indicadores para tomada de decisão.

---

## 2) Módulos principais

### 2.1 Administrativo/Financeiro
- **Cadastro mestre**: clientes, fornecedores, motoristas, colaboradores, viaturas, armazéns.
- **Contas a pagar/receber**: lançamentos, vencimentos, estado de pagamento.
- **Faturação**: emissão por serviço concluído, integração com comercial e operação.
- **Conciliação financeira**: pagamentos recebidos, custos por viagem e por cliente.
- **Centro de custos**: combustível, portagens, manutenção, salários, subcontratações.

### 2.2 Comercial
- **CRM simples**: leads, clientes ativos, histórico de contactos.
- **Propostas e tabelas de preço**: por rota, volume, peso, tipo de carga e SLA.
- **Contratos**: vigência, anexos, condições comerciais.
- **Pipeline comercial**: oportunidades por fase (novo, proposta, negociação, ganho/perdido).
- **Rentabilidade por cliente**: receita versus custo operacional.

### 2.3 Operacional
- **Ordens de transporte**: criação manual ou via integração (API/EDI).
- **Planeamento de rotas**: alocação por motorista/viatura, capacidade e janela de entrega.
- **Gestão de frota**: manutenção preventiva, seguros, inspeções, documentação.
- **App do motorista (fase 2)**: check-in, prova de entrega (foto/assinatura), ocorrências.
- **Monitorização em tempo real (fase 3)**: geolocalização e estado de entrega.
- **Gestão de incidentes**: atraso, avaria, devolução, dano, extravio.

### 2.4 BI e Indicadores
- Dashboard executivo com:
  - OTIF (on time in full);
  - custo por km;
  - ocupação de frota;
  - margem por cliente/rota;
  - taxa de devoluções e incidentes.

---

## 3) Perfis de utilizador e permissões
- **Administração**: visão total + configurações financeiras e estratégicas.
- **Equipa comercial**: CRM, propostas, contratos, visão de faturação de clientes.
- **Operações/Tráfego**: ordens, rotas, motoristas, viaturas, ocorrências.
- **Financeiro**: contas a pagar/receber, faturação, relatórios financeiros.
- **Motorista**: app simplificada para execução da rota e confirmação de entregas.

Regras recomendadas:
- acesso por perfil (RBAC);
- registo de auditoria (quem alterou o quê e quando);
- proteção de dados (RGPD).

---

## 4) Fluxo ponta-a-ponta (processo macro)
1. Comercial cria cliente e proposta.
2. Cliente aprova proposta e contrato é ativado.
3. Pedido de transporte entra no sistema (manual/API).
4. Operações planeia rota e aloca recursos.
5. Motorista executa coleta/entrega e regista prova.
6. Sistema fecha serviço e envia para faturação.
7. Financeiro acompanha recebimento e margem.
8. Dashboard atualiza KPIs da operação.

---

## 5) Arquitetura tecnológica recomendada (MVP)

### 5.1 Backend
- API REST central com autenticação JWT.
- Linguagens sugeridas: **Node.js (NestJS)** ou **Python (FastAPI)**.
- Banco de dados relacional: **PostgreSQL**.
- Filas (eventos assíncronos): **Redis + BullMQ** (ou Celery no Python).

### 5.2 Frontend Web
- **React + Next.js** para painéis administrativos/comerciais/operacionais.
- Design system com componentes reutilizáveis.

### 5.3 App móvel (fase 2)
- **React Native** para motoristas.

### 5.4 Infraestrutura
- Deploy em cloud (AWS/Azure/GCP).
- CI/CD com GitHub Actions.
- Observabilidade: logs centralizados, alertas e monitorização de uptime.

---

## 6) Modelo de dados inicial (entidades-chave)
- Cliente
- Contrato
- Proposta
- TabelaPreco
- OrdemTransporte
- Rota
- ParagemEntrega
- Motorista
- Viatura
- Ocorrencia
- Fatura
- Pagamento
- CentroCusto

Relacionamentos principais:
- 1 Cliente → N Contratos
- 1 Contrato → N OrdensTransporte
- 1 OrdemTransporte → 1 Rota (MVP)
- 1 Rota → N ParagensEntrega
- 1 OrdemTransporte → N Ocorrencias
- 1 OrdemTransporte → 1 Fatura

---

## 7) Roadmap de implementação

### Fase 1 (8–12 semanas) — MVP Operacional + Comercial básico
- Cadastro mestre
- CRM básico
- Ordens de transporte
- Planeamento de rotas manual
- Fecho de serviço + faturação básica
- Dashboard de KPIs essenciais

### Fase 2 (6–10 semanas) — Mobilidade e automações
- App do motorista
- Prova de entrega digital
- Alertas automáticos de atraso
- Regras de preço avançadas

### Fase 3 (8+ semanas) — Escala e inteligência
- Integrações com ERP/faturação eletrónica
- Otimização de rotas assistida
- Previsão de procura e custos
- Monitorização em tempo real completa

---

## 8) Requisitos não funcionais
- Segurança: encriptação em trânsito (TLS) e dados sensíveis protegidos.
- Performance: resposta < 1s para consultas críticas de operação.
- Disponibilidade: objetivo inicial 99,5%.
- Backup e recuperação: rotina diária + testes de restauração.
- LGPD/RGPD: base legal, consentimento e retenção de dados.

---

## 9) Próximos passos práticos
1. Validar este escopo com a direção da LUSOGUARDA.
2. Priorizar processos críticos do dia 1 (faturação e operação).
3. Definir equipa: PO, analista de processos, tech lead e operação piloto.
4. Desenhar protótipo de ecrãs principais (1 semana).
5. Iniciar desenvolvimento da Fase 1 com entregas quinzenais.

---

## 10) Entregáveis imediatos sugeridos
- Documento de requisitos funcionais detalhado.
- Mapa de processos AS-IS / TO-BE.
- Backlog inicial (épicos e user stories).
- Protótipo navegável.
- Plano de migração de dados (clientes, viaturas, histórico mínimo).

