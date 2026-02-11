def get_sprints(client, board_id, state="active,closed"):
    """Fetch all sprints for a board."""
    return client.get_agile(f"board/{board_id}/sprint", params={"state": state})

def get_sprint_by_name(client, board_id, sprint_name):
    """Find a sprint by its name."""
    sprints = get_sprints(client, board_id).get("values", [])
    for s in sprints:
        if s["name"].lower() == sprint_name.lower():
            return s
    return None

def get_active_sprint(client, board_id):
    """Get the currently active sprint."""
    sprints = get_sprints(client, board_id, state="active").get("values", [])
    return sprints[0] if sprints else None
