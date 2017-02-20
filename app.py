from flask import *
##from flask.ext.login import LoginManager
from models.model import *
from models.user import *


app = Flask (__name__, template_folder = 'views', static_folder = 'statics')
##login_manager = LoginManager()
usuario_activo = None

@app.route('/')
def index_anon():
	return render_template('inicio_pasties_anonimo.html')

@app.route('/index')
def index():
	global usuario_activo
	model = Model()
	pasties = model.pasties()
	owners = model.owners()
	hashtags = model.hashtags()
	count = model.count()
	print 'epa aqui-----'
	print hashtags
	hashtags = model.fix_own(hashtags)
	print 'los modifique y recibi esto ----'
	print hashtags
	return render_template('index.html', usuario_activo=usuario_activo, max=count, hashtags=hashtags, pasties=pasties, owners=owners)  

@app.route('/iindex', methods=['POST'])
def iindex():
  model = Model()
  user = request.form['user']
  passwd = request.form['pass']
  if model.access(user,passwd)==False:
    return render_template('iniciar_sesion.html', ok = 0)
  else:
    new_user = User(user)
    session['logged_in'] = new_user.name
    global usuario_activo
    usuario_activo = new_user
    pasties = model.pasties()
    owners = model.owners()
    hashtags = model.hashtags()
    count = model.count()
    print 'epa aquii-----'
    print hashtags
    hashtags = model.fix_own(hashtags)
    print hashtags
    print count
    return render_template('index.html', usuario_activo=new_user, max=count, hashtags=hashtags, pasties=pasties, owners=owners)

@app.route('/busqueda_anonimo', methods=['POST'])
def busqueda_anonimo():
  model = Model()
  buscar= request.form['buscar']
  if model.verificar_hashtags(buscar):
  	owners=model.search_owner(buscar,'anonimo','anonimo')
  	print"-------------OWNERS.........."
  	print owners
  	times=model.search_time(buscar,'anonimo','anonimo')
  	print"-------------TIMES.........."
  	print times
  	titles=model.search_title(buscar,'anonimo','anonimo')
  	print"-------------TITLES.........."
  	print titles
  	contents=model.search_content(buscar,'anonimo','anonimo')
  	print"-------------CONTENTS.........."
  	print contents
  	##hashtags=model.search_hashtags(buscar,'anonimo','anonimo')
  	##print"-------------HASHTAGS.........."
  	##print hashtags
  	return render_template('busqueda_anonimo.html',usuario_activo=usuario_activo,ok=1,owners=owners,times=times,titles=titles, contents=contents)
  else:
  	return render_template('busqueda_anonimo.html',usuario_activo=usuario_activo,ok=0)

@app.route('/busqueda_registrado', methods=['POST'])
def busqueda_registrado():
  model = Model()
  global usuario_activo
  buscar= request.form['buscar']
  pasties = model.buscar_pasties(buscar,usuario_activo.name )
  owners = model.buscar_owners(buscar,usuario_activo.name)
  hashtags = model.buscar_hashtags(buscar)
  hashtags = model.fix_own(hashtags)
  max = model.busqueda_contar(buscar,usuario_activo.name)
  return render_template('busqueda_registrado.html', usuario_activo=usuario_activo, pasties=pasties, owners=owners, hashtags=hastags, max=max)

@app.route('/cambiar_contrasena')
def cambiar_contrasena():
	global usuario_activo
	return render_template('cambiar_contrasena.html', usuario_activo=usuario_activo)

@app.route('/change_pass',methods=['POST'])
def change_pass():
	global usuario_activo
	model = Model()
	pass_act=request.form['pass_actual']
	pass_nva=request.form['pass_nueva']
	pass_verif=request.form['pass_verif']
	if model.cambio_pass(pass_act, pass_nva, pass_verif,usuario_activo.name) == 1:
		return index()
	if model.cambio_pass(pass_act, pass_nva, pass_verif,usuario_activo.name) == 2:
		return render_template('cambiar_contrasena.html',ok=2, usuario_activo=usuario_activo)
	if model.cambio_pass(pass_act, pass_nva, pass_verif,usuario_activo.name) == 3:
		return render_template('cambiar_contrasena.html',ok=3, usuario_activo=usuario_activo)


@app.route('/logout')
def logout():
  global player 
  player = None
  session.pop('logged_in', None)
  return render_template('inicio_pasties_anonimo.html')
  
@app.route('/categorias')
def categorias():
	return render_template('categorias.html')

@app.route('/categorias_registrado')
def categorias_registrado():
	return render_template('categorias_registrado.html')

@app.route('/crear_pastie_registrado')
def crear_pastie_registrado():
	return render_template('crear_pastie_registrado.html')

@app.route('/guardar_pastie', methods=['POST'])
def guardar_pastie():
	model = Model()
	global usuario_activo
	title = request.form['title']
	content=request.form['content']
	hashtag=request.form['hashtag']
	privacidad=request.form['privacidad']
	if model.createPastie(title,content,hashtag,privacidad,usuario_activo.name):
		pasties = model.pasties()
		owners = model.owners()
		hashtags = model.hashtags()
		count = model.count()
		hashtags = model.fix_own(hashtags)
		return render_template('index.html', usuario_activo=usuario_activo, max=count, hashtags=hashtags, pasties=pasties, owners=owners)
	else:
		return render_template('crear_pastie_registrado.html',usuario_activo=usuario_activo,ok=0)

@app.route('/eliminar')
def eliminar():
	global usuario_activo
	owner = usuario_activo.name
	model = Model()
	pasties = model.own_pasties(owner)
	hashtags = model.own_hashtags(owner)
	count = model.own_count(owner)
	hashtags = model.fix_own(hashtags)
	print hashtags
	if hashtags[0] == '#NoTienesPasties':
		print 'creare el vacio'
		return render_template('eliminar_pastie.html', empty=1)
	return render_template('eliminar_pastie.html', usuario_activo=usuario_activo, max=count, hashtags=hashtags, pasties=pasties, owner=owner)

@app.route('/remove', methods=['POST'])
def remove():
	model = Model()
	id_remove = request.form['id_remove']
	print 'llegue a eliminar xD'
	if model.remove(id_remove):
		return eliminar()
	else:
		print 'no lo elimine'
		return eliminar()

@app.route('/login')
def login():
	return render_template('iniciar_sesion.html')

@app.route('/lista_editar')
def editar_lista():
	global usuario_activo
	owner = usuario_activo.name
	model = Model()
	pasties = model.own_pasties(owner)
	hashtags = model.own_hashtags(owner)
	count = model.own_count(owner)
	hashtags = model.fix_own(hashtags)
	if hashtags[0] == '#NoTienesPasties':
		print 'creare el vacio'
		return render_template('eliminar_pastie.html', empty=1)
	return render_template('lista_modificar_pastie.html', usuario_activo=usuario_activo, max=count, hashtags=hashtags, pasties=pasties, owner=owner)

@app.route('/editar', methods=['POST'])
def editar():
	model = Model()
	id_edit = request.form['id_edit']
	pastie = model.pastie_edit(id_edit)
	categorias = model.categorias_edit(id_edit)
	print 'categoras pa editar'
	print categorias
	return render_template('modificar_pastie.html', pastie=pastie, categorias=categorias)

@app.route('/edit', methods=['POST'])
def edit():
	model = Model()
	id_edit = request.form['id_edit']
	title = request.form['title']
	content = request.form['contenido']
	categorias = request.form['categorias']
	privacidad = request.form['privacidad']
	if model.edit(id_edit, title, content, categorias, privacidad):
		return editar_lista()
	else:
		print "ENTRO AL ELSE DEL EDIT"
		return editar_lista()

@app.route('/perfil')
def perfil():
  if 'logged_in' in session:
    global usuario_activo
    print ' editare perfil, '
    print usuario_activo.name
    return render_template('modificar_perfil.html', dia=31,mes=12,ano=1950, usuario_activo=usuario_activo)

@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():
	  if 'logged_in' in session:
	  	print 'tengo que modificar el perfil de '
	  	global usuario_activo
	  	print usuario_activo.name
	  	model = Model()
	  	nombres = request.form['nombres']
	  	apellidos = request.form['apellidos']
	  	dia = request.form['dia']
	  	mes = request.form['mes']
	  	ano = request.form['ano']
	  	correo = request.form['correo']
	  	pass1 = request.form['pass1']
	  	pais = request.form['pais']
	  	ciudad = request.form['ciudad']
	  	telefono = request.form['telefono']
	  	if model.edit_profile(usuario_activo.name,nombres,apellidos,dia,mes,ano,correo,pass1,pais,ciudad,telefono):
	  		pasties = model.pasties()
	  		owners = model.owners()
	  		hashtags = model.hashtags()
	  		count = model.count()
	  		hashtags = model.fix_own(hashtags)
	  		return render_template('index.html', usuario_activo=usuario_activo, max=count, hashtags=hashtags, pasties=pasties, owners=owners)
	  	return render_template('modificar_perfil.html',ok=0,dia=31,mes=12,ano=1950, usuario_activo=usuario_activo)

@app.route('/profile')
def profile():
	return render_template('perfil.html')

@app.route('/user')
def usuario():
	return render_template('perfil_otro_usuario.html')

@app.route('/recuperar_pass')
def getpass():
	return render_template('recuperar_contrasena.html')

@app.route('/registro', methods = ['POST'])
def registro():
	model = Model()
	user = request.form['user']
	mail = request.form['mail']
	passwd = request.form['password']
	if model.registro(user,mail,passwd):
		new_user = User(user)
		session['logged_in'] = new_user.name
		global usuario_activo
		usuario_activo = new_user
		pasties = model.pasties()
    	owners = model.owners()
    	hashtags = model.hashtags()
    	count = model.count()
    	hashtags = model.fix_own(hashtags)
    	return render_template('index.html', usuario_activo=new_user, max=count, hashtags=hashtags, pasties=pasties, owners=owners)
   	return render_template('iniciar_sesion.html')


@app.route('/proc_pass', methods =['POST'])
def proc_pass():
  user = request.form['user']
  model = Model()
  if model.recuperar_pass(name=user):
    return render_template('iniciar_sesion.html', ok = 1)
  else:
    print 'Correo no existe'
    return render_template('recuperar_contrasena.html', ok = 0)

if __name__ == '__main__':
  app.secret_key = 'atiaccladr'
  app.config['SESSION_TYPE'] = 'filesystem'
  ##login_manager.init_app(app)
  app.debug = True
  app.run( host = '0.0.0.0', port = 5000 )
