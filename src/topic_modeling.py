import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# =====================================
# CONFIGURATION
# =====================================

METADATA_FOLDER = "data/metadata"
OUTPUT_FOLDER = "data/final_results"
NUM_TOPICS = 3

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================
# LOAD ABSTRACTS
# =====================================

def load_abstracts(metadata_folder):
    abstracts = []
    paper_names = []

    for file in os.listdir(metadata_folder):
        if file.endswith("_metadata.json"):
            path = os.path.join(metadata_folder, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            abstract = data.get("abstract", "").strip()
            if abstract:
                abstracts.append(abstract)
                paper_names.append(data.get("source_file", file))

    return abstracts, paper_names

# =====================================
# GENAI-STYLE GAP EXPLANATION
# =====================================

def explain_gap(topic_id, keywords, paper_count):
    return (
        f"Topic {topic_id}, characterized by keywords such as "
        f"{', '.join(keywords)}, appears under-explored with only "
        f"{paper_count} paper(s) compared to other topics. "
        f"This suggests a potential research opportunity to further "
        f"investigate challenges, methodologies, and innovations "
        f"within this thematic area."
    )

# =====================================
# MAIN PIPELINE
# =====================================

def main():
    abstracts, paper_names = load_abstracts(METADATA_FOLDER)

    print(f"Loaded {len(abstracts)} abstracts")

    if len(abstracts) < 2:
        print("Not enough data for topic modeling.")
        return

    # ---------------------------------
    # STEP 1: TEXT → NUMBERS
    # ---------------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000
    )

    tfidf_matrix = vectorizer.fit_transform(abstracts)
    print("TF-IDF matrix shape:", tfidf_matrix.shape)

    # ---------------------------------
    # STEP 2: CLUSTERING
    # ---------------------------------

    kmeans = KMeans(
        n_clusters=NUM_TOPICS,
        random_state=42,
        n_init=10
    )

    kmeans.fit(tfidf_matrix)
    labels = kmeans.labels_

    print("\n--- TOPIC ASSIGNMENTS ---")
    for paper, label in zip(paper_names, labels):
        print(f"{paper} → Topic {label}")

    # ---------------------------------
    # STEP 3: TOP WORDS PER TOPIC
    # ---------------------------------

    terms = vectorizer.get_feature_names_out()
    topic_keywords = {}

    print("\n--- TOP WORDS PER TOPIC ---")
    for topic_idx, center in enumerate(kmeans.cluster_centers_):
        top_indices = center.argsort()[-10:][::-1]
        keywords = [terms[i] for i in top_indices]
        topic_keywords[int(topic_idx)] = keywords

        print(f"\nTopic {topic_idx}:")
        for word in keywords:
            print(f"  {word}")

    # ---------------------------------
    # STEP 4: TOPIC DENSITY
    # ---------------------------------

    topic_counts = {}
    for label in labels:
        label = int(label)
        topic_counts[label] = topic_counts.get(label, 0) + 1

    print("\n--- TOPIC DENSITY ---")
    for topic, count in sorted(topic_counts.items()):
        print(f"Topic {topic}: {count} paper(s)")

    # ---------------------------------
    # STEP 5: GAP DETECTION + EXPLANATION
    # ---------------------------------

    min_count = min(topic_counts.values())
    final_results = []

    print("\n--- WORLD-CLASS RESEARCH GAP INSIGHTS ---")

    for topic, count in topic_counts.items():
        if count == min_count:
            explanation = explain_gap(
                topic,
                topic_keywords[topic],
                count
            )

            print("\n" + explanation)

            final_results.append({
                "topic_id": int(topic),
                "paper_count": int(count),
                "keywords": [str(k) for k in topic_keywords[topic]],
                "gap_explanation": explanation
            })

    # ---------------------------------
    # STEP 6: SAVE FINAL REPORT
    # ---------------------------------

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "research_gap_report.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4)

    print(f"\nFINAL REPORT SAVED AT: {output_path}")
    print("\nWORLD-CLASS PIPELINE COMPLETED SUCCESSFULLY")

# =====================================
# ENTRY POINT
# =====================================

if __name__ == "__main__":
    main()
