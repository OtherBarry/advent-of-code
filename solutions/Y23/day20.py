from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import suppress
from enum import Enum
from itertools import count
from math import lcm
from queue import Queue
from typing import Any

from solutions.base import BaseSolution


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Network:
    def __init__(self) -> None:
        self._modules: dict[str, Module] = {}
        self._pulse_queue: Queue[tuple[Pulse, str, str]] = Queue()
        self._listeners: set[tuple[str, Pulse]] = set()
        self.listen_queue: list[str] = []

    def add_module(self, module: "Module") -> None:
        self._modules[module.name] = module
        module.set_network(self)

    def get_module(self, name: str) -> "Module":
        return self._modules[name]

    def send_pulse(self, pulse: Pulse, source: str, destination: str) -> None:
        self._pulse_queue.put((pulse, source, destination))

    def add_listener(self, source_id: str, pulse: Pulse) -> None:
        self._listeners.add((source_id, pulse))

    def push_button(self) -> tuple[int, int]:
        self._pulse_queue.put((Pulse.LOW, "button", "broadcaster"))
        low_count = 0
        high_count = 0
        while not self._pulse_queue.empty():
            pulse, source, destination = self._pulse_queue.get()
            if (source, pulse) in self._listeners:
                self.listen_queue.append(source)
            with suppress(KeyError):
                self._modules[destination].handle_pulse(pulse, source)
            if pulse == Pulse.LOW:
                low_count += 1
            else:
                high_count += 1
        return low_count, high_count

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Network":
        inputs = defaultdict(list)
        network = cls()
        network.add_module(ReceiverModule("rx", []))
        for line in lines:
            source, destination = line.split(" -> ")
            destinations = destination.split(", ")
            module: Module
            if source[0] == "%":
                module = FlipFlopModule(source[1:], destinations)
            elif source[0] == "&":
                module = ConjunctionModule(source[1:], destinations)
            elif source == "broadcaster":
                module = BroadcastModule(source, destinations)
            else:
                msg = f"Unknown module type: {source}"
                raise ValueError(msg)
            network.add_module(module)
            for destination in destinations:
                inputs[destination].append(module.name)

        for destination, sources in inputs.items():
            with suppress(KeyError):
                module = network.get_module(destination)
                for input_ in sources:
                    module.add_input(input_)
        return network


class Module(ABC):
    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self._outputs = outputs
        self.inputs: list[str] = []
        self._network: Network | None = None

    def set_network(self, network: Network) -> None:
        self._network = network

    def add_input(self, input_: str) -> None:
        self.inputs.append(input_)

    def send_pulse(self, pulse: Pulse, destination: str) -> None:
        if self._network is not None:
            self._network.send_pulse(pulse, self.name, destination)

    @abstractmethod
    def handle_pulse(self, pulse: Pulse, source: str) -> None:
        pass


class FlipFlopModule(Module):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._is_on = False

    def handle_pulse(self, pulse: Pulse, source: str) -> None:  # noqa: ARG002
        if pulse == Pulse.LOW:
            self._is_on = not self._is_on
            next_pulse = Pulse.HIGH if self._is_on else Pulse.LOW
            for connection in self._outputs:
                self.send_pulse(next_pulse, connection)


class ConjunctionModule(Module):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._memory: dict[str, Pulse] = {}

    def memory_is_high(self) -> bool:
        return all(
            self._memory.get(input_, Pulse.LOW) == Pulse.HIGH for input_ in self.inputs
        )

    def handle_pulse(self, pulse: Pulse, source: str) -> None:
        self._memory[source] = pulse
        next_pulse = Pulse.LOW if self.memory_is_high() else Pulse.HIGH
        for connection in self._outputs:
            self.send_pulse(next_pulse, connection)


class BroadcastModule(Module):
    def handle_pulse(self, pulse: Pulse, source: str) -> None:  # noqa: ARG002
        for connection in self._outputs:
            self.send_pulse(pulse, connection)


class ReceiverModule(Module):
    def handle_pulse(self, pulse: Pulse, source: str) -> None:
        pass


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        network = Network.from_lines(self.raw_input.splitlines())
        low_sum = 0
        high_sum = 0
        for _ in range(1000):
            low, high = network.push_button()
            low_sum += low
            high_sum += high
        return low_sum * high_sum

    def part_2(self) -> int:
        network = Network.from_lines(self.raw_input.splitlines())
        dependents = network.get_module(network.get_module("rx").inputs[0]).inputs
        for i in dependents:
            network.add_listener(i, Pulse.HIGH)
        history = {}
        for num_presses in count(1):
            network.push_button()
            for _ in range(len(network.listen_queue)):
                i = network.listen_queue.pop()
                if i not in history:
                    history[i] = num_presses
            if len(history) == len(dependents):
                break
        return lcm(*history.values())
