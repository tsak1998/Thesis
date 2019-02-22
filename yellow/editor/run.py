from flask import Flask, render_template, url_for, flash, request, redirect, session,jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

app.secret_key = 'some_secret'

engine = create_engine("mysql+pymysql://root:pass@localhost:3306/thesis")

@app.route('/', methods = ["GET","POST"])
def homepage():
	
	return render_template('index.html')

@app.route('/yellow', methods = ["GET","POST"])
def post_req():
	if request.method == 'POST':
		data = request.get_json()
		
		#data : list
		# data[0] : nodes and elements
		# data[1] : sections
		# data[2] : point_loads

		df_model = pd.DataFrame(columns=['en', 'nn' 'type', 'supportType', 'nodal_load', 'nodei', 'nodej',
										 'coord_x', 'coord_y', 'coord_z', 'elem_type', 'length', 'section_id',
										 'dof_dx', 'dof_dy', 'dof_dz', 'dof_rx', 'dof_ry', 'dof_rz'])


		df_sections = pd.DataFrame(columns=['section_id', 'A', 'E', 'G',
											  'Ix', 'Iy', 'Iz'])
		#df_sections = pd.DataFrame(columns=)

		df_point_loads = pd.DataFrame(columns=['nn' , 'p_x', 'p_y', 'p_z', 'm_x', 'm_y', 'm_z'])

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


			print(sect)
			sect['user_id'] = 'cv13116'
			df = pd.DataFrame([sect], columns=sect.keys())
			df_sections = pd.concat([df_sections, df], axis =0).reset_index(drop=True)


		for d in data[2]:

			df = pd.DataFrame([d], columns=d.keys())
			df_point_loads = pd.concat([df_point_loads, df], axis =0).reset_index(drop=True)




		nodes = df_model.loc[df_model['type']=='node'].dropna(axis=0, how='all')
		elements = df_model.loc[df_model['type']=='element'].dropna(axis=0, how='all')
		nodes = nodes.dropna(axis=1, how='all')
		elements = elements.dropna(axis=1, how='all')

		nodes = nodes.sort_values('nn', axis=0)
		elements = elements.sort_values('en', axis=0)

		print(nodes.to_string())
		print('\n')
		print(elements.to_string())
		print('\n')
		print(df_sections.to_string())
		print('\n')
		print(nodes.nn)
		print('\n')
		print(df_point_loads.to_string())

		del elements['type']
		elements['user_id'] = 'cv13116'
		df_point_loads['user_id'] = 'cv13116'

		del nodes['type'], nodes['supportType']
		nodes['user_id'] = 'cv13116'


		elements.to_sql('elements', engine, schema='thesis', if_exists='append', index=False, index_label=None, chunksize=None, dtype=None)
		df_point_loads.to_sql('loads_nodal', engine, schema='thesis', if_exists='append', index=False, index_label=None, chunksize=None, dtype=None)
		nodes.to_sql('nodes', engine, schema='thesis', if_exists='append', index=False, index_label=None, chunksize=None, dtype=None)
		df_sections.to_sql('sections', engine, schema='thesis', if_exists='append', index=False, index_label=None, chunksize=None, dtype=None)


	return render_template('index.html')

if __name__=="__main__":
	app.run(debug="TRUE")

'''
from flask import Flask, render_template, url_for, flash, request, redirect, session,jsonify
import pandas as pd

app = Flask(__name__)

app.secret_key = 'some_secret'

@app.route('/', methods = ["GET","POST"])
def homepage():
	
	return render_template('index.html')

@app.route('/yellow', methods = ["GET","POST"])
def post_req():
	if request.method == 'POST':
		data =  request.get_json(force = True)
		print('yellow')
		print(data)
		#data_model = data['model']
		#data_sections = data['sections']
		#data = dict(data)
		#print(data['userData'])
		#df_elements = pd.DataFrame(columns=['id', 'type'])
		df_model = pd.DataFrame(columns=['id', 'type', 'supportType', 'nodal_load', 'node_i', 'node_j',
										 'x', 'y', 'z', 'elem_type', 'length', 'section_id'])

		df_sections = pd.DataFrame(columns=['section_id', 'sect_mat', 'sect_type',
											 'h', 'b', 'h1', 'b1'])
		#df_sections = pd.DataFrame(columns=)
		for d in data_model:
			df = pd.DataFrame([d['object']['userData']], columns=d['object']['userData'].keys())
			df_model = pd.concat([df_model, df], axis =0).reset_index(drop=True)

			
			if (d['object']['userData']['type']=='node'):
				df  = pd.DataFrame([d['object']['userData']], columns=d['object']['userData'].keys())
				df_nodes = pd.concat([df_nodes, df], axis =0).reset_index(drop=True)
			elif (d['object']['userData']['type']=='element'):

				df1  = pd.DataFrame([d['object']['userData']], columns=d['object']['userData'].keys())
				df_elements = pd.concat([df_nodes, df1], axis =0).reset_index(drop=True)
			
		#print(df_elements)

		nodes = df_model.loc[df_model['type']=='node'].dropna(axis=0, how='all')
		elements = df_model.loc[df_model['type']=='element'].dropna(axis=0, how='all')
		nodes = nodes.dropna(axis=1, how='all')
		elements = elements.dropna(axis=1, how='all')

		print(nodes)
		print(elements.to_string())
	


	return render_template('index.html')

if __name__=="__main__":
	app.run(debug="TRUE")

'''
