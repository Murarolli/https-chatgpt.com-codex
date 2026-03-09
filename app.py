from __future__ import annotations

import html
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lusoguarda.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nif TEXT,
    cidade TEXT,
    contato TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ordens_transporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    origem TEXT NOT NULL,
    destino TEXT NOT NULL,
    status TEXT NOT NULL,
    valor REAL NOT NULL DEFAULT 0,
    data_entrega_prevista TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
"""


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(SCHEMA_SQL)
        client_count = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        if client_count == 0:
            now = datetime.utcnow().isoformat()
            conn.execute(
                "INSERT INTO clientes (nome, nif, cidade, contato, created_at) VALUES (?, ?, ?, ?, ?)",
                ("Cliente Exemplo Lda", "501234567", "Guarda", "gerencia@cliente.pt", now),
            )
            conn.execute(
                "INSERT INTO ordens_transporte (cliente_id, origem, destino, status, valor, data_entrega_prevista, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (1, "Guarda", "Lisboa", "Planeada", 320.0, datetime.utcnow().date().isoformat(), now),
            )


def layout(title: str, content: str, msg: str = "") -> str:
    flash = f"<p class='msg'>{html.escape(msg)}</p>" if msg else ""
    return f"""<!doctype html>
<html lang='pt'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{html.escape(title)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin:0; background:#f2f5f8; }}
header {{ background:#073763; color:white; padding:1rem 1.5rem; display:flex; justify-content:space-between; }}
nav a {{ color:white; margin-left:1rem; text-decoration:none; }}
main {{ padding:1.2rem; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; }}
.card {{ background:white; border-radius:8px; padding:1rem; }}
form {{ display:grid; grid-template-columns:repeat(3,minmax(150px,1fr)); gap:.6rem; margin-bottom:1rem; }}
input,select,button {{ padding:.55rem; border:1px solid #ccd; border-radius:6px; }}
button {{ background:#0b5394; color:white; border:none; }}
table {{ width:100%; border-collapse:collapse; background:white; }}
th,td {{ padding:.55rem; border-bottom:1px solid #ddd; text-align:left; }}
.msg {{ background:#fff3cd; border:1px solid #ffeeba; padding:.5rem; }}
</style>
</head>
<body>
<header><h2>LUSOGUARDA Logística</h2>
<nav><a href='/'>Dashboard</a><a href='/clientes'>Clientes</a><a href='/ordens'>Ordens</a></nav></header>
<main>{flash}{content}</main></body></html>"""


def redirect(start_response, location: str):
    start_response("303 See Other", [("Location", location)])
    return [b""]


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query = parse_qs(environ.get("QUERY_STRING", ""))
    msg = query.get("msg", [""])[0]

    if method == "POST":
        size = int(environ.get("CONTENT_LENGTH") or 0)
        raw = environ["wsgi.input"].read(size).decode("utf-8")
        form = {k: v[0] for k, v in parse_qs(raw).items()}
    else:
        form = {}

    if path == "/":
        with get_db() as conn:
            total_clientes = conn.execute("SELECT COUNT(*) c FROM clientes").fetchone()["c"]
            total_ordens = conn.execute("SELECT COUNT(*) c FROM ordens_transporte").fetchone()["c"]
            pendentes = conn.execute("SELECT COUNT(*) c FROM ordens_transporte WHERE status!='Entregue'").fetchone()["c"]
            receita = conn.execute("SELECT COALESCE(SUM(valor),0) t FROM ordens_transporte").fetchone()["t"]
            ordens = conn.execute(
                "SELECT o.id, c.nome cliente, o.origem, o.destino, o.status, o.valor FROM ordens_transporte o JOIN clientes c ON c.id=o.cliente_id ORDER BY o.id DESC LIMIT 8"
            ).fetchall()
        rows = "".join(
            f"<tr><td>{o['id']}</td><td>{html.escape(o['cliente'])}</td><td>{html.escape(o['origem'])}</td><td>{html.escape(o['destino'])}</td><td>{html.escape(o['status'])}</td><td>€ {o['valor']:.2f}</td></tr>"
            for o in ordens
        )
        content = f"""
<div class='grid'>
  <div class='card'><h3>Clientes</h3><p>{total_clientes}</p></div>
  <div class='card'><h3>Ordens</h3><p>{total_ordens}</p></div>
  <div class='card'><h3>Pendentes</h3><p>{pendentes}</p></div>
  <div class='card'><h3>Receita</h3><p>€ {receita:.2f}</p></div>
</div>
<h3>Últimas Ordens</h3>
<table><thead><tr><th>ID</th><th>Cliente</th><th>Origem</th><th>Destino</th><th>Status</th><th>Valor</th></tr></thead><tbody>{rows}</tbody></table>
"""
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [layout("Dashboard", content, msg).encode("utf-8")]

    if path == "/clientes":
        if method == "POST":
            nome = form.get("nome", "").strip()
            if not nome:
                return redirect(start_response, "/clientes?msg=Nome+obrigatorio")
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO clientes (nome,nif,cidade,contato,created_at) VALUES (?,?,?,?,?)",
                    (
                        nome,
                        form.get("nif", "").strip(),
                        form.get("cidade", "").strip(),
                        form.get("contato", "").strip(),
                        datetime.utcnow().isoformat(),
                    ),
                )
            return redirect(start_response, "/clientes?msg=Cliente+criado")

        with get_db() as conn:
            clientes = conn.execute("SELECT * FROM clientes ORDER BY id DESC").fetchall()
        rows = "".join(
            f"<tr><td>{c['id']}</td><td>{html.escape(c['nome'])}</td><td>{html.escape(c['nif'] or '')}</td><td>{html.escape(c['cidade'] or '')}</td><td>{html.escape(c['contato'] or '')}</td></tr>"
            for c in clientes
        )
        content = f"""
<h3>Cadastro de Clientes</h3>
<form method='post'>
<input name='nome' placeholder='Nome' required>
<input name='nif' placeholder='NIF'>
<input name='cidade' placeholder='Cidade'>
<input name='contato' placeholder='Email/Telefone'>
<button type='submit'>Criar Cliente</button>
</form>
<table><thead><tr><th>ID</th><th>Nome</th><th>NIF</th><th>Cidade</th><th>Contato</th></tr></thead><tbody>{rows}</tbody></table>
"""
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [layout("Clientes", content, msg).encode("utf-8")]

    if path == "/ordens":
        if method == "POST":
            required = [form.get("cliente_id", ""), form.get("origem", ""), form.get("destino", ""), form.get("status", "")]
            if not all(x.strip() for x in required):
                return redirect(start_response, "/ordens?msg=Campos+obrigatorios+em+falta")
            try:
                valor = float(form.get("valor", "0") or "0")
            except ValueError:
                return redirect(start_response, "/ordens?msg=Valor+invalido")
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO ordens_transporte (cliente_id,origem,destino,status,valor,data_entrega_prevista,created_at) VALUES (?,?,?,?,?,?,?)",
                    (
                        int(form.get("cliente_id")),
                        form.get("origem", "").strip(),
                        form.get("destino", "").strip(),
                        form.get("status", "").strip(),
                        valor,
                        form.get("data_entrega_prevista", "").strip() or None,
                        datetime.utcnow().isoformat(),
                    ),
                )
            return redirect(start_response, "/ordens?msg=Ordem+criada")

        with get_db() as conn:
            clientes = conn.execute("SELECT id,nome FROM clientes ORDER BY nome").fetchall()
            ordens = conn.execute(
                "SELECT o.*, c.nome cliente FROM ordens_transporte o JOIN clientes c ON c.id=o.cliente_id ORDER BY o.id DESC"
            ).fetchall()

        opts = "".join([f"<option value='{c['id']}'>{html.escape(c['nome'])}</option>" for c in clientes])
        rows = "".join(
            f"<tr><td>{o['id']}</td><td>{html.escape(o['cliente'])}</td><td>{html.escape(o['origem'])}</td><td>{html.escape(o['destino'])}</td><td>{html.escape(o['status'])}</td><td>€ {o['valor']:.2f}</td><td>{html.escape(o['data_entrega_prevista'] or '-')}</td></tr>"
            for o in ordens
        )
        content = f"""
<h3>Ordens de Transporte</h3>
<form method='post'>
<select name='cliente_id' required><option value=''>Cliente</option>{opts}</select>
<input name='origem' placeholder='Origem' required>
<input name='destino' placeholder='Destino' required>
<select name='status' required><option>Planeada</option><option>Em trânsito</option><option>Entregue</option></select>
<input name='valor' type='number' step='0.01' placeholder='Valor (€)'>
<input name='data_entrega_prevista' type='date'>
<button type='submit'>Criar Ordem</button>
</form>
<table><thead><tr><th>ID</th><th>Cliente</th><th>Origem</th><th>Destino</th><th>Status</th><th>Valor</th><th>Previsão</th></tr></thead><tbody>{rows}</tbody></table>
"""
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [layout("Ordens", content, msg).encode("utf-8")]

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Not found"]


if __name__ == "__main__":
    init_db()
    print("Servidor em http://localhost:5000")
    with make_server("0.0.0.0", 5000, app) as httpd:
        httpd.serve_forever()
