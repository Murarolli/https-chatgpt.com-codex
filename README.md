# LUSOGUARDA - Sistema interno (MVP funcional)

MVP web para gestão gerencial com base de dados local, pronto para correr no notebook interno **ou online**.

## Funcionalidades
- Dashboard gerencial com indicadores rápidos
- Cadastro de clientes
- Cadastro e acompanhamento de ordens de transporte
- Base de dados local SQLite (`lusoguarda.db`)
- Sem dependências externas (usa apenas Python padrão)

---

## Opção A (mais simples): usar ONLINE com conta gratuita (Render)
Se você não quer mexer com CMD/terminal local, pode publicar online grátis.

### Passo 1: criar conta grátis
- Criar conta em: https://render.com (pode usar login Google/GitHub)

### Passo 2: subir este projeto para o GitHub
- Crie um repositório no GitHub
- Envie estes arquivos (`app.py`, `README.md`, etc.)

### Passo 3: criar o serviço na Render
1. Clique em **New +** → **Web Service**
2. Conecte o repositório do GitHub
3. Configure:
   - **Build Command:** vazio
   - **Start Command:** `python3 app.py`
4. Clique em **Create Web Service**

A Render vai gerar um link do tipo:
- `https://seu-app.onrender.com`

Pronto: esse link abre no navegador sem precisar CMD no seu notebook.

> Nota: plano gratuito pode "adormecer" se ficar sem uso e demorar alguns segundos para voltar.

---

## Opção B: rodar no próprio notebook (local)

## Importante (para quem é leigo)
Se você abrir só o navegador, não vai funcionar enquanto o sistema não estiver ligado.

Pense assim:
1. Primeiro você **liga o sistema** no terminal.
2. Depois você abre o navegador no endereço local.

### Qual terminal usar?
- **Windows:** Prompt de Comando (CMD) ou PowerShell
- **macOS:** app Terminal
- **Linux:** Terminal

### Passo a passo local
1. Abrir terminal
2. Entrar na pasta do projeto
3. Executar:

```bash
python3 app.py
```

No Windows, se necessário:

```bash
python app.py
```

4. Abrir no navegador:
- `http://localhost:5000`
- se não abrir: `http://127.0.0.1:5000`

---

## Problemas comuns

### "Não criou nada no meu notebook"
Normal: o sistema só cria banco/tabelas quando você executa `python3 app.py`.

### "Não abre no navegador"
- Confirme que o terminal está com o servidor ligado
- Se fechar o terminal, o sistema desliga

### "Python não encontrado"
- Instalar Python 3: https://www.python.org/downloads/
- No Windows, marcar "Add Python to PATH"

---

## Observações
- Ao arrancar, o sistema cria automaticamente as tabelas e um cliente/ordem de exemplo.
- Estrutura pronta para migrar para PostgreSQL numa próxima fase.
