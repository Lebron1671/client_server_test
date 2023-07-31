from Application.ClientSide.IClient import IClient
from Application.ServerSide.IServer import IServer
from Models.AvlNode import AVLNode
from Models.Person import Person


class Server(IServer):
    def __init__(self):
        self.root = None
        self.length = 0
        self._observers = set()

    def subscribe(self, observer: IClient):
        self._observers.add(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.display()

    def insert(self, person: Person):
        self.root = self._insert_recursive(self.root, person)
        self.length += 1
        self.notify_observers()

    def update(self, person: Person):
        self._update_recursive(self.root, person)
        self.notify_observers()

    def delete(self, person: Person):
        self.root = self._delete_recursive(self.root, person)
        self.length -= 1
        self.notify_observers()

    def get_batch_entries(self, start_index: int, end_index: int, client_data=None):
        data = client_data if client_data is not None else self.sort()
        return data[start_index:end_index]

    def sort(self, column_name='Id', desc=False):
        sorted_elements = []
        self._in_order_traversal_recursive(self.root, sorted_elements, desc=desc)

        if column_name == 'Name':
            return sorted(sorted_elements, key=lambda person: person.name, reverse=desc)
        elif column_name == 'Age':
            return sorted(sorted_elements, key=lambda person: person.age, reverse=desc)
        return sorted_elements

    def get_new_id(self):
        return 1 if self.length == 0 else self.sort()[-1].id + 1

    def _insert_recursive(self, node: AVLNode, person: Person):
        if not node:
            return AVLNode(person)

        if person < node.person:
            node.left = self._insert_recursive(node.left, person)
        else:
            node.right = self._insert_recursive(node.right, person)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1:
            if person < node.left.person:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if person > node.right.person:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _update_recursive(self, node: AVLNode, person: Person):
        if not node:
            return

        if person.id < node.person.id:
            self._update_recursive(node.left, person)
        elif person.id > node.person.id:
            self._update_recursive(node.right, person)
        else:
            node.person.name = person.name
            node.person.age = person.age
            return

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1:
            if self._get_balance(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _delete_recursive(self, node: AVLNode, person: Person):
        if not node:
            return node

        if person < node.person:
            node.left = self._delete_recursive(node.left, person)
        elif person > node.person:
            node.right = self._delete_recursive(node.right, person)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            successor = self._get_min_value_node(node.right)
            node.person = successor.person
            node.right = self._delete_recursive(node.right, successor.person)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1:
            if self._get_balance(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _in_order_traversal_recursive(self, node: AVLNode, result: list, desc=False):
        if node is not None:
            if desc:
                self._in_order_traversal_recursive(node.right, result, desc=True)
                result.append(node.person)
                self._in_order_traversal_recursive(node.left, result, desc=True)
            else:
                self._in_order_traversal_recursive(node.left, result, desc=False)
                result.append(node.person)
                self._in_order_traversal_recursive(node.right, result, desc=False)

    def _rotate_left(self, z: AVLNode):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, y: AVLNode):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _get_height(self, node: AVLNode):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: AVLNode):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node: AVLNode):
        current = node
        while current.left:
            current = current.left
        return current
