# This is a funny brain-exercised game:
# get four cards from poke, which in range
# of A to 10 (A represents 1 here).
# Then try to figure out how to combine 
# these four numbers into a specific number
# (24 here) with only + - * / operations.
# And all of four numbers must be involved 
# and only for once.
import sys

CombineInto = 24

def full_arrangement(array):
    if len(array) == 2:
        if array[0] == array[1]:
            yield array
        else:
            yield array
            yield [array[1], array[0]]
        return
    
    presence = []
    for i in range(len(array)):
        if array[i] in presence:
            continue
        presence.append(array[i])
        for part_array in full_arrangement(array[:i] + array[i+1:]):
            new_array = [array[i]] + part_array
            yield new_array

def _op(op_id, x, y):
    if op_id == 0:
        return x + y
    elif op_id == 1:
        if x - y >= 0:
            return x - y
        else:
            return None
        return x - y
    elif op_id == 2:
        return x * y
    elif op_id == 3:
        if y == 0:
            return None
        if x % y == 0:
            return x // y
        else:
            return None

def enum_op():
    for i in range(4):
        for j in range(4):
            for k in range(4):
                yield (i, j, k)

def transform(op_id):
    str_op = ['+', '-', '×', '÷']
    return str_op[op_id]

def display(state, array, op_id):
    if state == 1:
        node1 = _op(op_id[0], array[0], array[1])
        node2 = _op(op_id[1], array[2], array[3])
        print("%d %s %d -> %d" % (array[0], transform(op_id[0]), array[1], node1))
        print("%d %s %d -> %d" % (array[2], transform(op_id[1]), array[3], node2))
        print("%d %s %d -> %d" % (node1, transform(op_id[2]), node2, CombineInto))
    elif state == 2:
        node1 = _op(op_id[0], array[0], array[1])
        node2 = _op(op_id[1], node1, array[2])
        print("%d %s %d -> %d" % (array[0], transform(op_id[0]), array[1], node1))
        print("%d %s %d -> %d" % (node1, transform(op_id[1]), array[2], node2))
        print("%d %s %d -> %d" % (node2, transform(op_id[2]), array[3], CombineInto))
    else:
        raise NotImplementedError
        

def main(numbers):
    assert len(numbers) == 4
    for array in full_arrangement(numbers):
        # state1
        for idx_i, idx_j, idx_k in enum_op():
            node1 = _op(idx_i, array[0], array[1])
            if node1 is None:
                continue

            node2 = _op(idx_j, array[2], array[3])
            if node2 is None:
                continue
            
            node3 = _op(idx_k, node1, node2)
            if node3 is None:
                continue
            elif node3 == CombineInto:
                display(1, array, [idx_i, idx_j, idx_k])
                return
        
        # state2
        for idx_i, idx_j, idx_k in enum_op():
            node1 = _op(idx_i, array[0], array[1])
            if node1 is None:
                continue

            node2 = _op(idx_j, node1, array[2])
            if node2 is None:
                continue

            node3 = _op(idx_k, node2, array[3])
            if node3 is None:
                continue
            elif node3 == CombineInto:
                display(2, array, [idx_i, idx_j, idx_k])
                return
    print("组合%s没有找到解法" % str(numbers))

if __name__ == "__main__":

    assert len(sys.argv[1:]) == 4
    array = [int(x) for x in sys.argv[1:]]
    main(array)