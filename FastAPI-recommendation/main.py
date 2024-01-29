from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import FastAPIVote, FastAPIProduct
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]


SQLALCHEMY_DATABASE_URL = "postgresql://maciej:maciej@database:5432/DiceAndTiles"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_item_co_occurrence(item_id: int, db: Session):
    # Fetch upvotes for the given item
    upvotes = (
        db.query(FastAPIVote)
        .filter(FastAPIVote.product_id == item_id, FastAPIVote.value == 2)
        .all()
    )

    # Calculate item co-occurrence
    co_occurrence_counts = {}
    for upvote in upvotes:
        # Fetch other items upvoted by the same user
        other_upvotes = (
            db.query(FastAPIVote)
            .filter(
                FastAPIVote.owner_id == upvote.owner_id,
                FastAPIVote.product_id != item_id,
                FastAPIVote.value == 2,
            )
            .all()
        )

        # Update co-occurrence counts based on user upvotes
        for other_upvote in other_upvotes:
            if other_upvote.product_id not in co_occurrence_counts:
                co_occurrence_counts[other_upvote.product_id] = 0
            co_occurrence_counts[other_upvote.product_id] += 1

    return co_occurrence_counts

# fetch recommendations for item
@app.get("/recommend/{item_id}")
async def get_item_co_occurrence(item_id: int, db: Session = Depends(get_db)):
    co_occurrence_counts = calculate_item_co_occurrence(item_id, db)

    # Sort items based on co-occurrence counts (descending order)
    sorted_items = sorted(
        co_occurrence_counts.items(), key=lambda x: x[1], reverse=True
    )

    # Get top N recommended items (adjust N as needed)
    # top_recommendations = [item[0] for item in sorted_items[:5]]

    # return {"item_id": item_id, "co_occurrence_recommendations": top_recommendations}
    top_recommendations = []
    for recommended_product_id, co_occurrence_count in sorted_items[:5]:
        # Fetch detailed information about the recommended product
        recommended_product = (
            db.query(FastAPIProduct)
            .filter(FastAPIProduct.id == recommended_product_id)
            .first()
        )

        if recommended_product:
            # Include relevant information in the recommendation
            recommendation_info = {
                "product_id": recommended_product_id,
                "product_name": recommended_product.name,
                "product_thumbnail":recommended_product.thumbnail,
                "product_slug":recommended_product.slug
                # Add more details as needed
            }
            top_recommendations.append(recommendation_info)

    return {"item_id": item_id, "co_occurrence_recommendations": top_recommendations}