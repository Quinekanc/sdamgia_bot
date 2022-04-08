from sdamgia import SdamGIA


class ParserSdamGIA():
    def __init__(self, sgia: SdamGIA):
        self.sdamgia = sgia

    def get_problem_dict(self, subject, id):
        answer = self.sdamgia.get_problem_by_id(subject, id)
        ans_dict = {}

        ans_dict['condition'] = answer['condition']
        ans_dict['right_ans'] = answer['answer']
        ans_dict['right_solution'] = answer['solution']

        return ans_dict
