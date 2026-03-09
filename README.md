# LUSOGUARDA - Sistema interno (MVP funcional)

MVP web para gestão gerencial com base de dados local, pronto para correr no notebook interno.

## Funcionalidades
- Dashboard gerencial com indicadores rápidos
- Cadastro de clientes
- Cadastro e acompanhamento de ordens de transporte
- Base de dados local SQLite (`lusoguarda.db`)
- Sem dependências externas (usa apenas Python padrão)

## Como executar
```bash
python3 app.py
```

Depois aceder a: `http://localhost:5000`

## Observações
- Ao arrancar, o sistema cria automaticamente as tabelas e um cliente/ordem de exemplo.
- Estrutura pronta para migrar para PostgreSQL numa próxima fase.
