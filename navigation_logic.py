def decide_next_action(blocked_ahead, blocked_left, blocked_right, goal_reached):
    if goal_reached:
        return "STOP"
    if not blocked_ahead:
        return "FORWARD"
    if not blocked_left:
        return "LEFT"
    if not blocked_right:
        return "RIGHT"
    return "STOP"
