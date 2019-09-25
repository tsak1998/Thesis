import pandas as pd
from section_properties import section_properties


def parser(user_id, data, engine):
    # data contains dicts of elements, labels, loads and sections
    elements = pd.DataFrame(data[0])
    elements['user_id'] = user_id
    del elements['type'], elements['label_position'], elements['xLocal'], elements['yLocal'], elements['zLocal']
    nodes = pd.DataFrame(data[1])
    nodes['user_id'] = user_id
    del nodes['type'], nodes['label_position']
    sections = pd.DataFrame(data[3])
    #sections.columns = ['section_id', 'material', 'type', 'dimensions', 'A', 'Ix', 'Iy', 'Iz']
    sections['user_id'] = user_id
    sections['section_id'] = sections['id']
    sections = sections.rename(columns={'Material Id': 'material'})
    materials = pd.DataFrame(data[4], columns = ['material_id', 'E', 'G', 'n'])
    materials['user_id'] = user_id
    materials = materials.rename(columns={'id': 'material_id'})
    # for loads and sections data needs to be created
    # because computations take as argouments loads: P = [px,py,pz,mx,my,mz]
    # loads have to be parsed and saved in this structure

    point_loads = pd.DataFrame(columns=['user_id', 'nn', 'c', 'p_x', 'p_y', 'p_z', 'm_x', 'm_y', 'm_z'])

    temp_loads = pd.DataFrame(data[2])
    temp_loads_group = temp_loads.groupby(['nn', 'c'])
    for t in temp_loads_group:
        nn = t[0][0]
        c = t[0][1]
        p_x, p_y, p_z, m_x, m_y, m_z = 0, 0, 0, 0, 0, 0
        for index, load in t[1].iterrows():
            if load.type == 'p_load':
                if load.direction == 'x':
                    p_x += load.value
                elif load.direction == 'y':
                    p_y += load.value
                else:
                    p_z += load.value
            else:
                if load.direction == 'x':
                    m_x += load.value
                elif load.direction == 'y':
                    m_y += load.value
                else:
                    m_z += load.value
        temp_load = {'nn': load.nn, 'c': load.c, 'p_x': p_x, 'p_y': p_y, 'p_z': p_z, 'm_x': m_x, 'm_y': m_y, 'm_z': m_z}
        df = pd.DataFrame([temp_load], columns=temp_load.keys())
        point_loads = pd.concat([point_loads, df], axis=0).reset_index(drop=True)

    point_loads['user_id'] = user_id
    d_loads = pd.DataFrame(data[5])
    d_loads['user_id'] = user_id

    elements.rename(columns={'en': 'number'}, inplace=True)
    nodes.rename(columns={'nn': 'number'}, inplace=True)
    point_loads.rename(columns={'nn': 'number'}, inplace=True)
    #materials.rename(columns={'en': 'number'}, inplace=True)
    d_loads.rename(columns={'en': 'number'}, inplace=True)
    # sections
    # the data provided is the material and the section geometry
    # for steel sections A, Ix, Iy, Iz will be taken from the database
    # for concrete  will be calculated
    # group the sections by material
    # temp_sections = pd.DataFrame(data[3])
    #steel_sections = temp_sections.loc[temp_sections['material'] == 'stl']
    # concrete_sections = temp_sections.loc[temp_sections['material'] == 'con']
    #concrete_sections = section_properties(concrete_sections, user_id, engine)
    # need the library


    return elements, nodes, point_loads, sections, materials, d_loads
