import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5433,
        dbname="knowledge-assistant-db",
        user="user",
        password="password",
    )


def insert_chunks(chunks: list[dict]):
    with get_connection() as conn:
        with conn.cursor() as cursor:

            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO chunks (
                        filename,
                        page,
                        chunk_index,
                        text,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s)

                    ON CONFLICT (filename, page, chunk_index)
                    DO NOTHING
                    """,
                    (
                        chunk["filename"],
                        chunk["page"],
                        chunk["chunk_index"],
                        chunk["text"],
                        chunk["embedding"].tolist(),
                    ),
                )

        conn.commit()
