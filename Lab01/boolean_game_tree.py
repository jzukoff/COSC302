######## Josh Zukoff, Zach Rabin, Connor Ford
######## Answers written as comments on bottom

import random
import math

class GameTree():

    # constructor
    def __init__(self, param):
        self.reset_count()
        if type(param) == list: # given a list of leaf values
            self.k = int(math.log(len(param), 2)//2)
            self.leaf_list = param
        else: # construct a random list of leaf values
            self.k = param
            self.leaf_list = []
            for i in range(2**(2*self.k)):
                self.leaf_list.append(round(random.random()))

    # These functions help keep count of how many leaves have been examined

    # resets the count to zero
    def reset_count(self):
        self.leaf_read_count = 0

    # returns the count
    def get_count(self):
        return self.leaf_read_count


    # returns a leaf value of the game tree
    def get_leaf(self, param):
        if type(param) == int: # given an integer index into the leaf_list
            if param >= 0 and param < 2**(2*self.k):
                self.leaf_read_count = self.leaf_read_count + 1
                return self.leaf_list[param]
        if type(param) == list: # given a left-right path; 0==left, 1==right
            index = 0
            for i in param:
                index = index*2 + i
            self.leaf_read_count = self.leaf_read_count + 1
            return self.leaf_list[index]

    # deterministic evaluation algorithm
    def evaluate1(self):
        return self.__recursive_evaluate1([])

    def __recursive_evaluate1(self, tree_path):
        if len(tree_path) == 2 * self.k: # have a path of depth 2k, so a leaf
            return self.get_leaf(tree_path)
        elif len(tree_path) < 2 * self.k:
            # evaluate the left subtree recursively
            left = self.__recursive_evaluate1(tree_path + [0])
            # evaluate the right subtree recursively
            right = self.__recursive_evaluate1(tree_path + [1])
            
            if len(tree_path) % 2 == 0:  # node corresponds to AND
                return left * right
            else:  # node corresponds to OR
                return left + right - (left * right)



    def evaluate2(self):
        return self.__recursive_evaluate2([])
    
    def __recursive_evaluate2(self, tree_path):
        if len(tree_path) == 2 * self.k: # have a path of depth 2k, so a leaf
            return self.get_leaf(tree_path)
        elif len(tree_path) < 2 * self.k:
            # evaluate the left subtree recursively
            left = self.__recursive_evaluate2(tree_path + [0])
            if len(tree_path) % 2 == 0:
                if left == 0:
                    return 0
            elif left == 1:
                return 1
            # evaluate the right subtree recursively
            right = self.__recursive_evaluate2(tree_path + [1])
            
            if len(tree_path) % 2 == 0:  # node corresponds to AND
                return left * right
            else:  # node corresponds to OR
                return left + right - (left * right)




    def evaluate3(self):
        return self.__recursive_evaluate3([])

    def __recursive_evaluate3(self, tree_path):
        if len(tree_path) == 2 * self.k: # have a path of depth 2k, so a leaf
            return self.get_leaf(tree_path)
        elif len(tree_path) < 2 * self.k:
            # evaluate the left subtree recursively
            randomChoice = random.randint(0,1)
            randomChild = self.__recursive_evaluate3(tree_path + [randomChoice])
            if len(tree_path) % 2 == 0:
                if randomChild == 0:
                    return 0
            elif randomChild == 1:
                return 1
            # evaluate the right subtree recursively
            if randomChoice == 0:
                otherChild = self.__recursive_evaluate3(tree_path + [1])
            else:
                otherChild = self.__recursive_evaluate3(tree_path + [0])
            
            if len(tree_path) % 2 == 0:  # node corresponds to AND
                return randomChild * otherChild
            else:  # node corresponds to OR
                return randomChild + otherChild - (randomChild * otherChild)


def main():
    k = eval(input("Enter number of turns (depth/2): "))
    T = GameTree(k)
    if 'y' in input("Print tree? "):
        print(T.leaf_list)
        input("Hit return to continue")
    answer = T.evaluate2()
    count = T.get_count()
    print("The tree evaluates to %d after reading %d leaf values." % (answer, count))

##    Below is our code for evaluating empirically the three algorithms

##
##    monteVegasDiff = []
##    count = 0
##    print ("K \t MonteCount \t VegasCount \t Worst Case")
##    for k in range(1,7):
##        for i in range(100):
##            
##
##            T = GameTree(k)
##            answer2 = T.evaluate2()
##            count2 = T.get_count()
##        
##            T.reset_count()
##            answer3 = T.evaluate3()
##            count3 = T.get_count()
##    
##            T.reset_count()
##            answer = T.evaluate1()
##            count = T.get_count()
##            monteVegasDiff.append(count3-count2)
##
##            print (k, "\t", count2, "\t\t", count3, "\t\t", count)
##    totalDiff = 0
##    for i in range(len(monteVegasDiff)):
##        totalDiff += monteVegasDiff[i]
##    print ("Avg Vegas-Monte")
##    print (totalDiff/len(monteVegasDiff))
##            


if __name__ == '__main__':
    main()

#A Runtime of the deterministic algorithm is O(2**(2k))

#C Yes there is a decrease in the number of leaves read, because aside from the worst case, you can at times only read the left child rather than both

#D The worst case scenario our pruning fails and all values on the left and right are checked, this would happen in for each and the left child is one, and for each or the left child is 0, therefore forcing you to check right as well

#F There really is not a difference between evaluate2() and evaluate3() this is because the inputs are being randomly generated so adding randomness to the choice of subtree does not actually improve our algorithm

#Description of Evaluation: For the test, we ran each of the three evaluate algorithms a fairly large number of times, on identical data sets of varying size. we then compared the results by finding the average difference between the results of evaluate2 and evaluate 3, which proved to hover around 0
