from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text1 = "I love programming"
text2 = "I enjoy writing code"
text3 = "The weather is very hot today"

embedding1 = model.encode(text1)
embedding2 = model.encode(text2)
embedding3 = model.encode(text3)

# print("Text:", text)
# print("\nEmbedding:")
# print(embedding1, embedding2, embedding3)

print("\nDimension:", len(embedding1))
print("\nDimension:", len(embedding2))
print("\nDimension:", len(embedding3))
