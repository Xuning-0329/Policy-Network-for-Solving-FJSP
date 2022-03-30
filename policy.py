import math
import sys

import matplotlib.pyplot as plt
from policy_gradient import PolicyGradient
from src.utils.parser import parse
from src.utils.gantt import draw_chart
from decode import get_observation,decoding
from Rules import *
import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model
model= linear_model.LinearRegression()
import time
# path='./测试样例/test2.dat'
t0=time.time()
round=200
x=np.arange(0,round)
y=[]
table_index=0
operator=2
path= f'Mk1{table_index+1}.fjs'
job_machine=parse(path)
Job=len(job_machine['jobs'])
M=job_machine['machinesNb']
All_job_number=0
for i in range(Job):
    All_job_number+=len(job_machine['jobs'][i])


job_index=[
    [None for _ in range(len(job_machine['jobs'][i]))]
    for i in range(Job)
]
index_temp=1
for i in range(Job):
    for j in range(len(job_machine['jobs'][i])):
        job_index[i][j]=index_temp
        index_temp+=1




sf = open(f'Mk1{table_index+1}.txt')
sdata = sf.readlines()
setupTime = []
for i in range(M):
    temp = [
        [None for _ in range(All_job_number)]
        for _ in range(All_job_number+1)
    ]
    for j in range(All_job_number+1):
        line = sdata[i*(All_job_number+1)+j].replace('\n', '').replace('\r','').split()
        for k in range(All_job_number):
                temp[j][k] = line[k]
    setupTime.append(temp)
# for i in range(len(setupTime)):
#     print(setupTime[i])
# # print(setupTime)
# sys.exit(1)









n_actions=3
n_features=6
sd=[]
ave_f=0

RL = PolicyGradient(
    n_actions=n_actions,
    n_features=n_features,
    learning_rate=0.01,
    reward_decay=1,
    output_graph=False,
)

makespan_min = 10000
# min_data={}
for i_episode in range(round):
    index = [0 for i in range(Job)]
    machine_available_time = [[0 for _ in range(1000)] for __ in range(M)]
    operator_avilable_time = [[0 for _ in range(1000)] for __ in range(operator)]
    end_time = [0 for _ in range(Job)]
    end_job = [0 for _ in range(M)]
    machine_max = [0 for i in range(M)]
    indicator = 1
    total_time = 0
    makespan_before = 340
    OS = []
    MS = []
    se_time = []
    prc_time = []
    data = {}
    for idx in range(M):
        machine_name = f"Machine-{idx + 1}"
        data[machine_name] = []
    observation = get_observation(job_machine, index, machine_available_time, machine_max, All_job_number, end_time,
                                  indicator)
    # # print(observation)
    # result1=[]
    for i in range(All_job_number):
        action = RL.choose_action(observation, i_episode, round)
        if action == 0:
            result = rule1(machine_available_time, setupTime, operator_avilable_time, job_index, end_job, end_time,
                           index, job_machine, data)
        elif action == 1:
            result = rule2(machine_available_time, setupTime, operator_avilable_time, job_index, end_job, end_time,
                           index, job_machine, data)
        elif action == 2:
            result = rule3(machine_available_time, setupTime, operator_avilable_time, job_index, end_job, end_time,
                           index, job_machine, data)

        OS.append(result[0])
        MS.append(result[1])
        se_time.append(result[2])
        prc_time.append(result[3])
        #
        total_time += result[2] + result[3]
        # decoding(index, machine_available_time, end_time, result[0], result[1], result[2], machine_max)
        indicator = total_time / (i + 1) / max(end_time)
        observation_ = get_observation(job_machine, index, machine_available_time, machine_max, All_job_number,
                                       end_time, indicator)
        if i == All_job_number - 1:
            # print(data.items())
            # print(result1)
            if max(end_time) <= makespan_before:
                reward = 1
            else:
                reward = -1
            makespan_before = max(end_time)
            y.append(makespan_before)
            if makespan_min > max(end_time):
                makespan_min = max(end_time)
                min_data = data
        else:
            reward = 0
        RL.store_transition(observation, action, reward)
        observation = observation_
    # print(OS)
    # print(MS)
    # print(RL.ep_rs)
    # ep_rs_sum = sum(RL.ep_rs)
    # print(ep_rs_sum)
    # print("episode:", i_episode, "makespan:", max(end_time))
    vt = RL.learn()
# sd.append(makespan_min)
# ave_f+=makespan_min
print('最小makespan:', makespan_min)
# fin_res=0
# ave_f/=30
# for i in range(len(sd)):
#     fin_res=fin_res+(sd[i]-ave_f)**2
# fin_res=math.sqrt(fin_res/30)
# from xlutils.copy import copy
# import xlrd
# data=xlrd.open_workbook("实验结果.xls")
# workbook=copy(data)
# worksheet=workbook.get_sheet(table_index)
# for i in range(len(sd)):
#     worksheet.write(8,i+1,sd[i])
# worksheet.write(8,31,min(sd))
# worksheet.write(8,32,ave_f)
# worksheet.write(8,33,fin_res)
# x = np.array(x).reshape(-1, 1)
# y = np.array(y)
# model.fit(x, y)
# predict = model.predict(x)
# plt.plot(x, y, color='blue', linewidth=0.8)
# plt.plot(x, predict, color='red', linewidth=1.5)
# plt.xlim(0, round)
# plt.show()
draw_chart(min_data,'mk01')

# t1=time.time()
# print(t1-t0)

