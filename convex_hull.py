# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, plot_points, draw_hull  # type: ignore
from NodeClass import Node


""""
Work log:
Got basic code down for joining small hulls of 3 points or less
Figure out some code for debugging to draw lines
For some reason the tests are not working
They do not like my Node class, specifically that lnode can be of type str/None. 

Next task: Figure out why the tests are angry
Also making a github repo would be a good thing for this project. Maybe even all of the projects. 
"""
# Time: O(nlogn)
# sorting takes O(nlogn)
# divide_and_conquer also takes O(nlogn)
# result list takes O(n)
# Total = nlogn + nlogn + n = O(nlogn)


# Space: O(n)
# Input = n
# Python sorting at worst takes O(n) space
# divide_and_conquer takes O(n) space as well
# making result list as worst takes O(n)
# total = n + n + n = O(n)
def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""

    points = sorted(
        points, key=lambda point: point[0]
    )  # sort hull points by x-coordinate
    plot_points(points)

    node_list: list[Node] = divide_and_conquer(points)
    resList: list[tuple[float, float]] = makeResultList(node_list[0])
    draw_hull(resList)
    return resList


# time: going through each node to insert into resList at worst takes O(n)
# space: makes list at worst of length n = O(n)
def makeResultList(originNode: Node) -> list[tuple[float, float]]:
    resList: list[tuple[float, float]] = []
    resList.append(originNode.get_point())  # type: ignore
    nextNode = originNode.get_rNode()
    while nextNode != originNode and nextNode:
        resList.append(nextNode.get_point())
        nextNode = nextNode.get_rNode()
    return resList


# O(nlogn)
# Time: creates two new problems of half the size. Combining operation takes O(n), so whole equation == T(n) = 2T(n/2) + O(n)
# According to the master theorem: if we put a/b^d we get 2/2^1 which == 1. If this == 1, then we have T(n) = O(n^d logn).
# d is just 1, so we end up with O(nlogn) for time complexity


# O(n)
# Space: The input is of size n, and we create a node for every input, so we end up with n nodes
# We are creating new lists, but those lists only have a constant 2 elements
# We are using recursion which utilizes the stack, however we split the problem in half with each call
# The maximum depth reached will be depth = log base 2 of n. So our space complexity for the stack is O(logn)
# Combining everyhting, we get n (input) + n (nodes created) + logn (stack storage). The n dominates, so we get O(n)
def divide_and_conquer(points: list[tuple[float, float]]) -> list[Node]:
    if len(points) == 1:
        return createNodes(points)
    else:
        # assert that this splits list into two halves
        lList = divide_and_conquer(points[: len(points) // 2])
        rList = divide_and_conquer(points[len(points) // 2 :])
        combinedList = combine(lList, rList)
        return combinedList


# calculating upper/lower tangents is linear time O(n), and constant space complexity.
# removing bad nodes is constant space and time. It is just reassignign pointers in the left and rightmost nodes
# Overall time = O(n) + O(constant) = O(n)
# Overall Space = O(constant)
def combine(lList: list[Node], rList: list[Node]) -> list[Node]:
    # find upper tangent
    upperBound: tuple[Node | None, Node | None] = findUpperTangent(lList, rList)
    lowerBound: tuple[Node | None, Node | None] = findLowerTangent(lList, rList)
    # remove unnecesary edges
    removeBadNodeConnections(upperBound, lowerBound)
    # lList.extend(rList)
    newList = [lList[0], rList[len(rList) - 1]]
    return newList


# time/space: There are no loops, and every operation in this function is constant. No new data structures are created, it's just new assignments
# so this entire function is constant space/time complexity
def removeBadNodeConnections(
    upperBound: tuple[Node | None, Node | None],
    lowerBound: tuple[Node | None, Node | None],
) -> None:
    """
    The assumption is that in the left list, all nodes clockwise of the upper bound and counter clockwise of lower bound should have connections killed
    With the right list, everything conter clockwise of the upper bound and counter clockwise of the lower bound should be killed
    """
    leftUpper: Node | None = upperBound[0]
    leftLower: Node | None = lowerBound[0]
    rightUpper: Node | None = upperBound[1]
    rightLower: Node | None = lowerBound[1]
    if leftUpper and leftLower and rightLower and rightUpper:
        leftUpper.set_rNode(rightUpper)
        rightUpper.set_lNode(leftUpper)
        # draw_line(leftUpper.get_point(), rightUpper.get_point())
        leftLower.set_lNode(rightLower)
        rightLower.set_rNode(leftLower)
        # draw_line(leftLower.get_point(), rightLower.get_point())


# Time: at worst, the left and right most points will be at the very bottom, and every node will have to
# be checked twice, making this O(2n) where n is the lenght of the left and right lists. So this will be linear: O(n)
# Space: There is no recursion, and we only create a constant numbber of variables to hold the nodes, so this is constant space.
# although we might change leftTangent/rightTangent n times, assuming we are just replacing the old variable, this is still constant.
def findUpperTangent(
    lList: list[Node], rList: list[Node]
) -> tuple[Node | None, Node | None]:
    leftTangent: Node | None = lList[len(lList) - 1]
    rightTangent: Node | None = rList[0]
    temp = (leftTangent, rightTangent)
    # draw_line(rightTangent.get_point(), leftTangent.get_point())  # type: ignore

    done = False
    while not done:
        done = True
        while upperLeftNotCalibrated(temp[0], temp[1]):
            if leftTangent is not None:
                leftTangent = leftTangent.get_lNode()
                temp = (leftTangent, rightTangent)
                # draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False
        while upperRightNotCalibrated(temp[0], temp[1]):
            if rightTangent is not None:
                rightTangent = rightTangent.get_rNode()
                temp = (leftTangent, rightTangent)
                # draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False

    return temp


# time complexity: calculating slope is constant, comparison also constant, so time complexity is O(constant)
# space complexity: two values are required to hold slopes, this is also constant. O(constant)
def upperLeftNotCalibrated(lNode: Node | None, rNode: Node | None) -> bool:
    """
    Upper left is not calibrated as long as if we went counter clockwise, we got a lower slope
    """
    if lNode is not None and rNode is not None:
        initialSlope = calculate_slope(lNode.get_point(), rNode.get_point())
        potentialNewSlope = calculate_slope(
            lNode.get_lNode().get_point(),  # type: ignore
            rNode.get_point(),
        )
        return potentialNewSlope < initialSlope
    print("Node was None")
    return False


def upperRightNotCalibrated(lNode: Node | None, rNode: Node | None) -> bool:
    if lNode is not None and rNode is not None:
        initialSlope = calculate_slope(lNode.get_point(), rNode.get_point())
        potentialNewSlope = calculate_slope(
            lNode.get_point(),
            rNode.get_rNode().get_point(),  # type: ignore
        )
        return potentialNewSlope > initialSlope
    print("Node was None")
    return False


def findLowerTangent(
    lList: list[Node], rList: list[Node]
) -> tuple[Node | None, Node | None]:
    leftTangent: Node | None = lList[len(lList) - 1]
    rightTangent: Node | None = rList[0]
    temp = (leftTangent, rightTangent)

    # draw_line(rightTangent.get_point(), leftTangent.get_point())  # type: ignore

    done = False
    while not done:
        done = True
        while lowerLeftNotCalibrated(temp[0], temp[1]):
            if leftTangent is not None:
                leftTangent = leftTangent.get_rNode()
                temp = (leftTangent, rightTangent)
                # draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False
        while lowerRightNotCalibrated(temp[0], temp[1]):
            if rightTangent is not None:
                rightTangent = rightTangent.get_lNode()
                temp = (leftTangent, rightTangent)
                # draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False

    return temp


def lowerLeftNotCalibrated(lNode: Node | None, rNode: Node | None) -> bool:
    """
    Lower left is not calibrated as long as if we went clockwise, we got a bigger slope
    """
    if lNode is not None and rNode is not None:
        initialSlope = calculate_slope(lNode.get_point(), rNode.get_point())
        potentialNewSlope = calculate_slope(
            lNode.get_rNode().get_point(),  # type: ignore
            rNode.get_point(),
        )
        return potentialNewSlope > initialSlope
    print("Node was None")
    return False


def lowerRightNotCalibrated(lNode: Node | None, rNode: Node | None) -> bool:
    """
    Lower right not calibrated when, if we go counter clockwise, we get a lower slope
    """
    if lNode is not None and rNode is not None:
        initialSlope = calculate_slope(lNode.get_point(), rNode.get_point())
        potentialNewSlope = calculate_slope(
            lNode.get_point(),
            rNode.get_lNode().get_point(),  # type: ignore
        )
        return potentialNewSlope < initialSlope
    print("Node was None")
    return False


def createNodes(points: list[tuple[float, float]]) -> list[Node]:
    soloNode = Node(points[0])
    soloNode.set_lNode(soloNode)
    soloNode.set_rNode(soloNode)
    return [soloNode]


def calculate_slope(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    x1, y1 = point1
    x2, y2 = point2

    return (y2 - y1) / (x2 - x1)
