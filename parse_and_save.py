import pandas as pd
from sqlalchemy import create_engine
from createdb import createDB

def parse_and_save(proj_code, data):
	#engine = create_engine('mysql+pymysql://bucketuser:dencopc@localhost/bucketlist')
	engine = create_engine("mysql+pymysql://root:password@localhost:3306/_0000125")


	df_model = pd.DataFrame(columns=['en', 'nn' 'type', 'supportType', 'nodal_load', 'nodei', 'nodej',
									 'coord_x', 'coord_y', 'coord_z', 'elem_type', 'length', 'section_id',
									 'dof_dx', 'dof_dy', 'dof_dz', 'dof_rx', 'dof_ry', 'dof_rz'])
	elem_cols = ['id', 'user_id', 'en', 'nodei', 'nodej', 'length', 'elem_type', 'section_id']
	df_sections = pd.DataFrame(columns=['section_id', 'A', 'E', 'G',
										  'Ix', 'Iy', 'Iz'])

	df_point_loads = pd.DataFrame(columns=['nn', 'p_x', 'p_y', 'p_z', 'm_x', 'm_y', 'm_z'])

	for d in data[0]:
		df = pd.DataFrame([d['object']['userData']], columns=d['object']['userData'].keys())
		df_model = pd.concat([df_model, df], axis =0).reset_index(drop=True)

	for d in data[1]:
		#df_dict = pd.DataFrame([d], columns=d.keys())
		#moment of inertia for the RC sections
		sect = {}
		sect['section_id'] = d['section_id']
		if (d['sect_type']=='rect'):

			h = float(d['h'])
			b = float(d['b'])

			sect['A'] = h*b
			sect['E'] = 20000
			v = 0.2
			sect['G'] = sect['E']/2*(1+v)

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

			sect['E'] = 20000
			v = 0.2
			sect['G'] = sect['E']/2*(1+v)

			sect['Ix'] = b*H*(yc-H/2)*2 + b*H**3/12 + h*B*(H + h/2 - yc)*2 + h**3*B/12
			sect['Iy'] = b**3*H/12 + B**3*h/12

			ix1 = h*B**3*(1/3-0.21*(B/h)*(1-B**4/(12*h**4)))
			ix2 = H*b**3*(1/3-0.21*(b/H)*(1-b**4/(12*H**4)))
			sect['Iz'] = ix1 + ix2
		elif (d['sect_type']=='hea200'):
			sect['A'] = 0.00438
			sect['E'] = 210000
			v = 0.3
			sect['G'] = sect['E']/2*(1+v)

			sect['Ix'] = 3.69*10**-6
			sect['Iy'] = 1.34*10**-5
			sect['Iz'] = 0.149*10**-6


	sect['user_id'] = 'cv13116'
	df = pd.DataFrame([sect], columns=sect.keys())
	df_sections = pd.concat([df_sections, df], axis =0).reset_index(drop=True)

	nodes = df_model.loc[df_model['type']=='node'].dropna(axis=0, how='all')
	elements = df_model.loc[df_model['type']=='element'].dropna(axis=0, how='all')
	nodes = nodes.dropna(axis=1, how='all')
	elements = elements.dropna(axis=1, how='all')

	nodes = nodes.sort_values('nn', axis=0).reset_index(drop=True)
	elements = elements.sort_values('en', axis=0).reset_index(drop=True)

	del elements['type']
	elements['user_id'] = 'cv13116'

	elements['id'] = elements.index + 1
	elements = elements[elem_cols]
	df_point_loads['user_id'] = 'cv13116'
	print(elements, nodes)

	del nodes['type'], nodes['supportType']
	nodes['user_id'] = 'cv13116'
	nodes['id'] = nodes.index+1

	createDB(proj_code, elements=elements, nodes=nodes, loads_nodal=df_point_loads, sections=df_sections)

	