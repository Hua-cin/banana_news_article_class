import pandas as pd

data = [{"A":1, "B":5, "C":3},{"A":1, "C":5},{"A":1,"C":2}]
columns = ["A","B","C"]


test = pd.DataFrame(data=data, columns=columns)
test = test.fillna(0)
print(test)
print('\n')
# test.loc[2,"A"] = test.loc[2,"A"]*10
# test.iloc[:1, :1] = test.iloc[:1, :1]
#
# for i in range(3):
#     test.iloc[i]=test.iloc[i]/test.iloc[i].max()
# test['區別']= [1,-1,0]
# test.iloc[1:2,:] = test.iloc[1:2,:] * (-1)
# print(test.iloc[1:2,:])

# test["A"][0]=10

# print(test)
for i in test:
    test[i][0] = test[i][0] * 10
print(test)

# for i in range(test.shape[0]):
#     if test["A"][i] == 0:
#         test.iloc[i, :] = test.iloc[i, :] * 100
# print(test)

# m_5 = ['價格', '颱風', '產量', '農民', '採收', '損失', '農業', '外銷', '出口']
# print('價格' in m_5)