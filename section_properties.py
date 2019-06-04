# calculates A, Ix, Iy, Iz properties for 
# rect, T, L 
import pandas as pd
from sqlalchemy import create_engine

def section_properties(concrete_sections, user_id, engine):
    df_sections = pd.DataFrame(columns=['section_id', 'A', 'E', 'G',
										'Ix', 'Iy', 'Iz'])
    for index, d in concrete_sections.iterrows():
        sect = {}
        sect['section_id'] = d['section_id']
        mat = pd.read_sql("SELECT E,G from materials WHERE material_category='" + d.material_category + "'", engine)
        sect['sect_type'] = d.sect_type
        sect['material'] = d.material_category
        v = 0.2
        E = mat.E.get_values()[0]
        G = mat.G.get_values()[0]
        # 
        if (d['sect_type']=='rect'):

            h = float(d['h'])
            b = float(d['b'])

            sect['A'] = h*b
            sect['E'] = E
            sect['G'] = G

            sect['Ix'] = h*b**3/12
            sect['Iy'] = b*h**3/12
            sect['Iz'] = h*b**3*(1/3-0.21*(b/h)*(1-b**4/(12*h**4)))
        elif (d['sect_type']=='T'):
            H = float(d['h'])
            B = float(d['b'])
            h = float(d['h1'])
            b = float(d['b1'])
            sect['A'] = B*h + H*b
            xc = B/2
            yc =  ((H+h/2)*h*B+H**2*b/2)/sect['A']

            sect['E'] = E
            sect['G'] = G

            sect['Ix'] = b*H*(yc-H/2)*2 + b*H**3/12 + h*B*(H + h/2 - yc)*2 + h**3*B/12
            sect['Iy'] = b**3*H/12 + B**3*h/12

            ix1 = h*B**3*(1/3-0.21*(B/h)*(1-B**4/(12*h**4)))
            ix2 = H*b**3*(1/3-0.21*(b/H)*(1-b**4/(12*H**4)))
            sect['Iz'] = ix1 + ix2
        

    
    sect['user_id'] = user_id 
    sections = pd.DataFrame([sect], columns=sect.keys())
    # sections = pd.concat([df_sections, df], axis =0).reset_index(drop=True)
    return sections