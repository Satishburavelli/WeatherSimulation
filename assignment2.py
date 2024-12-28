import numpy as np

class WeatherSimulation:
    def __init__(self, transition_probabilities, holding_times):
        self.transition_probabilities = transition_probabilities
        self.holding_times = holding_times
        self._present_state = 'sunny'
        self._remaining_hours = self.holding_times[self._present_state]

        for state, transitions in self.transition_probabilities.items():
            if not np.isclose(sum(transitions.values()), 1.0):
                raise RuntimeError(f"The transition probabilities of '{state}' do not sum to 1")

    def get_states(self):
        return list(self.transition_probabilities.keys())

    def current_state(self):
        return self._present_state

    def set_state(self, new_state):
        if new_state not in self.get_states():
            raise ValueError(f"the '{new_state}' which is not valid")
        self._present_state = new_state
        self._remaining_hours = self.holding_times[new_state]

    def current_state_remaining_hours(self):
        return self._remaining_hours

    def next_state(self):
        self._remaining_hours -= 1
        if self._remaining_hours <= 0:
            transitions = self.transition_probabilities[self._present_state]
            states = list(transitions.keys())
            probabilities = list(transitions.values())
            self._present_state = np.random.choice(states, p=probabilities)
            self._remaining_hours = self.holding_times[self._present_state]
        return self._present_state

    def iterable(self):
        while True:
            yield self.current_state()
            self.next_state()

    def simulate(self, hours):
        state_counts = {state: 0 for state in self.get_states()}
        for _ in range(hours):
            state_counts[self.current_state()] += 1
            self.next_state()
        return [round((count / hours) * 100, 4) for count in state_counts.values()]