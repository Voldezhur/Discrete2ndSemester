class Node:
    def __init__(self, data):
        self.parent = None
        self.left = None
        self.right = None
        self.code = ''
        self.data = data
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()
    def insertLeft(self, data):
        self.left = Node(data)
        self.right.code = '1'
        self.left.parent = self
    def insertRight(self, data):
        self.right = Node(data)
        self.right.code = '0'
        self.right.parent = self

    def listify(self, nodesList):
        if self.right is None and self.left is None:
            nodesList.append((self.data, self.code))
        if self.left:
            self.left.listify(nodesList)

        if self.right:
            self.right.listify(nodesList)