import pyarrow as pa

columns_def = """
    id VARCHAR PRIMARY KEY,
    type VARCHAR,
    actor STRUCT(
        id VARCHAR,
        login VARCHAR,
        display_login VARCHAR,
        gravatar_id VARCHAR,
        url VARCHAR,
        avatar_url VARCHAR
    ),
    repo STRUCT(id VARCHAR, name VARCHAR, url VARCHAR),
    payload JSON,
    public BOOLEAN,
    created_at TIMESTAMP,
    org STRUCT(
        id VARCHAR,
        login VARCHAR,
        gravatar_id VARCHAR,
        url VARCHAR,
        avatar_url VARCHAR
    ),
    event_at_year INTEGER,
    event_at_month INTEGER
"""

columns_list = """
    id,
    type,
    actor,
    repo,
    payload,
    public,
    created_at,
    org
"""

columns = """
    {
        'id': 'VARCHAR',
        'type': 'VARCHAR',
        'actor': 'STRUCT(
            id VARCHAR,
            login VARCHAR,
            display_login VARCHAR,
            gravatar_id VARCHAR,
            url VARCHAR,
            avatar_url VARCHAR
        )',
        'repo': 'STRUCT(id VARCHAR, name VARCHAR, url VARCHAR)',
        'payload': 'JSON',
        'public': 'BOOLEAN',
        'created_at': 'TIMESTAMP',
        'org': 'STRUCT(
            id VARCHAR,
            login VARCHAR,
            gravatar_id VARCHAR,
            url VARCHAR,
            avatar_url VARCHAR
        )'
    }
"""

pa_schema = [
    ("id", pa.string()),
    ("type", pa.string()),
    (
        "actor",
        pa.struct(
            [
                ("id", pa.int64()),
                ("login", pa.string()),
                ("display_login", pa.string()),
                ("gravatar_id", pa.string()),
                ("url", pa.string()),
                ("avatar_url", pa.string()),
            ]
        ),
    ),
    (
        "repo",
        pa.struct([("id", pa.int64()), ("name", pa.string()), ("url", pa.string())]),
    ),
    ("payload", pa.string()),
    ("public", pa.bool_()),
    ("created_at", pa.timestamp("s")),
    (
        "org",
        pa.struct(
            [
                ("id", pa.string()),
                ("login", pa.string()),
                ("gravatar_id", pa.string()),
                ("url", pa.string()),
                ("avatar_url", pa.string()),
            ]
        ),
    ),
]
