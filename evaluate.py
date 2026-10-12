from retriever import retrieve_from_db
from tests.evaluation_questions import evaluation_questions

total_questions = len(evaluation_questions)

hits_at_1 = 0
hits_at_3 = 0
reciprocal_rank_sum = 0


for index, item in enumerate(evaluation_questions, start=1):

    question = item["question"]

    results = retrieve_from_db(
        query=question,
        top_k=3,
    )

    expected_filename = item["expected_filename"]
    expected_page = item["expected_page"]

    # Find the rank of the expected source
    found_rank = None

    for rank, result in enumerate(results, start=1):

        if result["filename"] == expected_filename and result["page"] == expected_page:
            found_rank = rank
            break

    # Calculate metrics
    if found_rank == 1:
        hits_at_1 += 1

    if found_rank is not None:
        hits_at_3 += 1
        reciprocal_rank_sum += 1 / found_rank

    print("\n" + "=" * 60)
    print(f"Question {index}: {question}")
    print(f"Expected: {expected_filename} - Page {expected_page}")
    print(f"Result: {'PASS' if found_rank else 'FAIL'}")
    print(f"Found Rank: {found_rank}")

    for rank, result in enumerate(results, start=1):
        print(
            f"  Rank {rank}: "
            f"{result['filename']} | "
            f"Page {result['page']} | "
            f"Score {result['score']:.4f}"
        )


# Final metrics
hit_rate_1 = hits_at_1 / total_questions if total_questions else 0
hit_rate_3 = hits_at_3 / total_questions if total_questions else 0
mrr_at_3 = reciprocal_rank_sum / total_questions if total_questions else 0


print("\n" + "=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)

print("Total Questions:", total_questions)
print(f"Hit Rate @1: {hit_rate_1:.2%}")
print(f"Hit Rate @3: {hit_rate_3:.2%}")
print(f"MRR @3: {mrr_at_3:.4f}")
