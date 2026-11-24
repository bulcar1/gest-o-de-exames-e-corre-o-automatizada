import sqlite3
import os
DB_PATH = "database/database.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS questoes (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    texto             TEXT NOT NULL,
    tipo              TEXT NOT NULL
                      CHECK (tipo IN ('escolha_multipla', 'verdadeiro_falso', 'resposta_curta', 'desenvolvimento')),
    opcoes_json       TEXT,
    resposta_correta  TEXT,
    dificuldade       TEXT
                      CHECK (dificuldade IN ('facil', 'media', 'dificil')),
    disciplina        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exames (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo            TEXT NOT NULL,
    data_hora_inicio  TEXT NOT NULL,
    duracao_minutos   INTEGER NOT NULL CHECK (duracao_minutos > 0),
    criado_por        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exame_questoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    exame_id    INTEGER NOT NULL,
    questao_id  INTEGER NOT NULL,
    pontuacao   REAL NOT NULL DEFAULT 1 CHECK (pontuacao >= 0),
    ordem       INTEGER NOT NULL,
    FOREIGN KEY (exame_id)   REFERENCES exames(id)   ON DELETE CASCADE,
    FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE RESTRICT,
    UNIQUE (exame_id, questao_id),
    UNIQUE (exame_id, ordem)
);

CREATE TABLE IF NOT EXISTS alunos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_aluno  TEXT NOT NULL UNIQUE,
    nome          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    turma         TEXT
);

CREATE TABLE IF NOT EXISTS submissoes_exame (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    exame_id         INTEGER NOT NULL,
    aluno_id         INTEGER NOT NULL,
    data_submissao   TEXT,
    pontuacao_total  REAL DEFAULT 0,
    estado           TEXT NOT NULL DEFAULT 'em_curso'
                     CHECK (estado IN ('em_curso', 'submetido', 'corrigido')),
    FOREIGN KEY (exame_id) REFERENCES exames(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
    UNIQUE (exame_id, aluno_id)
);

CREATE TABLE IF NOT EXISTS respostas (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    submissao_id         INTEGER NOT NULL,
    questao_id           INTEGER NOT NULL,
    resposta_dada        TEXT,
    pontuacao_atribuida  REAL DEFAULT 0,
    FOREIGN KEY (submissao_id) REFERENCES submissoes_exame(id) ON DELETE CASCADE,
    FOREIGN KEY (questao_id)   REFERENCES questoes(id) ON DELETE RESTRICT,
    UNIQUE (submissao_id, questao_id)
);

CREATE TABLE IF NOT EXISTS utilizadores (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    role           TEXT NOT NULL
                   CHECK (role IN ('operador', 'admin'))
);
"""


def get_connection():
    """Devolve uma ligação à base de dados com chaves estrangeiras ativas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso em", DB_PATH)