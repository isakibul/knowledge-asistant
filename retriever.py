from sentence_transformers.util import cos_sim

from embedder import embed_query
from db import get_connection


# Old: Python RAM retrieval
def retrieve(
    query: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:

    query_embedding = embed_query(query)

    results = []

    for chunk in chunks:
        score = cos_sim(
            query_embedding,
            chunk["embedding"],
        ).item()

        results.append(
            {
                "score": score,
                "text": chunk["text"],
                "page": chunk["page"],
                "chunk_index": chunk["chunk_index"],
                "filename": chunk["filename"],
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]


# New: PostgreSQL + pgvector retrieval
def retrieve_from_db(
    query: str,
    top_k: int = 3,
) -> list[dict]:

    query_embedding = embed_query(query)

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    filename,
                    page,
                    chunk_index,
                    text,
                    1 - (embedding <=> %s::vector) AS score
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding.tolist(),
                    query_embedding.tolist(),
                    top_k,
                ),
            )

            rows = cursor.fetchall()

    results = []

    for row in rows:
        results.append(
            {
                "filename": row[0],
                "page": row[1],
                "chunk_index": row[2],
                "text": row[3],
                "score": float(row[4]),
            }
        )

    return results
