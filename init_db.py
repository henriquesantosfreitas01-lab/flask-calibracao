import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "database.db")

# Conecta ao banco (cria se não existir)
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Cria tabela de instrumentos se não existir
c.execute("""
CREATE TABLE IF NOT EXISTS instrumentos (
    tag TEXT PRIMARY KEY,
    modelo TEXT,
    fabricante TEXT,
    ns TEXT,
    local_inst TEXT,
    ordem TEXT
)
""")

# Exemplo de tags de teste
tags_teste = [
    ("MTUM0602", "ModeloX", "FabricanteY", "12345", "Laboratório 1", "001"),
    ("MNMT1522", "ModeloA", "FabricanteB", "67890", "Laboratório 2", "002"),
    ("ABC1234", "ModeloC", "FabricanteD", "54321", "Laboratório 3", "003")
]

# Inserir tags, ignorando duplicadas
for tag, modelo, fabricante, ns, local, ordem in tags_teste:
    c.execute("""
    INSERT OR IGNORE INTO instrumentos (tag, modelo, fabricante, ns, local_inst, ordem)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (tag, modelo, fabricante, ns, local, ordem))

conn.commit()
conn.close()

print("Banco inicializado com sucesso!")
