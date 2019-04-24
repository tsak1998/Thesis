def dxf_import(dxf):

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
    
    nd = pd.DataFrame(NDS)
    nd.columns = ['x', 'z', 'y']
    #nd.sort_values(by=['y', 'x', 'z'], ascending=True, na_position='first', inplace=True)
    #for i in range(nd.shape[0]):
    #    cnt = 0
    #    nd.rename(index={i:str(cnt)}, inplace=True)
    #    cnt +=1
    elm = pd.DataFrame(ELMS)
    elm.columns = ['i', 'j']
    #elm.sort_values(by='i', ascending=True, na_position='first', inplace=True)
    #for i in range(elm.shape[0]):
    #    elm.rename(index={i:i}, inplace=True)
    #print('look:')
    #print(nd)
    #print(elm)

    return nd, elm

