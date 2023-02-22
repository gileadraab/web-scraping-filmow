from database import Rating


def format_rating_info(comment_info, movie):
    rating = Rating(
        user_id=comment_info.user_id,
        movie_id=movie.id,
        rating=comment_info.rating,
    )
    return rating
