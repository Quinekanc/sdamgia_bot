class SdamGiaResponse():
    def __init__(self, responseDict: dict):
        self.rawData = responseDict

        self.id: str = responseDict["id"]
        self.topic: str = responseDict["topic"]
        self.condition: Condition = Condition(responseDict["condition"]['text'],
                                   responseDict["condition"]['images'])
        self.solution: Solution = Solution(responseDict["solution"]['text'],
                                   responseDict["solution"]['images'])
        self.answer: str = responseDict["answer"]
        self.analogs: list = responseDict["analogs"]
        self.url: str = responseDict["url"]

    def __getitem__(self, item):
        return self.rawData[item]


class Condition():
    def __init__(self, text: str, images: list):
        self.text: str = text
        self.images: list = images


class Solution():
    def __init__(self, text: str, images: list):
        self.text: str = text
        self.images: list = images