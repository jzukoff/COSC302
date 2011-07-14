
                                       
def intersection(line1,line2):
    x = (line2[1] - line1[1]) / (line1[0] - line2[0])
    y = line1[0]*x + line1[1]
    return (x,y)

def merge(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        slopel = left[i][0]
        sloper = right[j][0]
        if slopel == sloper:
            if left[i][1] > right[j][1]:
                if len(result)==0:
                    result.append(left[i])
                else:
                    z = i-1
                    while z>0 and intersection(left[i],result[z])[1] > intersection(result[z],result[z-1])[1]:
                        result.pop(len(result)-1)
                        z-=1
                    if len(result)>0:
                        intersectX = intersection(left[i], result[len(result)-1])[0]
                        result[len(result)-1][3] = intersectX
                        left[i][2] = intersectX
                    result.append(left[i])
            else:
                if len(result) == 0:
                    result.append(right[j])
                else:
                    z = i-1
                    while z>0 and intersection(right[j],result[z])[1] > intersection(result[z],result[z-1])[1]:
                        result.pop(len(result)-1)
                        z-=1
                    if len(result)>0:
                        intersectX = intersection(right[j], result[len(result)-1])[0]
                        result[len(result)-1][3] = intersectX
                        right[j][2] = intersectX
                    result.append(right[j])
            i += 1
            j += 1
        
        elif slopel <= sloper:
            z = len(result) - 1
            while z>0 and intersection(left[i],result[z])[0] < intersection(left[i],result[z-1])[0]:
                result.pop(len(result)-1)
                z-=1
            if len(result)>0:
                intersectX = intersection(left[i], result[len(result)-1])[0]
                result[len(result)-1][3] = intersectX
                left[i][2] = intersectX
            result.append(left[i])
            i += 1
            
        else:
            z = len(result) - 1
            while z>0 and intersection(right[j],result[z])[0] < intersection(right[j],result[z-1])[0]:
                result.pop(len(result)-1)
                z-=1
            if len(result) > 0:
                intersectX = intersection(right[j], result[len(result)-1])[0]
                result[len(result)-1][3] = intersectX
                right[j][2] = intersectX
            result.append(right[j])
            j += 1
    while (i < len(left)):
        intersectX = intersection(left[i], result[len(result)-1])[0]
        if type(result[len(result)-1][2]) == type(""):
            result[len(result)-1][3] = intersectX
            left[i][2] = intersectX
            result.append(left[i])
            i+=1
        elif intersectX > result[len(result)-1][2]:
            result[len(result)-1][3] = intersectX
            left[i][2] = intersectX
            result.append(left[i])
            i+=1
        else:
            result.pop(len(result)-1)
            
    while (j < len(right)):
        intersectX = intersection(right[j],result[len(result)-1])[0]
        if type(result[len(result)-1][2]) == type(""):
            result[len(result)-1][3] = intersectX
            right[j][2] = intersectX
            result.append(right[j])
            j+=1
        elif intersectX > result[len(result)-1][2]:
            result[len(result)-1][3] = intersectX
            right[j][2] = intersectX
            result.append(right[j])
            j+=1
        else:
            result.pop(len(result)-1)
    return result

def mergesort(lines):
    if len(lines) < 2:
        return lines
    else:
        middle = len(lines) // 2
        left = mergesort(lines[:middle])
        right = mergesort(lines[middle:])
        return merge(left, right)
    
def main():
    surface = []
    lines = []
    try:
        i = 0
        while True:
            line = eval(input())
            lines.append(list(line) + ['-','+'])
            i+=1

    except EOFError:
        None

    lines = mergesort(lines)
    print (['minX','maxX'], '\t', ['m','b'])
    for line in lines:
        ### Rounding just for formatting purposes ###
        for i in range(len(line)):
            if type(line[i]) != type(""):
                line[i] = round(line[i],2)
        print ([line[2:4]], '\t', [line[0:2]])






if __name__=='__main__':
    main()
