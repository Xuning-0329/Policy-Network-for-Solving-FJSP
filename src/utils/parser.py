#!/usr/bin/env python

# This module parses .fjs files as found in the "Monaldo" FJSP dataset.
# More explanations on this file format can be found in the dataset.

path='../../test_data/Brandimarte_Data/Text/Mk01.fjs'
def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:2]))
    # print(firstLineValues)

    jobsNb = firstLineValues[0] #工作数量
    machinesNb = firstLineValues[1] #机器数量

    jobs = []

    for i in range(jobsNb):
        currentLine = file.readline()
        currentLineValues = list(map(int, currentLine.split()))
        # print(currentLineValues)
        operations = []

        j = 1
        while j < len(currentLineValues):
            k = currentLineValues[j]
            j = j+1
            # print(j)

            operation = []

            for ik in range(k):
                machine = currentLineValues[j]
                j = j+1
                processingTime = currentLineValues[j]
                j = j+1

                operation.append({'machine': machine, 'processingTime': processingTime})
            operations.append(operation)
        jobs.append(operations)
        # print(operations)


    file.close()
    # print(jobs[0][5])
    return {'machinesNb': machinesNb, 'jobs': jobs}
# parse(path)
# dict=parse(path)
# print(dict)