
class AVLTree:
    root= None

class AVLNode:
    parent= None
    leftnode= None
    rightnode= None
    key= None
    value= None 
    bf= None
    height=None

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#__________________________________________________
# Versiones anteriores y funciones extras: 
#__________________________________________________

# Bance factor
def balanceFactor(node):

    def height(node):

        if node is None:
            return -1
        
        return (1 + max(height(node.leftnode), height(node.rightnode)))
    
    bf= height(node.leftnode) - height(node.rightnode)
    
    return bf

# Actualizar el balance factor
def update_bf(node):
    if node is not None:
        node.bf= balanceFactor(node)


#Balance (no optimizada complejidad mayor a O(n^2))
def calculate_balance_sin_optimizar(B):

    if B.root is None:
        return None
    
    def traverse(node):
        if node is not None:
            node.bf= balanceFactor(node)
            traverse(node.leftnode)
            traverse(node.rightnode)
    
    traverse(B.root)
    return B


# Cálulo de altura de los nodos: 

def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.rightnode), height(node.leftnode))


def calculate_height(B):

    if B.root is None:
        return None
    
    def traverse(node):

        if node is None:
            return None
        
        node.height= height(node)

        traverse(node.leftnode)
        traverse(node.rightnode)
    
    traverse(B.root)


def calculate_height_and_bf(B):
    if B.root is None:
        return B
    
    def traverse(node):

        if node is None:
            return -1
        
        left_height= traverse(node.leftnode)
        right_height= traverse(node.rightnode)

        node.height= 1 + max(left_height, right_height)
        node.bf= left_height - right_height

        return node.height

    traverse(B.root)
    return B

def verf(node):
    if node.height is not None:
        return node.height
    else:
        return -1


def update_node(node):
    if node is None:
        return None
    
    left_height= verf(node.leftnode)
    right_height= verf(node.rightnode)

    node.height= 1 + max(left_height, right_height)
    node.bf= left_height - right_height


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#__________________________________________________
# Ejercicio 1: 
#__________________________________________________

#Rotacion hacia la izquierda

def rotateLeft(B, avlnode):
    
    new_root= avlnode.rightnode # mi nueva raíz es el hijo derecho del node
    subtree= new_root.leftnode # guardamos subarbol izquierdo si es que tenemos


    new_root.leftnode= avlnode
    avlnode.rightnode= subtree

    if subtree is not None:
        subtree.parent= avlnode

    new_root.parent= avlnode.parent

    if avlnode.parent is not None:
        if avlnode.parent.leftnode == avlnode:
            avlnode.parent.leftnode = new_root
        else:
            avlnode.parent.rightnode = new_root
    else:
        B.root= new_root
   
    avlnode.parent= new_root 

    update_node(avlnode)
    update_node(new_root)

    return new_root



#Rotacion hacia la derecha

def rotateRight(B, avlnode):
    
    
    new_root= avlnode.leftnode # mi nueva raíz es el hijo izquierdo del node
    subtree= new_root.rightnode # guardamos subarbol derecho si es que tenemos

    
    new_root.rightnode= avlnode
    avlnode.leftnode= subtree

    if subtree is not None:
        subtree.parent= avlnode

    new_root.parent= avlnode.parent

    if avlnode.parent is not None:
        if avlnode.parent.leftnode == avlnode:
            avlnode.parent.leftnode = new_root
        else:
            avlnode.parent.rightnode = new_root
    else:
        B.root= new_root
   
    avlnode.parent= new_root 

    update_node(avlnode)
    update_node(new_root)

    return new_root

#__________________________________________________
# Ejercicio 2: 
#__________________________________________________

def calculateBalance(B):

    if B.root is None:
        return None
    
    def traverse(node):

        if node is None:
            return -1
        
        left= traverse(node.leftnode)
        right= traverse(node.rightnode)
        node.bf= left - right

        return 1 + max(left, right)
    
    traverse(B.root)
    return B


#__________________________________________________
# Ejercicio 3: 
#__________________________________________________

def reBalance(B):

    def balance(node):

        if node is None:
            return None
        
        if abs(node.bf) > 2:
            return None

        if node.bf > 1:
            if node.leftnode.bf < 0:
                rotateLeft(B, node)
                rotateRight(B, node)
            else:
                rotateRight(B, node)
        
        if node.bf < -1:
            if node.rightnode.bf > 0:
                rotateRight(B, node)
                rotateLeft(B, node)
            else:
                rotateLeft(B, node)
        
        balance(node.leftnode)
        balance(node.rightnode)

    balance(B.root)

    return B

#__________________________________________________
# Ejercicio 4: 
#__________________________________________________

def altura(node):
    if node is None:
        return -1
    return node.height

def balance(B, node):
    if node.bf > 1:  # Desbalanceado a la izquierda
        if node.leftnode.bf < 0:  # Caso Izq-Der 
            rotateLeft(B, node.leftnode)
        rotateRight(B, node)

    elif node.bf < -1:  # Desbalanceado a la derecha
        if node.rightnode.bf > 0:  # Caso Der-Izq 
            rotateRight(B, node.rightnode)
        rotateLeft(B, node)


def balanceParent(B, node):
    current = node
    while current is not None:
        # Recalcular altura y balance factor
        current.height = 1 + max(altura(current.leftnode), altura(current.rightnode))
        current.bf = altura(current.leftnode) - altura(current.rightnode)

        # Si está desbalanceado, balancear
        if abs(current.bf) > 1:
            balance(B, current)

        # Subir hacia el padre
        current = current.parent
    
def insert(B, element, key):

    newNode= AVLNode()
    newNode.value= element
    newNode.key= key
    newNode.height = 0
    newNode.bf = 0

    if B.root is None:
        B.root=newNode
        return key

    def insert_node(node):

        if key < node.key:
            if node.leftnode is None:
                node.leftnode= newNode
                newNode.parent= node
                current= newNode.parent
                balanceParent(B, current)
                return key 
            else:
                return insert_node(node.leftnode)
        else: 
            if key > node.key:
                if node.rightnode is None:
                    node.rightnode= newNode
                    newNode.parent= node
                    current= newNode.parent
                    balanceParent(B, current)
                    return key
                else:
                    return insert_node(node.rightnode)
            else: 
                return None
               
    return insert_node(B.root)

#__________________________________________________
# Ejercicio 5: 
#__________________________________________________

def delete(B, element):

    if B.root is None:
        return None
    
    def min_node(node):
        if node.leftnode is None:
            return node
        return min_node(node.leftnode)


    def delete_node(node, element):

        if node is None:
            return None

        if node.value==element:
            delete_key= node.key
            #Caso 1: Sin hijos:
            if node.leftnode is None and node.rightnode is None:
                if node.parent is not None:
                    if node.parent.leftnode==node:
                        node.parent.leftnode= None
                    else:
                        node.parent.rightnode= None
                else:
                    B.root= None

                balanceParent(B, node.parent)
                return delete_key
            else: 
                #Caso 2: Un hijo:
                if node.leftnode is None or node.rightnode is None:
                    if node.leftnode is None:
                        child= node.rightnode
                    else:
                        child=node.leftnode
                    child.parent= node.parent

                    if node.parent is not None:
                        if node.parent.leftnode==node:
                            node.parent.leftnode=child 
                        else:
                            node.parent.rightnode=child
                    else:
                        B.root=child

                    balanceParent(B, node.parent)
                    return delete_key
                else:
                    #Caso 3: Dos hijos
                    successor= min_node(node.rightnode)
                    padre= successor.parent
                    node.key= successor.key
                    node.value= successor.value
                    balanceParent(B, padre)
                    return delete_node(node.rightnode, successor.value)

        #Buscamos en el subárbol izquierdo        
        result= delete_node(node.leftnode, element)
        if result is not None:
            return result
        
        #Buscamos en el subárbol derecho
        return delete_node(node.rightnode, element)
       
    return delete_node(B.root, element)