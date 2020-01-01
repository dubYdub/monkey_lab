
def handle_bounds(bounds):
    tmp = bounds.partition('][')
    list1 = tmp[0]
    list2 = tmp[2]
    list1 = list1.split(",")
    list2 = list2.split(",")
    # print(list1)
    x1 = int(list1[0][1:])
    y1 = int(list1[1])
    x2 = int(list2[0])
    y2 = int(list2[1][:-1])
    return (x1+x2)/2, (y1+y2)/2

bounds = "[0,799][360,925]"
a,b = handle_bounds(bounds)
print(a,b)