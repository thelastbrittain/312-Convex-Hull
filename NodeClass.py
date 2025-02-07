from __future__ import annotations


class Node:
    """
    This class holds a tuple of points, the reference to node to the left,
    and the refernce to node to the right
    """

    def __init__(
        self,
        point: tuple[float, float],
        lNode: "Node" | None = None,
        rNode: "Node" | None = None,
    ):
        self.point = point
        self.lNode = lNode
        self.rNode = rNode

    def get_point(self) -> tuple[float, float]:
        return self.point

    def set_point(self, point: tuple[float, float]):
        self.point = point

    def set_lNode(self, lNode: "Node"):
        self.lNode = lNode

    def set_rNode(self, rNode: "Node"):
        self.rNode = rNode

    def get_rNode(self) -> "Node" | None:
        return self.rNode

    def get_lNode(self) -> "Node" | None:
        return self.lNode
