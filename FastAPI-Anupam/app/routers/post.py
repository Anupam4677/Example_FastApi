from typing import List, Optional
import sys
sys.path.append(".")
# from app import models
import oauth2
import schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models


router =APIRouter(
    prefix="/posts",
    tags =['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
              Limit: int = 13,skip:int=0,search:Optional[str] = ""):  

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # print(f"limit:{Limit}")
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    # cumodels.Post.idrsor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
    #                (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user)
    new_post = models.Post(owner_id =current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print('1')
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()

    # post= db.query(models.Post).filter(models.Post.id == id).first()
    post=  db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested actions")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_del = db.query(models.Post).filter(models.Post.id == id)
    post = post_del.first()
    # print(post.owner_id,current_user.id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested actions")
    
    
    post_del.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s WHERE id = %s RETURNING *""",(post.title,post.content,str(id)))
    # updated_post = cursor.fetchone()
    # print(updated_post)
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested actions")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()