import pandas as pd

data = [{"A":0, "B":5},{"A":1, "C":5},{"A":1,"C":2}]
columns = ["A","B","C"]


test = pd.DataFrame(data=data, columns=columns)
test = test.fillna(0)
print(test)
test["B"] = test["B"]*10
print(test)

for i in range(test.shape[0]):
    if test["A"][i] == 0:
        test.iloc[i, :] = test.iloc[i, :] * 100
print(test)

# for i in range(dd.shape[0]):
#     if dd["香蕉"][i] == 0:
#         dd.iloc[i, 1:] = dd.iloc[i, 1:] * 100