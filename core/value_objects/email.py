class Email:
    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)
