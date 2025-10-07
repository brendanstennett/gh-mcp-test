from fastapi import APIRouter, HTTPException

from api.models.comment import Comment
from api.setup.dependencies import CommentsRepositoryDep, CurrentUserDep

router = APIRouter()


@router.get("", response_model=list[Comment], tags=["comments"])
async def list_comments(comments_repository: CommentsRepositoryDep) -> list[Comment]:
    comments = await comments_repository.all_comments()
    return list(comments)


@router.get("/{comment_id}", response_model=Comment, tags=["comments"])
async def find_comment(comment_id: int, comments_repository: CommentsRepositoryDep) -> Comment:
    comment = await comments_repository.find_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("", response_model=Comment, status_code=201, tags=["comments"])
async def create_comment(comment: Comment, comments_repository: CommentsRepositoryDep, user: CurrentUserDep) -> Comment:
    comment.user_id = user.id
    return await comments_repository.create_comment(comment)


@router.put("/{comment_id}", response_model=Comment, tags=["comments"])
async def update_comment(
    comment_id: int, comment: Comment, comments_repository: CommentsRepositoryDep, _user: CurrentUserDep
) -> Comment:
    updated_comment = await comments_repository.update_comment(comment_id, comment)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/{comment_id}", status_code=204, tags=["comments"])
async def delete_comment(comment_id: int, comments_repository: CommentsRepositoryDep, _user: CurrentUserDep):
    success = await comments_repository.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
