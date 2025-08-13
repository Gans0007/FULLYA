def get_streak_emoji(streak: int) -> str:
    if streak < 3:
        return ""
    elif streak < 4:
        return "☄️"
    elif streak < 7:
        return "🤘🏻"
    elif streak < 14:
        return "🔥"
    elif streak < 21:
        return "🦅"
    elif streak < 30:
        return "🚀"
    elif streak < 45:
        return "🐉"
    else:
        return "👑"
