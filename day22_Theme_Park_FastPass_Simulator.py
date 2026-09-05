"""Day 22: Theme Park FastPass Simulator.

Visitors are served from the VIP lane first. Visitors in the same lane keep
their arrival order, so the scheduler is fair within each priority level.
"""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Visitor:
	"""A visitor waiting for a ride."""

	name: str
	vip: bool = False


class ThemeParkQueue:
	"""Schedule normal visitors and VIP visitors using FIFO lanes."""

	def __init__(self) -> None:
		self._normal: deque[Visitor] = deque()
		self._vip: deque[Visitor] = deque()
		self._history: list[str] = []

	def enqueue(self, name: str, vip: bool = False) -> Visitor:
		"""Add a visitor to the back of the appropriate priority lane."""
		if not name.strip():
			raise ValueError("visitor name cannot be empty")

		visitor = Visitor(name=name, vip=vip)
		lane = self._vip if vip else self._normal
		lane.append(visitor)
		self._history.append(f"JOIN  {'VIP' if vip else 'NORMAL':6} {name}")
		return visitor

	def process_next(self) -> Visitor | None:
		"""Serve the next visitor, preferring VIP while preserving FIFO order."""
		if self._vip:
			visitor = self._vip.popleft()
		elif self._normal:
			visitor = self._normal.popleft()
		else:
			self._history.append("SERVE queue empty")
			return None

		self._history.append(
			f"SERVE {'VIP' if visitor.vip else 'NORMAL':6} {visitor.name}"
		)
		return visitor

	def process_all(self) -> list[Visitor]:
		"""Serve every visitor and return them in service order."""
		served = []
		visitor = self.process_next()
		while visitor is not None:
			served.append(visitor)
			visitor = self.process_next()
		return served

	def snapshot(self) -> dict[str, list[str]]:
		"""Return the current lanes without exposing mutable queue objects."""
		return {
			"vip": [visitor.name for visitor in self._vip],
			"normal": [visitor.name for visitor in self._normal],
		}

	def visualize(self) -> str:
		"""Return the queue's operation history as a readable timeline."""
		if not self._history:
			return "No queue operations yet."

		lines = ["Queue operation timeline:"]
		lines.extend(f"{step}. {operation}" for step, operation in enumerate(self._history, 1))
		return "\n".join(lines)


def run_demo() -> None:
	"""Run a small example showing priority and FIFO behavior."""
	queue = ThemeParkQueue()
	queue.enqueue("Maya")
	queue.enqueue("Leo", vip=True)
	queue.enqueue("Ari")
	queue.enqueue("Zoe", vip=True)

	print("Waiting queues:", queue.snapshot())
	print("Service order:", [visitor.name for visitor in queue.process_all()])
	print(queue.visualize())


if __name__ == "__main__":
	run_demo()
