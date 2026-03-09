# LUSOGUARDA - Sistema interno (MVP funcional)

MVP web para gestão gerencial com base de dados local, pronto para correr no notebook interno.

## Funcionalidades
- Dashboard gerencial com indicadores rápidos
- Cadastro de clientes
- Cadastro e acompanhamento de ordens de transporte
- Base de dados local SQLite (`lusoguarda.db`)
- Sem dependências externas (usa apenas Python padrão)

## Importante (para quem é leigo)
Se você abrir só o navegador, não vai funcionar enquanto o sistema não estiver ligado.

Pense assim:
1. Primeiro você **liga o sistema** no terminal.
2. Depois você abre o navegador no endereço local.

---

## Qual terminal e qual programa usar?

### Windows
- **Programa 1 (terminal):** Prompt de Comando (CMD) ou PowerShell
- **Programa 2 (navegador):** Chrome / Edge / Firefox

### macOS
- **Programa 1 (terminal):** Terminal
- **Programa 2 (navegador):** Safari / Chrome / Firefox

### Linux
- **Programa 1 (terminal):** Terminal da distribuição
- **Programa 2 (navegador):** Chrome / Firefox

---

## Passo a passo (simples)

### 1) Confirmar Python instalado
No terminal, execute:

```bash
python3 --version
```

Se aparecer algo como `Python 3.x.x`, está OK.

> No Windows, se `python3` não funcionar, teste `python --version`.

### 2) Entrar na pasta do projeto
No terminal, vá para a pasta onde estão os arquivos (`app.py`, `README.md`):

```bash
cd /caminho/da/pasta/do/projeto
```

### 3) Ligar o sistema
Execute:

```bash
python3 app.py
```

> No Windows, se necessário:

```bash
python app.py
```

Quando estiver correto, aparece algo como:

```text
Servidor em http://localhost:5000
```

### 4) Abrir no navegador
Com o terminal ainda aberto, abra:

- `http://localhost:5000`

Se quiser, teste também:
- `http://127.0.0.1:5000`

---

## Problemas comuns

### "Não abre no navegador"
- Verifique se o terminal está com o servidor rodando.
- Se fechou o terminal, o sistema desliga.
- Rode de novo `python3 app.py` e tente novamente.

### "Porta em uso"
Se aparecer erro de porta 5000 ocupada, feche outros programas que usem essa porta e rode de novo.

### "Python não encontrado"
Instale Python 3 e marque a opção de adicionar ao PATH (no Windows).

---

## Como parar o sistema
No terminal onde está rodando, pressione:

- `Ctrl + C`

---

## Observações
- Ao arrancar, o sistema cria automaticamente as tabelas e um cliente/ordem de exemplo.
- Estrutura pronta para migrar para PostgreSQL numa próxima fase.
