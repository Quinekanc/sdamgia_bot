from sdamgia import SdamGIA

sdamgia = SdamGIA()

subject = 'math'
id = '1001'
a = sdamgia.get_problem_by_id(subject, id)



print(a)