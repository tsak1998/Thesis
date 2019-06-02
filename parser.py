import pandas as pd
from sqlalchemy import create_engine
from createdb import createDB
from section_properties import section_properties

def parse_and_save(user_id, data):
	engine = create_engine("mysql+pymysql://root:password@localhost:3306/yellow")  
	# data contains dicts of elements, labels, loads and sections
	elements = pd.DataFrame(data[0])
	elements['user_id'] = user_id
	del elements['type']
	nodes = pd.DataFrame(data[1])
	nodes['user_id'] =user_id
	del nodes['type']
	# for loads and sections data needs to be created
	# because computations take as argouments loads: P = [px,py,pz,mx,my,mz]
	# loads have to be parsed and saved in this structure
	point_loads = pd.DataFrame(columns=['user_id', 'nn', 'c', 'p_x', 'p_y', 'p_z', 'm_x', 'm_y', 'm_z'])
	temp_loads = pd.DataFrame(data[2])
	for index, load in temp_loads.iterrows():	
		if load.type == 'p_load':
			if load.direction=='x':
				p = [load.value, 0, 0, 0, 0, 0]
			elif load.direction=='y':
				p = [0 ,load.value ,0 ,0, 0, 0]
			else:
				p = [0, 0, load.value, 0, 0, 0]
		else:
			if load.direction=='x':
				p = [0, 0, 0, load.value, 0, 0]
			elif load.direction=='y':
				p = [0 ,0 ,0 ,0, load.value, 0]
			else:
				p = [0, 0, 0, 0, 0, load.value]
		temp_load = {'nn' : load.nn , 'c': load.c, 'p_x': p[0],
					'p_y': p[1], 'p_z': p[2], 'm_x': p[3], 'm_y': p[4], 'm_z': p[5]}
		df = pd.DataFrame([temp_load], columns=temp_load.keys())
		point_loads = pd.concat([point_loads, df], axis =0).reset_index(drop=True)
	point_loads['user_id'] = user_id
	# sections
	# the data provided is the material and the section geometry
	# for steel sections A, Ix, Iy, Iz will be taken from the database
	# for concrete  will be calculated
	# group the sections by material
	temp_sections = pd.DataFrame(data[3])
	steel_sections = temp_sections.loc[temp_sections['material']=='stl']
	concrete_sections = temp_sections.loc[temp_sections['material']=='con']
	concrete_sections = section_properties(concrete_sections, user_id)
	# need the library
	df_steel_sections = pd.DataFrame(columns=['section_id', 'A', 'E', 'G',
										'Ix', 'Iy', 'Iz'])
	for index, section in steel_sections.iterrows():
		engine = create_engine('mysql+pymysql://root:password@localhost/yellow')
		sect = pd.read_sql("SELECT A,Ix,Iy,Iz from steel_sections WHERE sect_type='" + section.sect_type + "'", engine)
		mat = pd.read_sql("SELECT E,G from materials WHERE material_category='" + section.material_category + "'", engine)
		sect['user_id'] = user_id
		sect['section_id'] = section['section_id']
		temp_sect = pd.concat([sect, mat], axis=1)
	sections = pd.concat([temp_sect, concrete_sections], axis=0)
	
	createDB(user_id, elements=elements, nodes=nodes, point_loads=point_loads, sections=sections)

	
'''
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

for d in data[1]['sections']:
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


sect['user_id'] = user_id 
df = pd.DataFrame([sect], columns=sect.keys())
df_sections = pd.concat([df_sections, df], axis =0).reset_index(drop=True)

nodes = df_model.loc[df_model['type']=='node'].dropna(axis=0, how='all')
elements = df_model.loc[df_model['type']=='element'].dropna(axis=0, how='all')
nodes = nodes.dropna(axis=1, how='all')
elements = elements.dropna(axis=1, how='all')

nodes = nodes.sort_values('nn', axis=0).reset_index(drop=True)
elements = elements.sort_values('en', axis=0).reset_index(drop=True)

del elements['type']
elements['user_id'] = user_id

elements['id'] = elements.index + 1
elements = elements[elem_cols]
df_point_loads['user_id'] = user_id
del elements['id']

del nodes['type'], nodes['supportType']
nodes['user_id'] = user_id
# nodes['id'] = nodes.index+1

createDB(user_id, elements=elements, nodes=nodes, point_loads=df_point_loads, sections=df_sections)

'''