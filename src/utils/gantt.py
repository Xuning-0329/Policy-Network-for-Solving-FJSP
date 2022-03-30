#!/usr/bin/env python

# This module helps creating Gantt from a dictionary or a text file.
# Output formats are a Matplotlib chart or a LaTeX code (using pgfgantt).
from matplotlib.pyplot import MultipleLocator
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import colors as mcolors
import random
matplotlib.rcParams['pdf.fonttype']=42
matplotlib.rcParams['ps.fonttype']=42
colors = []

for name, hex in mcolors.cnames.items():
    colors.append(name)
random.shuffle(colors)

def parse_data(file):
    try:
        textlist = open(file).readlines()
    except:
        return

    data = {}

    for tx in textlist:
        if not tx.startswith('#'):
            splitted_line = tx.split(',')
            machine = splitted_line[0]
            operations = []

            for op in splitted_line[1::]:
                label = op.split(':')[0].strip()
                l = op.split(':')[1].strip().split('-')
                start = int(l[0])
                end = int(l[1])
                operations.append([start, end, label])

            data[machine] = operations
    return data


def draw_chart(data,filename):
    nb_row = len(data.keys())

    pos = np.arange(0.5, nb_row * 0.5 + 0.5, 0.5)

    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)

    index = 0
    max_len = []
    x_ticks=[0]
    for machine, operations in data.items():
        for op in operations:
            max_len.append(op[1])
            number = int(op[2].split("-")[0])
            # c = colors[number]
            c='white'
            rect = ax.barh((index * 0.5) + 0.5, op[1]-op[0], left=op[0], height=0.3, align='center',
                           edgecolor='black', color=c, alpha=0.8)


            # max_len.append(op[3])
            c2='royalblue'
            rect2=ax.barh((index * 0.5) + 0.5, op[0]-op[3], left=op[3], height=0.3, align='center',
                           edgecolor='black', color=c2, alpha=0.8)


            # adding label
            width = int(rect[0].get_width())
            Str='${O_{%s%s}}$'%(op[2].split('-')[0],op[2].split('-')[1])
            # Str = f"O_{op[2].split('-')[0]}{op[2].split('-')[1]}"
            xloc = op[0] + 0.50 * width
            x_ticks.append(xloc)
            clr = 'black'
            align = 'center'

            yloc = rect[0].get_y() + rect[0].get_height() / 2.0
            ax.text(xloc, yloc, Str, horizontalalignment=align,
                            verticalalignment='center', color=clr,fontsize=10, weight='bold',
                            clip_on=True)

            # c2 = 'green'
            # rect1 = ax.barh((index * 0.5) + 0.5, op[2], left=op[0] + op[1], height=0.3, align='center', edgecolor=c2,
            #                 color=c2, alpha=0.8)
            #
            # width = int(rect1[0].get_width())
            # Str1 = ""
            # xloc1 = op[0]+op[1] + 0.50 * width
            # x_ticks.append(xloc1)
            # clr = 'black'
            # align = 'center'
            # yloc1 = rect1[0].get_y() + rect1[0].get_height() / 2.0
            # ax.text(xloc1, yloc1, Str1, horizontalalignment=align,
            #         verticalalignment='center', color=clr, fontsize=7, weight='bold',
            #         clip_on=True)

        index += 1
    x_ticks.append(max_len)

    ax.set_ylim(ymin=-0.1, ymax=nb_row * 0.5 + 0.5)
    # ax.grid(color='gray', linestyle=':')
    # x_major_locator = MultipleLocator(2)
    # ax.xaxis.set_major_locator(x_major_locator)
    ax.set_xlim(0, max(max_len))
    # ax.axis.Axis
    print('最优makesapn:',max(max_len))

    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=1)

    font = font_manager.FontProperties(size='small')
    # ax.legend(loc=1, prop=font,label=filename)

    ax.invert_yaxis()
    plt.title("Flexible Job Shop Solution")
    # plt.axis('off')
    plt.savefig(filename+'.png')
    plt.show()


def export_latex(data):
    max_len = []
    head = """
\\noindent\\resizebox{{\\textwidth}}{{!}}{{
\\begin{{tikzpicture}}[x=.5cm, y=1cm]
\\begin{{ganttchart}}{{1}}{{{}}}
[vgrid, hgrid]{{{}}}
\\gantttitle{{Flexible Job Shop Solution}}{{{}}} \\\\
\\gantttitlelist{{1,...,{}}}{{1}} \\\\
"""
    footer = """
\\end{ganttchart}
\\end{tikzpicture}}\n
    """
    body = ""
    for machine, operations in sorted(data.items()):
        counter = 0
        for op in operations:
            max_len.append(op[1])
            label = "O$_{{{}}}$".format(op[2].replace('-', ''))
            body += "\\Dganttbar{{{}}}{{{}}}{{{}}}{{{}}}".format(machine, label, op[0]+1, op[1])
            if counter == (len(operations) - 1):
                body += "\\\\ \n"
            else:
                body += "\n"
            counter += 1

    lenM = max(10, max(max_len))
    print(head.format(lenM, lenM, lenM, lenM))
    print(body)
    print(footer)

