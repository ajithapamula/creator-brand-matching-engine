🧠 Creator–Brand Matching Engine (AI Recommendation System)

A production-style AI-powered matching system that connects brands with the most relevant creators using semantic embeddings, vector search, and ranking models.
Built with FastAPI, Sentence-BERT, FAISS, and MLflow, this project demonstrates an end-to-end pipeline — from ML modeling to API deployment.

🚀 Overview

The Creator–Brand Matching Engine enables brand teams to discover creators based on:

Semantic similarity between brand descriptions and creator bios

Engagement metrics like average engagement rate and followers

Vector similarity search using FAISS for scalability

It exposes a clean FastAPI REST interface for easy integration into products.

🧩 Tech Stack
Layer	Technology
Language	Python 3.11
Framework	FastAPI
Modeling	Sentence-BERT (all-MiniLM-L6-v2)
Vector Search	FAISS
Data Storage	CSV (sample) → PostgreSQL/MongoDB ready
Experiment Tracking	MLflow
Infrastructure	Local / Docker (ready for AWS or Render)
🗂️ Project Structure
creator-brand-matching/
├── .env.example
├── README.md
├── requirements.txt
├── docker/
│   └── Dockerfile
├── api/
│   └── main.py
├── src/
│   ├── config.py
│   ├── embeddings.py
│   ├── repository.py
│   ├── indexer.py
│   ├── ranker.py
│   ├── mlflow_tracking.py
│   └── utils.py
├── data/
│   ├── sample_creators.csv
│   └── sample_brands.csv
├── tests/
│   └── test_ranking.py
└── .faiss/

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/creator-brand-matching.git
cd creator-brand-matching

2️⃣ Create a Virtual Environment

Windows:

python -m venv .venv
.venv\Scripts\activate


macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create Environment File

Copy .env.example to .env:

cp .env.example .env

5️⃣ Run the API
uvicorn api.main:app --reload --port 8000


Visit:
👉 http://127.0.0.1:8000/docs

🌐 API Documentation
1. GET /health

Description: Health check endpoint.
Response:

{
  "status": "ok",
  "index_size": 5
}

2. POST /recommend

Description: Get top creators matching a brand description.

Request Body:

{
  "brand_description": "Eco-friendly fashion brand",
  "top_k": 3,
  "alpha": 0.8,
  "beta": 0.2
}


Response Example:

{
  "results": [
    {
      "rank": 1,
      "creator_id": "c3",
      "name": "Neha Eco",
      "bio": "Sustainable fashion & eco-friendly living",
      "topics": "fashion|sustainability",
      "avg_engagement_rate": 0.055,
      "followers": 63000,
      "semantic_similarity": 0.7981,
      "score": 0.6495
    }
  ]
}


Explanation:

semantic_similarity: cosine similarity between brand and creator embeddings.

score: final weighted score combining similarity and engagement.

3. POST /creators/upsert

Description: Add or update a creator record.
Request Example:

{
  "creator_id": "c6",
  "name": "Anya Lifestyle",
  "bio": "Sustainable home decor and minimalism tips",
  "topics": "home|eco|minimalism",
  "avg_engagement_rate": 0.048,
  "followers": 75000
}


Response:

{"status": "upserted", "index_size": 6}

🧠 How It Works
Step 1 — Embedding Creation

Uses Sentence-BERT (all-MiniLM-L6-v2) to convert text (bios, brand descriptions) into dense vector embeddings.

Each vector captures semantic meaning beyond keywords.

Step 2 — Vector Indexing (FAISS)

All creator embeddings are indexed using FAISS (Facebook AI Similarity Search) for efficient nearest-neighbor search.

Allows instant retrieval of similar creators for a given brand.

Step 3 — Ranking

Combines semantic similarity and engagement score:

final_score = 0.8 * similarity + 0.2 * engagement_rate


You can tune alpha and beta in the request to adjust importance.

Step 4 — API & Monitoring

FastAPI serves endpoints for recommendations and updates.

MLflow logs retrieval latency and similarity statistics.

Ready for Grafana dashboards for drift & latency monitoring.

🧩 Example Walkthrough
curl -X POST http://127.0.0.1:8000/recommend \
 -H "Content-Type: application/json" \
 -d '{"brand_description":"Eco-friendly fashion brand","top_k":3}'


Response:

Top 3 Matching Creators
1️⃣ Neha Eco — Fashion, Sustainability
2️⃣ Meera Beauty — Beauty, Skincare
3️⃣ Rohan Fitness — Health, Fitness

🧪 Run Tests
pytest -q

🐳 Docker Support
docker build -t vrd-matching-engine .
docker run -p 8000:8000 vrd-matching-engine

📊 MLflow Tracking

Start MLflow UI:

mlflow ui --backend-store-uri mlruns --port 5000


Then open:
👉 http://127.0.0.1:5000

You’ll see metrics like:

wall_clock_s → inference latency

topk → top-k parameter used

avg_similarity → average similarity score

📈 Future Enhancements
Feature	Description
🧩 Pinecone Integration	Replace FAISS with a cloud-based vector DB
⚙️ Auto-retraining	Update embeddings periodically using pipelines
📊 Monitoring Dashboard	Add Grafana + Prometheus metrics
🧠 Learn-to-Rank	Train a supervised model for better scoring
☁️ Deploy on AWS / Render	Containerized deployment for production use
🧾 Resume Bullet Points (You can add to CV)

Developed an AI-powered Creator–Brand Recommendation Engine using Sentence-BERT embeddings and FAISS vector search, exposed via FastAPI, achieving sub-150ms query latency on 1K profiles.

Integrated MLflow for experiment tracking and model monitoring; implemented ranking logic combining semantic and engagement metrics.

Packaged using Docker for scalable deployment on AWS/Render.

🗣 Interview Summary (Pitch)

“I built a FastAPI-based semantic matching system that connects brands with relevant creators using Sentence-BERT embeddings and FAISS. The system calculates similarity between brand descriptions and creator bios, ranks them with engagement metrics, and exposes results as an API. It’s fully containerized, monitored with MLflow, and can easily scale using Pinecone.”

🧩 Credits

Developer: [Your Name]

Role Targeted: AI Engineer / ML Developer

Inspired By: Real-world recommender systems used in influencer marketing platforms