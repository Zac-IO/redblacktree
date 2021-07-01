'''
CS3C Final Project
Zach Weisner
Red Black Tree Implementation
'''

import enum
import random


class Color(enum.Enum):
    null = 0
    red = 1
    black = 2

class RedBlackNode:

    def __init__(self, value = None, color = Color.null):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return f"{self.value}:{self.color.name}"

class RedBlackTree:

    class DuplicateError(Exception):
        pass

    class NotFoundError(Exception):
        pass

    def __init__(self):
        self.root = None
        self.count = 0
        self.null = RedBlackNode(value = None, color = Color.black)


    def insert(self,value):
        if self.root is None:
            self.root = RedBlackNode(value, color=Color.black)
            self.root.left = self.null
            self.root.right = self.null
            self.count+=1
            return
        inserted = RedBlackNode(value, color=Color.red)
        inserted.left = self.null
        inserted.right = self.null
        parent = self.find_parent(value)
        inserted.parent = parent
        if parent.value < value:
            parent.right = inserted
        else:
            parent.left = inserted

        self.fixup(inserted)
        self.count+=1

    def find_parent(self, value):
        previous = RedBlackNode()
        child = self.root
        while child is not self.null:  #Could also be sentinel node
            previous = child
            if child.value < value:
                child = child.right
            elif child.value > value:
                child = child.left
            else:
                raise self.DuplicateError
        return previous

    def fixup(self,node):
        while node and node.parent and node.parent.parent and \
            node.parent.color is Color.red:
            if node.parent.parent and node.parent is node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color is Color.red:
                    self.recolor(node,uncle)
                    node = node.parent.parent
                elif node is node.parent.right:
                    node = node.parent
                    self.left_rotation(node)
                else:
                    node.parent.color = Color.black
                    node.parent.parent.color = Color.red
                    self.right_rotation(node.parent.parent)
            else:
                uncle = node.parent.parent.left  #Right unbalanced
                if uncle is not None and uncle.color is Color.red:
                    self.recolor(node,uncle)
                    node = node.parent.parent
                elif node is node.parent.left:
                    node = node.parent
                    self.right_rotation(node.parent)
                else:
                    node.parent.color = Color.black
                    node.parent.parent.color = Color.red
                    self.left_rotation(node.parent.parent)


        self.root.color = Color.black

        return node

    def recolor(self, node,uncle):
        uncle.color = Color.black
        node.parent.color = Color.black
        node.parent.parent.color = Color.red
        #node = node.parent.parent
        #return node

    def left_rotation(self, node):
        if not node:
            return
        if node.right is self.null:
            return
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not self.null:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node is node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child



        #return right_child

    def right_rotation(self,node):
        if not node:
            return
        if node.left is self.null:
            return
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not self.null:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node is node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child


        #return left_child

    def __str__(self):
        return f"{self.count} sized binary tree\n" + self._str(self.root, 0)

    def _str(self, subtree_root, depth, _repr=False):
        if subtree_root is self.null or subtree_root is None:
            return ""

        s = ""
        s += self._str(subtree_root.right, depth + 1, _repr)
        s += (" " * 4 * depth
              + (repr(subtree_root) if _repr else str(subtree_root))
              + "\n")
        s += self._str(subtree_root.left, depth + 1, _repr)
        return s

    def in_order_walk(self):
        self.print_inorder(self.root)

    def print_inorder(self,subtree_root):
        if subtree_root is None:
            return
        self.print_inorder(subtree_root.left)
        print(subtree_root)
        self.print_inorder(subtree_root.right)


    def find(self, data):
        if self.root is None:
            raise AttributeError("Rootless red-black tree has no data")
        return self.recursive_find(self.root,data)

    def recursive_find(self,node,data):
        if node is self.null:
            raise RedBlackTree.NotFoundError
        if node is None or node.value == data:
            return node

        if data < node.value:
            return self.recursive_find(node.left, data)
        else:
            return self.recursive_find(node.right,data)

    def node_successor(self,node):
        if node.right:
            return self.find_minimum(node.right)
        y = node.parent
        while y and node is y.right:
            node = y
            y = y.parent

        return y

    def find_maximum(self,subtree_root):
        maximum = subtree_root
        while maximum.right is not self.null:
            maximum = maximum.right
        return maximum

    def tree_max(self):
        return self.find_maximum(self.root)

    def find_minimum(self,subtree_root):
        minimum = subtree_root
        while minimum.left is not self.null:
            minimum = minimum.left
        return minimum

    def red_black_delete(self,data):
        node = self.find(data)
        if node is None:
            raise RedBlackTree.NotFoundError

        if node.left is self.null or node.right is self.null:
            y = node
        else:
            y = self.node_successor(node)

        if y.left is not self.null:
            x = y.left
        else:
            x = y.right

        if x:
            x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y is y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        if y is not node:
            node.value = y.value

        self.count -=1

        if y.color is Color.black: #black height property potentially violated
            self.rb_delete_fixup(x) #looks ok until rb_delete_fixup()

    def rb_delete_fixup(self,x):
        while x is not self.root and x.color is \
            Color.black:
            if x is x.parent.left:
                sibling = x.parent.right
                if sibling is None or sibling.right is None or sibling.left \
                    is None:
                    break

                if sibling.color is Color.red:
                    sibling.color = Color.black
                    x.parent.color = Color.red
                    self.left_rotation(x.parent)
                    sibling = x.parent.right

                if sibling.left and sibling.right and sibling.left.color is \
                    Color.black and \
                    sibling.right.color is\
                    Color.black:

                    sibling.color = Color.red
                    x = x.parent
                else:
                    if sibling is None or sibling.right is None or sibling.left \
                        is None:
                        break
                    if sibling.right and sibling.right.color is Color.black:
                        sibling.left.color = Color.black
                        sibling.color = Color.red
                        self.right_rotation(sibling)
                        sibling = x.parent.right


                    sibling.color = x.parent.color
                    x.parent.color = Color.black
                    sibling.right.color = Color.black
                    self.left_rotation(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling is None or sibling.right is None or sibling.left \
                    is None:
                    break
                if sibling.color is Color.red:
                    sibling.color = Color.black
                    x.parent.color = Color.red
                    self.right_rotation(x.parent)
                    sibling = x.parent.left

                if sibling.right and sibling.left and sibling.right.color is \
                    Color.black and \
                    sibling.left.color is \
                    Color.black:

                    sibling.color = Color.red
                    x = x.parent
                else:
                    if sibling is None or sibling.right is None or sibling.left \
                        is None:
                        break
                    if sibling.left and sibling.left.color is Color.black:
                        sibling.right.color = Color.black
                        sibling.color = Color.red
                        self.left_rotation(sibling)
                        sibling = x.parent.left

                    sibling.color = x.parent.color
                    x.parent.color = Color.black
                    sibling.left.color = Color.black
                    self.right_rotation(x.parent)
                    x = self.root
        if x:
            x.color = Color.black



if __name__ == "__main__":

    test = RedBlackTree()
    for i in range(10000):
        test.insert(i)
        #print(test)
    print(test)
    # test.red_black_delete(4)
    # print(test)
    # test.red_black_delete(5)
    # print(test)
    # test.red_black_delete(6)
    # print(test)
    # test.red_black_delete(8)
    # print(test)
    # test.red_black_delete(9)
    # print(test)
    # test = RedBlackTree()
    # for _ in random.sample(range(100000),1000):
    #     test.insert(_)
    #     #print(_)
    #
    # print(test)
    #
    # test.in_order_walk()
    #
    # tree = RedBlackTree()
    # for i in range(1,11):
    #     tree.insert(i)
    # print(tree)
    # tree.red_black_delete(6)
    # print(tree)
    # tree.red_black_delete(9)
    # print(tree)

    removals = []
    test = RedBlackTree()
    for _ in random.sample(range(2000),10):
        removals.append(_)
        test.insert(_)
    random.shuffle(removals)
    for _ in removals:
        print(test)
        print(f"removing {_}")
        test.red_black_delete(_)
        print(test)

    # tree = RedBlackTree()
    # nodes = [3,2,10,7]
    # for x in nodes:
    #     tree.insert(x)
    # tree.red_black_delete(3)
    # print(tree)

