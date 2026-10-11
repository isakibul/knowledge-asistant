from retriever import retrieve_from_db

query = "How many annual leave days do full-time employees get?"

results = retrieve_from_db(
    query=query,
    top_k=3,
)


print("\n" + "=" * 60)
print("QUERY")
print("=" * 60)
print(query)


print("\n" + "=" * 60)
print("TOP 3 RESULTS")
print("=" * 60)


for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"File: {result['filename']}")
    print(f"Page: {result['page']}")
    print(f"Chunk: {result['chunk_index']}")
    print("Text:")
    print(result["text"])
