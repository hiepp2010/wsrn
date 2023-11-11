import simpy
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from iostream1.Util import Util
from network.MobileCharger import MobileCharger
from network.Network import Network
from optimizer.offlineoptimizer.GraphRL.GraphRLOptimizer import GraphRlOptimizer

util = Util("D:/Hiep/wrsn-team-main/wrsn-team-main/algorithms_code/RLGraph/data/ga200.txt")
env = simpy.Environment()
net = Network(env=env, listNodes=util.listNodes, baseStation=util.BaseStation)
mc = MobileCharger(index=0, env=env, location=[250, 250])
testedT = 72000
algorithm = GraphRlOptimizer(env=env, T=18000, testedT=testedT)

env.process(mc.operate(net, testedT, algorithm))
env.process(algorithm.controller(mcs=[mc], net=net))
env.process(net.runNetwork(testedT))

env.run(until=testedT)
print(algorithm.log)
print('Time: ' + str(env.now) + ' The number of dead node:' + str(net.countDeadNodes()))
