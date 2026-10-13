"""CS0065 TA2: A rule-based vacuum cleaner for rooms A and B."""


def read_state(room):
    """Ask again until the user enters dirty or clean."""
    while True:
        state = input(f"Is room {room} Dirty or Clean? ").strip().lower()
        if state in ("dirty", "clean"):
            return state.title()
        print("Please enter dirty or clean.")


def read_steps():
    """Accept a whole number of steps, including zero."""
    while True:
        try:
            steps = int(input("How many steps should the agent run? "))
            if steps >= 0:
                return steps
        except ValueError:
            pass
        print("Please enter a whole number of 0 or more.")


def is_dirty(rooms, room):
    return rooms[room] == "Dirty"


def clean_room(rooms, room):
    rooms[room] = "Clean"


class VacuumAgent:
    def __init__(self, rooms):
        self.rooms = rooms
        self.location = "A"

    def move(self):
        # Switch from A to B, or from B to A.
        self.location = "B" if self.location == "A" else "A"

    def perceive_and_act(self):
        # Rule 1: Clean the current room if it is dirty.
        if is_dirty(self.rooms, self.location):
            clean_room(self.rooms, self.location)
            return f"Cleaned room {self.location}."
        # Rule 2: Move to the other room if this room is clean.
        self.move()
        return f"Moved to room {self.location}."


def main():
    print("Rule-Based Vacuum Cleaner: Rooms A and B")
    rooms = {room: read_state(room) for room in ("A", "B")}
    steps = read_steps()
    agent = VacuumAgent(rooms)
    print(f"\nInitial state: {rooms}")

    for step in range(1, steps + 1):
        print(f"\nStep {step}: Started in room {agent.location}")
        action = agent.perceive_and_act()
        print(f"Action: {action}")
        print(f"Current location: {agent.location}")
        print(f"Environment: {rooms}")

    print(f"\nFinal state: {rooms}")


if __name__ == "__main__":
    main()
