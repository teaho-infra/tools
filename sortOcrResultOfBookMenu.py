# 针对腾讯知图ocr一般图书目录输出的结果做处理
# 一般来讲，改掉process()的处理逻辑，改掉getLineOrder()的提取行顺序的逻辑就可复用
import re

def partition(arr, low, high):
    i = (low - 1)  # 最小元素索引
    pivot = arr[high]

    pivotNum = getLineOrder(pivot)

    for j in range(low, high):

        currentNum = getLineOrder(arr[j])
        # 当前元素小于或等于 pivot
        if currentNum <= pivotNum:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


# arr[] --> 排序数组
# low  --> 起始索引
# high  --> 结束索引

# 快排
def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def getLineOrder(str):
    res = re.findall(r"^[0-9]*", str)
    if res[0] == '':
        return 0
    else:
        return int(res[0])


def process(inputFileName, outputFileName):
    with open(inputFileName, 'r', 10) as file:
        lines = file.readlines()
        # Get useful lines
        lineFiltered = list(filter(lambda x: len(x.split("、")) > 1, lines))
        # print(lineFiltered)

        preHandleList = []
        for l in lineFiltered:
            # Get useful info
            splitArr = l.split("、")
            preHandleList.append(splitArr[1])

        quickSort(preHandleList, 0, len(preHandleList) - 1)

    with open(outputFileName, 'w') as writer:
        for breed in preHandleList:
            writer.write(breed)


process('\\place\\to\\input.txt', '\\place\\to\\output.txt')
