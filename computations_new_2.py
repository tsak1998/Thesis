from nodes import *

t_nodes = time()
nodes = session.query(Nodes).all()
#nodes = {node.nn: node for node in nodes}

session.query(Materials).all()

session.query(Sections).all()

session.query(Elements).all()

session.query(PointLoads).all()

print('querying : ', time() - t_nodes)
print('whole: ', time() - t1)
