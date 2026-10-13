# Task 4: Analysis Questions

## 1. What rules does the agent follow?

If the current room is dirty, the agent cleans it. If the current room is clean, the agent moves to the other room.

## 2. How does the agent decide when to clean and when to move?

It checks the current room in the dictionary. A Dirty value means it should clean. A Clean value means it should move. It takes one action per step.

## 3. What happens if both rooms are already clean at the start?

The two-room agent keeps moving between A and B until the chosen number of steps is finished. It does not clean anything because both rooms are clean. The bonus agent stays idle when all rooms are clean.

## 4. How would you modify the agent to handle more than two rooms?

I would add more rooms to the dictionary and change the move method so it can choose from those rooms. In the bonus program, the agent picks a dirty room at random when its current room is clean. It moves there, then cleans it on the next step. The grid shows each room's state and the agent's location.
