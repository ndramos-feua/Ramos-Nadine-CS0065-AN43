"""Bonus: Three rooms, random dirty-room choices, and a text grid."""

import random

from TA2_RAMOS import clean_room, is_dirty, read_state, read_steps


class BonusAgent:
    def __init__(self, rooms):
        self.rooms = rooms
        self.location = "A"

    def move(self, room):
        self.location = room

    def perceive_and_act(self):
        # Clean first if the room under the agent is dirty.
        if is_dirty(self.rooms, self.location):
            clean_room(self.rooms, self.location)
            return f"Cleaned room {self.location}."

        # Pick a dirty room at random when this room is clean.
        dirty_rooms = [room for room in self.rooms
                       if is_dirty(self.rooms, room)]
        if dirty_rooms:
            self.move(random.choice(dirty_rooms))
            return f"Moved to room {self.location}."
        return "All rooms are clean. Agent is idle."

    def show_grid(self):
        cells = []
        for room, state in self.rooms.items():
            label = f"{room}: {state}"
            if room == self.location:
                label += " (Agent)"
            cells.append(f"[{label}]")
        print(" ".join(cells))


def main():
    print("Bonus Vacuum Cleaner: Rooms A, B, and C")
    rooms = {room: read_state(room) for room in ("A", "B", "C")}
    steps = read_steps()
    agent = BonusAgent(rooms)
    print("\nInitial grid:")
    agent.show_grid()

    for step in range(1, steps + 1):
        print(f"\nStep {step}: Started in room {agent.location}")
        action = agent.perceive_and_act()
        print(f"Action: {action}")
        print(f"Current location: {agent.location}")
        agent.show_grid()

    print(f"\nFinal state: {rooms}")


if __name__ == "__main__":
    main()
