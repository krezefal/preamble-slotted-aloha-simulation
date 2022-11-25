class DataPacket:
    def __init__(self, entry_slot) -> None:
        self.entry = entry_slot
        self.exit = None

    def processed(self, exit_slot):
        self.exit = exit_slot

    def get_processing_time(self) -> float:
        return self.exit - self.entry
