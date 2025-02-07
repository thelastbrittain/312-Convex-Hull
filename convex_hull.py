# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, plot_points  # type: ignore
from NodeClass import Node
from test_utils import is_convex_hull  # type: ignore

""""
Work log:
Got basic code down for joining small hulls of 3 points or less
Figure out some code for debugging to draw lines
For some reason the tests are not working
They do not like my Node class, specifically that lnode can be of type str/None. 

Next task: Figure out why the tests are angry
Also making a github repo would be a good thing for this project. Maybe even all of the projects. 
"""


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # sort hull points by x-coordinate

    points = sorted(points, key=lambda point: point[0])
    plot_points(points)

    node_list: list[Node] = divide_and_conquer(points)

    resList: list[tuple[float, float]] = []
    firstNode = node_list[0]
    resList.append(firstNode.get_point())  # type: ignore
    nextNode = firstNode.get_rNode()
    while nextNode != firstNode and nextNode:
        resList.append(nextNode.get_point())
        nextNode = nextNode.get_rNode()
    assert is_convex_hull(resList, points)
    return resList


# actually want this to return a list of nodes
def divide_and_conquer(points: list[tuple[float, float]]) -> list[Node]:
    if len(points) == 1:
        return createNodes(points)
    else:
        # assert that this splits list into two halves
        lList = divide_and_conquer(points[: len(points) // 2])
        rList = divide_and_conquer(points[len(points) // 2 :])
        combinedList = combine(lList, rList)
        return combinedList


def combine(lList: list[Node], rList: list[Node]) -> list[Node]:
    # find upper tangent
    upperBound: tuple[Node | None, Node | None] = findUpperTangent(lList, rList)
    lowerBound: tuple[Node | None, Node | None] = findLowerTangent(lList, rList)
    # remove unnecesary edges
    removeBadNodeConnections(upperBound, lowerBound)
    # lList.extend(rList)
    newList = [lList[0], rList[len(rList) - 1]]
    return newList


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
        draw_line(leftUpper.get_point(), rightUpper.get_point())
        leftLower.set_lNode(rightLower)
        rightLower.set_rNode(leftLower)
        draw_line(leftLower.get_point(), rightLower.get_point())


def findUpperTangent(
    lList: list[Node], rList: list[Node]
) -> tuple[Node | None, Node | None]:
    leftTangent: Node | None = lList[len(lList) - 1]
    rightTangent: Node | None = rList[0]
    temp = (leftTangent, rightTangent)
    draw_line(rightTangent.get_point(), leftTangent.get_point())  # type: ignore

    done = False
    while not done:
        done = True
        while upperLeftNotCalibrated(temp[0], temp[1]):
            if leftTangent is not None:
                leftTangent = leftTangent.get_lNode()
                temp = (leftTangent, rightTangent)
                draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False
        while upperRightNotCalibrated(temp[0], temp[1]):
            if rightTangent is not None:
                rightTangent = rightTangent.get_rNode()
                temp = (leftTangent, rightTangent)
                draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False

    return temp


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

    draw_line(rightTangent.get_point(), leftTangent.get_point())  # type: ignore

    done = False
    while not done:
        done = True
        while lowerLeftNotCalibrated(temp[0], temp[1]):
            if leftTangent is not None:
                leftTangent = leftTangent.get_rNode()
                temp = (leftTangent, rightTangent)
                draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
                done = False
        while lowerRightNotCalibrated(temp[0], temp[1]):
            if rightTangent is not None:
                rightTangent = rightTangent.get_lNode()
                temp = (leftTangent, rightTangent)
                draw_line(leftTangent.get_point(), rightTangent.get_point())  # type: ignore
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
