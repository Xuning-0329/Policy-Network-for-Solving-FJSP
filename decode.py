import math
import numpy as np

makespan_b=0
def decoding(index,machine_available_time,end_time,job_number,machine,prc_time,machine_max):
        start_time=end_time[job_number]
        for t in range(start_time,1000):
            flag = True
            for prc_t in range(prc_time):
                if machine_available_time[machine][t+prc_t]!=0:
                    flag=False
            if flag:
                # machine_name=f"Machine-{machine+1}"
                # name_task = "{}-{}".format(job_number+1, index[job_number])
                # end_time[job_number]=t+prc_time
                # start_time=t
                # data[machine_name].append((start_time,end_time[job_number],name_task))
                for number in range(start_time,start_time+prc_time):
                    machine_available_time[machine][number]=1
                machine_max[machine]=max(machine_max[machine],t+prc_time)
                break
#state1:平均机器利用率
#state2:机器利用率标准差
#state3:opearations完成率
#state4:每个job平均完成率
#state5:job完成率标准差
#state6:预计makespan
#state7:
def get_observation(job_machine,index,machine_available_time,machine_max,All_job_number,end_time,indicator):
    global makespan_b
    # print(makespan_b)
    state1=0
    M=len(machine_available_time)
    count=0
    for i in range(M):
        if machine_max[i]!=0:
            count+=1
            state1+=machine_available_time[i].count(1)/machine_max[i]
    if count==0:
        state1=1
    else:
        state1/=count
    state2=0
    for i in range(M):
        if machine_max[i] != 0:
            state2+=(machine_available_time[i].count(1)/machine_max[i]-state1)**2
    if count==0:
        state2=0
    else:
        state2=math.sqrt(state2/count)
    state3=0
    Job=len(job_machine['jobs'])
    for i in range(Job):
        state3+=index[i]
    state3/=All_job_number
    state4=0
    for i in range(Job):
        state4+=index[i]/len(job_machine['jobs'][i])
    state4/=Job
    state5=0
    for i in range(Job):
        state5+=(index[i]/len(job_machine['jobs'][i])-state4)**2
    state5=math.sqrt(state5/Job)
    # state6_1=0
    # for i in range(Job):
    #     start_time = end_time[i]
    #     for j in range(index[i], len(job_machine['jobs'][i])):
    #         average = 0
    #         count = 0
    #         for item in job_machine['jobs'][i][j]:
    #             average += item['processingTime']
    #             count += 1
    #         start_time += average / count
    #     if start_time > state6_1:
    #         state6_1 = start_time
    # if makespan_b==0:
    #     state6=1
    # else:
    #     state6=state6_1/makespan_b
    # makespan_b=state6_1
    state7=indicator
    # print("观测值为:",(state1,state2,state3,state4,state5,state6,state7))
    return np.array((state1,state2,state3,state4,state5,state7))
