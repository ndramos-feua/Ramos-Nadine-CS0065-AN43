"""CS0065 TA1: random walks, saved paths, and scenario comparisons."""

import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import agentpy as ap
import matplotlib

# Save plots and animations without requiring a desktop window.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class RandomWalker(ap.Agent):
    def setup(self):
        self.path = []

    def step(self):
        # Right mode gives right a 60% chance; other directions get 40%.
        weights = [0.6, 0.1, 0.15, 0.15]
        if self.p.rule == "random":
            weights = [0.25] * 4
        dx, dy = self.model.random.choices(DIRECTIONS, weights=weights)[0]
        x, y = self.model.grid.positions[self]
        limit = self.p.size - 1
        # Clamp each coordinate so an attempted outside move stays inside.
        position = (max(0, min(limit, x + dx)),
                    max(0, min(limit, y + dy)))
        self.model.grid.move_to(self, position)
        self.path.append(position)


class RandomWalkModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)
        self.grid = ap.Grid(self, (self.p.size, self.p.size), torus=False)
        positions = [(self.random.randrange(self.p.size),
                      self.random.randrange(self.p.size))
                     for _ in self.agents]
        # Sharing a cell is allowed, as in the starter movement rule.
        self.grid.add_agents(self.agents, positions=positions)
        for agent in self.agents:
            agent.path.append(self.grid.positions[agent])

    def step(self):
        self.agents.step()


def simulate(count, size, steps, rule="random", seed=65):
    if min(count, size, steps) < 1:
        raise ValueError("Agents, grid size, and steps must be at least 1.")
    if rule not in ("random", "right"):
        raise ValueError("Movement rule must be random or right.")
    params = dict(agents=count, size=size, steps=steps, rule=rule)
    model = RandomWalkModel(params)
    model.run(seed=seed, display=False)
    return model


def save_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def configure_grid(ax, size, title):
    ax.set(xlim=(-0.5, size - 0.5), ylim=(-0.5, size - 0.5),
           xlabel="x", ylabel="y", title=title, aspect="equal")
    ticks = range(0, size, max(1, size // 15))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.grid(alpha=0.25)


def save_outputs(model, name, seed, animate=False):
    folder = ROOT / "outputs" / name
    folder.mkdir(parents=True, exist_ok=True)
    paths = [agent.path for agent in model.agents]
    rows = [(i, t, x, y) for i, path in enumerate(paths, 1)
            for t, (x, y) in enumerate(path)]
    save_csv(folder / "paths.csv", ["agent", "step", "x", "y"], rows)
    final = [(i, *path[0], *path[-1])
             for i, path in enumerate(paths, 1)]
    save_csv(folder / "final_positions.csv",
             ["agent", "start_x", "start_y", "final_x", "final_y"], final)
    occupied = Counter(path[-1] for path in paths)
    visited = set(position for path in paths for position in path)
    distance = [abs(p[-1][0] - p[0][0]) + abs(p[-1][1] - p[0][1])
                for p in paths]
    shift = sum(p[-1][0] - p[0][0] for p in paths) / len(paths)
    summary = dict(name=name, agents=len(paths), size=model.p.size,
                   steps=model.p.steps, rule=model.p.rule, seed=seed,
                   visited_cells=len(visited), final_cells=len(occupied),
                   shared_cells=sum(n > 1 for n in occupied.values()),
                   mean_distance=sum(distance) / len(paths),
                   mean_x_shift=shift, final_positions=final)
    lines = [f"Scenario: {name}",
             f"Agents: {len(paths)} | Grid: {model.p.size} x {model.p.size}",
             f"Steps: {model.p.steps} | Rule: {model.p.rule} | Seed: {seed}",
             "Agent | Start (x, y) | Final (x, y)"]
    lines += [f"{i:5} | ({sx:2}, {sy:2})     | ({x:2}, {y:2})"
              for i, sx, sy, x, y in final]
    lines += [f"Cells visited by all agents: {len(visited)}",
              f"Different final cells: {len(occupied)}",
              f"Final cells shared by agents: {summary['shared_cells']}",
              f"Mean distance from start (grid steps): {summary['mean_distance']:.2f}",
              f"Mean change in x: {shift:.2f}"]
    text = "\n".join(lines)
    (folder / "console.txt").write_text(text + "\n", encoding="utf-8")
    (folder / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(text + "\n")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    colors = [plt.get_cmap("tab20")(i % 20) for i in range(len(paths))]
    for path, color in zip(paths, colors):
        xs, ys = zip(*path)
        axes[0].plot(xs, ys, color=color, alpha=0.8, linewidth=1.3)
        axes[0].scatter(xs[0], ys[0], color=color, marker="x", s=32)
        axes[0].scatter(xs[-1], ys[-1], color=color, s=24)
    for (x, y), number in occupied.items():
        axes[1].scatter(x, y, s=150 + 40 * number, color="#176b87")
        axes[1].text(x, y, str(number), ha="center", va="center",
                     color="white", fontsize=9)
    configure_grid(axes[0], model.p.size, "Paths: x = start, dot = end")
    configure_grid(axes[1], model.p.size, "Final cells: number = agents")
    fig.suptitle(name.replace("_", " ") + f" | {model.p.steps} steps")
    fig.savefig(folder / "plot.png", dpi=180)
    plt.close(fig)

    if animate:
        fig, ax = plt.subplots(figsize=(6, 6), layout="constrained")
        configure_grid(ax, model.p.size, "Recorded agent paths")
        trails = [ax.plot([], [], color=c, linewidth=1)[0] for c in colors]
        dots = [ax.plot([], [], "o", color=c)[0] for c in colors]

        def update(frame):
            # Replay saved paths; drawing a frame never moves an agent.
            for path, line, dot in zip(paths, trails, dots):
                xs, ys = zip(*path[:frame + 1])
                line.set_data(xs, ys)
                dot.set_data([xs[-1]], [ys[-1]])
            ax.set_title(f"{name}: step {frame} of {model.p.steps}")
            return trails + dots

        movie = FuncAnimation(fig, update, frames=model.p.steps + 1,
                              interval=180, blit=False, repeat=False)
        movie.save(folder / "animation.gif", writer=PillowWriter(fps=6))
        plt.close(fig)
    return summary


def positive_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a whole number greater than 0.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true",
                        help="Run the six report scenarios.")
    parser.add_argument("--animate", action="store_true",
                        help="Also save an animated GIF for each run.")
    parser.add_argument("--seed", type=int, default=65)
    args = parser.parse_args()
    if args.demo:
        cases = [("A_baseline", 5, 10, 20, "random"),
                 ("B_more_agents", 20, 10, 20, "random"),
                 ("C_small_grid", 5, 5, 20, "random"),
                 ("D_large_grid", 5, 15, 20, "random"),
                 ("E_more_steps", 5, 10, 50, "random"),
                 ("F_prefer_right", 5, 10, 50, "right")]
    else:
        count = positive_input("Enter number of agents: ")
        size = positive_input("Enter grid size (10 means 10 x 10): ")
        steps = positive_input("Enter number of steps: ")
        rule = input("Movement rule (random/right) [random]: ").strip().lower()
        while rule not in ("", "random", "right"):
            rule = input("Please enter random or right: ").strip().lower()
        cases = [("custom", count, size, steps, rule or "random")]
    summaries = []
    for name, count, size, steps, rule in cases:
        model = simulate(count, size, steps, rule, args.seed)
        summaries.append(save_outputs(model, name, args.seed, args.animate))
    if args.demo:
        destination = ROOT / "outputs" / "comparison.json"
        destination.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print("Saved results in:", ROOT / "outputs")
    print("Open plot.png to view paths and final cells.")
    if args.animate:
        print("Open animation.gif to watch the saved movement.")


if __name__ == "__main__":
    main()
