from database import User


def format_user_info(comment_info):
    user = User(
        id=comment_info.user_id, name=comment_info.name, username=comment_info.username
    )
    return user
