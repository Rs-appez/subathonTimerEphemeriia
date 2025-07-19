def is_streamer(user):
    """
    Check if the user is a streamer.
    """
    streamers = ["appez", "ephemeriia"]
    return user.is_authenticated and user.username in streamers
