from sqlalchemy.orm import Session

from models import Post

def insert_post(new_post: Post, db: Session):
    post=Post(
        title=new_post.title,
        content=new_post.content
	)
    db.add(post)
    db.commit()
    
    return post.title

def read_post(db: Session):
    post=db.query(Post).all()

    return post