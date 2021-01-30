# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt

c = open("squid/squid.csv", 'r')
#c = open("vsftpd/vsftpd.csv")
#print c.readlines()
method = {}
parameters = {}
rec_type = {}

class point(object):
    def __init__(self, method, parameter, rec_num, rec_type):
        self.method = method
        self.parameter = parameter
        self.rec_num = rec_num
        self.rec_type = rec_type
        self.m_axis = 0
        self.p_axis = 0
        self.r_axis = []

def generate_axis(points):
    global method, parameters, rec_type

    for p in points:
        method_len = len(method)
        if p.method in method:
            pass
        else:
            method[p.method] = method_len + 1

        parameters_len = len(parameters)
        if p.parameter in parameters:
            pass
        else:
            parameters[p.parameter] = parameters_len + 1

        rec_type_len = len(rec_type)
        for rec in p.rec_type:
            if rec in rec_type:
                pass
            else:
                rec_type[rec] = rec_type_len + 1

    for p in points:
        p.m_axis = method[p.method]
        p.p_axis = parameters[p.parameter]
        p.r_axis = [rec_type[rec] for rec in p.rec_type]






points = []
lines = c.readlines()
for line in lines:
    line = line.strip('\n')
    args = line.split(',')
    p = point(*args)
    points.append(p)

generate_axis(points)

style = {1:">", 2:"<", 3:"^"}
color = {1:"b", 2:"r", 3:"g"}

plt.subplot(311)
plt.xlim((0, len(parameters)+1))
plt.ylim((0, len(rec_type)+1))
plt.xlabel('Options ID')
plt.ylabel('Reactions ID')
plt.title("Reaction Distribution of Random Testing")

for p in points:
    if p.m_axis == 1:
        for rec_axis in p.r_axis:
            rec_num = p.r_axis.count(rec_axis)
            plt.scatter(p.p_axis, rec_axis, marker='$'+str(rec_num)+'$', c=color[p.m_axis], alpha=1)

plt.subplot(312)
plt.xlim((0, len(parameters)+1))
plt.ylim((0, len(rec_type)+1))
plt.xlabel('Options ID')
plt.ylabel('Reactions ID')
plt.title("Reaction Distribution of Mutation-based Testing")


for p in points:
    if p.m_axis == 2:
        for rec_axis in p.r_axis:
            rec_num = p.r_axis.count(rec_axis)
            plt.scatter(p.p_axis, rec_axis, marker='$'+str(rec_num)+'$', c=color[p.m_axis], alpha=1)

plt.subplot(313)
plt.xlim((0, len(parameters)+1))
plt.ylim((0, len(rec_type)+1))
plt.xlabel('Options ID')
plt.ylabel('Reactions ID')
plt.title("Reaction Distribution of Constraints-based Testing")

for p in points:
    if p.m_axis == 3:
        for rec_axis in p.r_axis:
            rec_num = p.r_axis.count(rec_axis)
            plt.scatter(p.p_axis, rec_axis, marker='$'+str(rec_num)+'$', c=color[p.m_axis], alpha=1)

plt.savefig("squid.pdf")
plt.show()


