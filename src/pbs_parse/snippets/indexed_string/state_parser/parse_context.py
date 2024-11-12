class ParseContext:
    def __init__(self, beginning_state: str = "start") -> None:
        self.current_state = beginning_state
