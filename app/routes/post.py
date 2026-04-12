from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from ..database import get_db
from ..schemas import UserOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .options(joinedload(models.Post.owner))
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    # Extract post IDs from the fetched posts
    post_ids = [p.id for p in posts]

    if not post_ids:
        return []

    # Count votes for the retrieved posts only
    votes_rows = (
        db.query(models.Vote.post_id, func.count(models.Vote.post_id))
        .filter(models.Vote.post_id.in_(post_ids))
        .group_by(models.Vote.post_id)
        .all()
    )
    # Convert vote results into a dictionary
    votes_map = {pid: count for pid, count in votes_rows}

    return [{"post": p, "votes": votes_map.get(p.id, 0)} for p in posts]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2.get_current_user),
):
    # # Prevents SQL injection via sanitation
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()

    # # Commits to db
    # conn.commit()

    # Dynamic way by converting to dict and unpacking
    new_post = models.Post(user_id=current_user.id, **post.model_dump())

    # Add new post to db
    db.add(new_post)
    db.commit()
    # Return the newly created post
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2.get_current_user),
):
    # For some reason will crash if id is above 9 without comma after id
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = (
        db.query(models.Post)
        .options(joinedload(models.Post.owner))
        .filter(models.Post.id == id)
        .first()
    )

    votes = (
        db.query(func.count(models.Vote.post_id))
        .filter(models.Vote.post_id == id)
        .scalar()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    return {"post": post, "votes": votes or 0}


# Updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2.get_current_user),
):

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published =  %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_posts = cursor.fetchall()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    if updated_post.user_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action.",
        )

    # Typing error but still runs
    post_query.update(post.model_dump(), synchronize_session=False)  # type: ignore

    db.commit()

    updated_post = post_query.first()

    return updated_post


# Deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2.get_current_user),
):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    if post.user_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
