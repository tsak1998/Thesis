def dxf_import(dxf):
    import pandas as pd
    import time
    import math
    t1 = time.time()
    # DXFin: Read lines from DXF and returns two LISTs: NDS[X,Y,Z] & ELMS[NDSi,NDSj]

    # Read lines and store them into LIST all_lines
    all_lines = [entity for entity in dxf.entities if entity.dxftype == 'LINE']

    # Set the precision to prcs
    prcs = 10

    # Store coordinates (precision prcs) of start & end of each line into the LIST NODES
    NODES = []
    ELMS = []
    NODES.append(
        (round(all_lines[0].start[0], prcs), round(all_lines[0].start[1], prcs), round(all_lines[0].start[2], prcs)))
    NODES.append((round(all_lines[0].end[0], prcs), round(all_lines[0].end[1], prcs), round(all_lines[0].end[2], prcs)))

    for line in all_lines:
        nodei = (round(line.start[0], prcs), round(line.start[1], prcs), round(line.start[2], prcs))
        nodej = (round(line.end[0], prcs), round(line.end[1], prcs), round(line.end[2], prcs))
        try:
            i = NODES.index(nodei) + 1
        except:
            NODES.append(nodei)
            i = len(NODES)

        try:
            j = NODES.index(nodej) + 1
        except:
            NODES.append(nodej)
            j = len(NODES)
        ELMS.append((i, j))

    nd = pd.DataFrame(NODES)
    nd.columns = ['coord_x', 'coord_y', 'coord_z']
    nd['id'] = nd.index + 1
    nd['nn'] = nd.index + 1
    nd['dof_dx'], nd['dof_dy'], nd['dof_dz'] = 1, 1, 1
    nd['dof_rx'], nd['dof_ry'], nd['dof_rz'] = 1, 1, 1

    elm = pd.DataFrame(ELMS)
    elm.columns = ['nodei', 'nodej']
    elm['id'] = elm.index + 1
    elm['en'] = elm.index + 1
    elm['section_id'] = 1
    elm['elem_type'] = 'beam'
    elm['length'] = 1

    # elm.sort_values(by='i', ascending=True, na_position='first', inplace=True)
    # for i in range(elm.shape[0]):
    #    elm.rename(index={i:i}, inplace=True)
    # print('look:')
    # print(nd)
    # print(elm)
    print('DXF', time.time() - t1)
    print(elm)
    return nd, elm


'''
import pandas as pd

# DXFin: Read lines from DXF and returns two LISTs: NDS[X,Y,Z] & ELMS[NDSi,NDSj]

# Read lines and store them into LIST all_lines
all_lines = [entity for entity in dxf.entities if entity.dxftype == 'LINE']

# Set the precision to prcs
prcs=4

# Store coordinates (precision prcs) of start & end of each line into the LIST NODES
NODES=[]
for line in all_lines:
    NODES.append([round(line.start[0], prcs),round(line.start[1], prcs),round(line.start[2], prcs)])
    NODES.append([round(line.end[0], prcs),round(line.end[1], prcs),round(line.end[2], prcs)])

# Store unique coordinates of LIST NODES into LIST NDS
NDS=[]
[NDS.append(x) for x in NODES if x not in NDS]

# Store index from NDS of start & end node for each line into the LIST ELMS
ELMS=[]
for line in all_lines:
    ndi=[round(line.start[0], prcs),round(line.start[1], prcs),round(line.start[2], prcs)]
    ndj=[round(line.end[0], prcs),round(line.end[1], prcs),round(line.end[2], prcs)]
    ELMS.append([NDS.index(ndi),NDS.index(ndj)])
'''
