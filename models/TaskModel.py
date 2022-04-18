import uuid
from . import SdamGiaResponse
from interactions import Member


class TaskModel(SdamGiaResponse.SdamGiaResponse):
    def __init__(self, responseDict: dict, member: Member):
        super().__init__(responseDict)
        self.member = member
        self.uuid = str(uuid.uuid4())
        self.solved = False
        self.triesCount = 0
        self.result = None

    def solve(self):
        self.solved = True
        if self.triesCount <= 10:
            self.result = 11 - self.triesCount
        else:
            self.result = 0

    def tryToSolve(self, answer: str):
        self.triesCount += 1
        if answer.lower() == self.answer.lower():
            self.solve()
            return True
        return False
