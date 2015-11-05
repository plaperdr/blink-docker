import random

class Node:
    # Each node in the heap has a value, name of the file, original weight, weight, and total weight.
    # The total weight self.tw is self.w plus the weight of any children.
    __slots__ = ['v', 'f', 'ow', 'w', 'tw']
    def __init__(self, v, f, w):
        self.v, self.f, self.ow, self.w, self.tw = v, f, w, w, w

class RWS(list):
    #Random Weighted Sample
    #This class has been created to be able to get random
    #items from a weighted sample

    def __init__(self, items):
        super().__init__()
        for v, f, w in items:
            self.append(Node(v, f, w))             # create all the nodes
        for i in range(len(self) - 1, 0, -1):   # total up the tws
            self[i - 1].tw += self[i].tw        # add self[i]'s total to its parent

    def resetWeights(self):
        for i in range(0,len(self)):
            self[i].w = self[i].ow
            self[i].tw = self[i].ow
        for i in range(len(self) - 1, 0, -1):
            self[i - 1].tw += self[i].tw


    def popRandom(self):
        gas = self[0].tw * random.random()  # start with a random amount of gas
        i = 0                               # start driving at the root
        while gas > self[i].w:              # while we have enough gas to get past node i:
            gas -= self[i].w                #   drive past node i
            i += 1                          #   move to next node
        f = self[i].f                       # out of gas! h[i] is the selected node.
        w = self[i].w
        self[i].w = 0                       # make sure this node isn't chosen again
        while i>=0:                         # fix up total weights
            self[i].tw -= w
            i -= 1
        return f

    def getRandomItems(self,n):
        res = []
        for i in range(n):
            res.append(self.popRandom())
        return res

    def print(self):
        for node in self:
            print("{} {} {}".format(node.v,node.w,node.tw))


def main():
    print("RWS Test")
    plugList = [("1","A",50),("2","A",10),("3","A",1),("4","A",1),("5","A",1),("6","A",1),("7","A",1),("8","A",1),("9","A",1),("10","A",1),("11","A",1),("12","A",1),
                ("13","A",1),("14","A",1),("15","A",1),("16","A",1),("17","A",1),("18","A",1),("19","A",1),("20","A",1),("21","A",1),("22","A",1),("23","A",1),
                ("24","A",1),("25","A",1)]

    rws = RWS(plugList)
    chosen = rws.getRandomItems(5)
    print(chosen)
    rws.resetWeights()
    chosen = rws.getRandomItems(5)
    print(chosen)

if __name__ == '__main__':
    main()