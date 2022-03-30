import random

#随机选择机器
def choose_byrandom(job_number, job_machine, index):
    machine = len(job_machine['jobs'][job_number][index[job_number]])
    machine_number = random.randint(0, machine - 1)
    machine = job_machine['jobs'][job_number][index[job_number]][machine_number]['machine']-1
    prc_time = job_machine['jobs'][job_number][index[job_number]][machine_number]['processingTime']
    index[job_number] += 1
    return machine,prc_time

#earliest avavilable
def choose_earliest(machine_available_time,end_time,job_number, job_machine, index): #earliest available机器
    machine = job_machine['jobs'][job_number][index[job_number]]
    start_time = end_time[job_number]
    select_machine=None
    time=None
    earliest_time=10000
    for item in machine:
        # print('item',item)
        machine_number=item['machine']-1
        # print('machine编号:',machine_number)
        prc_time=item['processingTime']
        for t in range(start_time, 1000):
            flag = True
            for prc_t in range(prc_time):
                if machine_available_time[machine_number][t + prc_t] != 0:
                    flag = False
            if flag:
                if t==earliest_time:
                    if prc_time<time:
                        time = prc_time
                        select_machine = machine_number
                    elif prc_time==time:
                        select_machine=random.choice([select_machine,machine_number])
                elif t<earliest_time:
                    earliest_time=t
                    time=prc_time
                    select_machine=machine_number
                break
    index[job_number]+=1
    return select_machine,time

#最小处理时间
def choose_min_prc_time(machine_available_time,end_time,job_number, job_machine, index):
    machine = job_machine['jobs'][job_number][index[job_number]]
    prc_time=10000
    select_machine=None
    for item in machine:
        if item['processingTime']<prc_time:
            select_machine=item['machine']-1
            prc_time=item['processingTime']
        elif item['processingTime']==prc_time:
            select_machine=random.choice([select_machine,item['machine']-1])
    index[job_number] += 1
    return select_machine,prc_time

#最小完成时间
def choose_min_complete_time(machine_available_time,setupTime,operator_avilable_time,job_index,end_job,end_time,job_number, job_machine, index,data):
    machine = job_machine['jobs'][job_number][index[job_number]]
    start_time = end_time[job_number]
    select_machine = None
    total_time=None
    time = None
    end = 10000
    se_time=None
    operator_index=None
    op_index=None

    for item in machine:


        # print('item',item)
        machine_number = item['machine'] - 1
        # print('machine编号:',machine_number)
        last_job = end_job[machine_number]
        # print(last_job)
        # print(job_index[job_number][index[job_number]]-1)
        setup_time = int(setupTime[machine_number][last_job][job_index[job_number][index[job_number]]-1])
        prc_time = item['processingTime']

        for t in range(start_time, 1000):
            for i in range(len(operator_avilable_time)):
                flag1=True
                for setup_t in range(setup_time):
                    if operator_avilable_time[i][t+setup_t]!=0:
                        flag1=False
                    if machine_available_time[machine_number][t+setup_t]!=0:
                        flag1=False
                if flag1:
                    operator_index=i
                    break
            if not flag1:
                continue
            flag2 = True
            for prc_t in range(prc_time):
                if machine_available_time[machine_number][t+setup_time + prc_t] != 0:
                    flag2 = False
            if flag2:
                if t+prc_time+setup_time == end:
                    if prc_time+setup_time<total_time:
                        total_time=prc_time+setup_time
                        time=prc_time
                        se_time=setup_time
                        select_machine = machine_number
                        op_index=operator_index
                    # elif prc_time==time:
                    #     select_machine = random.choice([select_machine, machine_number])
                elif t+prc_time+setup_time < end:
                    end = t+prc_time+setup_time
                    time = prc_time
                    se_time=setup_time
                    total_time=prc_time+setup_time
                    select_machine = machine_number
                    op_index = operator_index
                break
    start_time=end-time-se_time
    for t in range(se_time):
        operator_avilable_time[op_index][start_time+t]=1
    for t in range(se_time+time):
        machine_available_time[select_machine][start_time+t]=1
    end_job[select_machine]=job_index[job_number][index[job_number]]
    index[job_number] += 1
    end_time[job_number]=end
    machine_name = f"Machine-{select_machine + 1}"
    name_task = "{}-{}".format(job_number+1, index[job_number])
    data[machine_name].append((start_time+se_time, end, name_task,start_time))
    # print(index)
    # print(f"job:{job_number+1}-{index[job_number]},'machine:{select_machine+1}','start_time:{start_time}','setup_time:{se_time}','process_time:{time}'")
    return select_machine,se_time, time




#最小完工率 + 最小完成时间
def rule1(machine_available_time,setupTime,operator_avilable_time,job_index,end_job, end_time, index, job_machine,data):
    J = len(job_machine['jobs'])
    min=0
    min_rate=1
    for i in range(J):
        rate=index[i]/len(job_machine['jobs'][i])
        if index[i]/len(job_machine['jobs'][i])==min_rate:
            min=random.choice([min,i])
        elif index[i]/len(job_machine['jobs'][i])<min_rate:
            min=i
            min_rate=index[i]/len(job_machine['jobs'][i])



    machine,setup_time,prc_time=choose_min_complete_time(machine_available_time,setupTime,operator_avilable_time,job_index,end_job,end_time,min, job_machine, index,data)
    return min,machine,setup_time,prc_time

#最大剩余工序处理时间 + 最小完成时间
def rule2(machine_available_time,setupTime,operator_avilable_time,job_index,end_job, end_time, index, job_machine,data):
    J = len(job_machine['jobs'])
    job_number=None
    # max=0
    for number in range(J):
        if index[number]<len(job_machine['jobs'][number]):
            # remain=len(job_machine['jobs'][number])-index[number]
            # sum=0
            # count_number=0
            # for i in range(index[number],len(job_machine['jobs'][number])):
            #     average=0
            #     count=0
            #     for item in job_machine['jobs'][number][i]:
            #         average+=item['processingTime']
            #         count+=1
            #     sum+=average/count
            #     count_number+=1
            # sum/=count_number
            # if sum>max:
            #     max=sum
            #     job_number=number
            # elif sum==max:
            if not job_number:
                job_number=number
            job_number=random.choice([job_number,number])
    machine,setup_time,prc_time=choose_min_complete_time(machine_available_time,setupTime,operator_avilable_time,job_index,end_job,end_time,job_number, job_machine, index,data)
    return job_number, machine,setup_time,prc_time




#最小已完成工作最大完工时间 + 最小完成时间
def rule3(machine_available_time,setupTime,operator_avilable_time,job_index,end_job, end_time, index, job_machine,data):
    J = len(job_machine['jobs'])
    job_number =0
    min=1000
    for number in range(J):
        if index[number] < len(job_machine['jobs'][number]):
            if end_time[number]<min:
                min=end_time[number]
                job_number=number
            elif end_time[number]==min:
                # print(job_number, number)
                job_number=random.choice([number,job_number])
                # print(job_number,number)
    machine,setup_time,prc_time=choose_min_complete_time(machine_available_time,setupTime,operator_avilable_time,job_index,end_job,end_time,job_number, job_machine, index,data)
    return job_number, machine,setup_time,prc_time
