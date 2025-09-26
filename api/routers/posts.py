from fastapi import APIRouter, HTTPException

from api.models.post import Post
from api.setup.dependencies import CurrentUserDep, PostsRepositoryDep

router = APIRouter()


@router.get("", response_model=list[Post], tags=["posts"])
async def list_posts(posts_repository: PostsRepositoryDep) -> list[Post]:
    posts = await posts_repository.all_posts()
    return list(posts)


@router.get("/{post_id}", response_model=Post, tags=["posts"])
async def find_post(post_id: int, posts_repository: PostsRepositoryDep) -> Post:
    post = await posts_repository.find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("", response_model=Post, status_code=201, tags=["posts"])
async def create_post(post: Post, posts_repository: PostsRepositoryDep, user: CurrentUserDep) -> Post:
    post.user_id = user.id
    return await posts_repository.create_post(post)


@router.put("/{post_id}", response_model=Post, tags=["posts"])
async def update_post(post_id: int, post: Post, posts_repository: PostsRepositoryDep, _user: CurrentUserDep) -> Post:
    updated_post = await posts_repository.update_post(post_id, post)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.delete("/{post_id}", status_code=204, tags=["posts"])
async def delete_post(post_id: int, posts_repository: PostsRepositoryDep, _user: CurrentUserDep):
    success = await posts_repository.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
