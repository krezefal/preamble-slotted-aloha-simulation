class UniqUser:
    def __init__(self, id_, entry_slot: int, slot_len: float):
        self.id_ = id_
        self.entry = entry_slot
        self.slot_len = slot_len

        self.exit = 0


    def processed(self, exit_slot: int):
        self.exit = exit_slot


    def get_processing_time(self) -> float:
        # +1 because user can send only at the end of the frame, so minimal
        # processing time = 1
        return (self.exit - self.entry + 1) * self.slot_len
