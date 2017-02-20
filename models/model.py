from flask import *
import datetime 
import psycopg2
import smtplib
import random


class Model:
  def __init__(self):
    pass

  def recuperar_pass(self, name=None):

    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pw_length = 12
    provicional = ""

    if name:
      connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
      query = connection.cursor()
      query.execute('select email from users where name_usuario=%s', (name,))
      result = query.fetchone()
      print result
      if result:
        
        gmail_user = 'atiacc2014@gmail.com'
        gmail_pwd = 'atiaccladr'
        FROM = 'atiacc2014@gmail.com'
        TO = result[0]
        SUBJECT = "Contrasena provisional"
        
        for i in range(pw_length):
          next_index = random.randrange(len(alphabet))
          provicional = provicional + alphabet[next_index]
        
        for i in range(random.randrange(1,3)):
          replace_index = random.randrange(len(provicional)//2)
          provicional = provicional[0:replace_index] + str(random.randrange(10)) + provicional[replace_index+1:]
        TEXT = "Tu contrasena provisional es " + provicional 

        query.execute('update users set password=%s where name_usuario=%s', (provicional,name,))
        query.execute('select password from users where name_usuario=%s', (name,))
        connection.commit()
        new_pass = query.fetchone()
        print new_pass

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com:465') #or port 465 doesn't seem to work!
        
        server.ehlo()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.quit()
        print 'successfully sent the mail'
        query.close()
        connection.close()
        return True                                                                                                                                                                                                                                                                     
      else:
        print 'Enviare false'
        query.close()
        connection.close()
        return False

  def registro(self, user=None, mail=None, password=None):
    null = None
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from users where name_usuario=%s', (user,))
    result = query.fetchone()
    if result:
      return False
    query.execute('select * from users where email=%s', (mail,))
    result = query.fetchone()
    if result: 
      return False
    else:
      query.execute('select count(id_p) from users')
      result = query.fetchone()
      new_id = int(result[0] + 1)
      print new_id
      query.execute('insert into users (id_p,name_usuario,email,password,nombres,apellidos,fecha_nac,pais,ciudad,telefono) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (new_id, user, mail, password, null, null, null, null, null, null,))
      connection.commit()
      print 'user added'
      query.close()
      connection.close()
      return True

  def access(self,user=None,passwd=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select count(name_usuario) from users where name_usuario=%s and password=%s', (user,passwd,))
    result = query.fetchone()
    print result[0]
    if result[0]==1:
      return user
    return False

  #MEJORAR VALORES DE RETORNO
  def edit_profile (self, user_to_edit=None, nombres=None, apellidos=None, dia=None, mes=None, ano=None, correo=None, pass1=None, pais=None, ciudad=None, telefono=None, user_act=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from users where name_usuario=%s', (user_to_edit,))
    row = query.fetchone()
    fecha_nac = dia + "/" + mes + "/" + ano
    query.execute('select count(email) from users where email=%s and name_usuario<>%s', (correo,user_to_edit,))
    ver_email = query.fetchone()
    print 'ver email:'
    print ver_email[0]
    if ver_email[0]>0:
      print 'ya esta en uso'
      return False
    if row:
      print 'si tiene algo'
      if pass1==row[3]:
        print 'si es la passwd'
        if nombres!=None:
          query.execute('update users set nombres=%s where name_usuario=%s', (nombres,user_to_edit,))
        if apellidos!=None:
          query.execute('update users set apellidos=%s where name_usuario=%s', (apellidos,user_to_edit,))
        if dia!=None and mes!=None and ano!=None:
          if fecha_nac!="0/0/0":
            query.execute('update users set fecha_nac=%s where name_usuario=%s', (fecha_nac,user_to_edit,))
        if correo!=row[2]: 
          if correo!="":
            query.execute('update users set email=%s where name_usuario=%s', (correo,user_to_edit,))
        if pais!=None:
          query.execute('update users set pais=%s where name_usuario=%s', (pais,user_to_edit,))
        if ciudad!=None:
          query.execute('update users set ciudad=%s where name_usuario=%s', (ciudad,user_to_edit,))
        if telefono!=None:
          query.execute('update users set telefono=%s where name_usuario=%s', (telefono,user_to_edit,))
        connection.commit()
        return True
      return False
    return False

  def createPastie (self, title=None, content=None, hashtag=None, privacidad=None, pertenece=None):
    null = None
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select id_p from pastie order by id_p desc;')
    result = query.fetchone()
    new_id_p = int(result[0] + 1)
    print 'PERTENECE'
    print pertenece
    query.execute('select id_p from users where name_usuario=%s', (pertenece,))
    id_pertenece = query.fetchone()
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print time
    query.execute('insert into pastie (id_p,title,contenido,privacidad,time,id_u) values (%s, %s, %s, %s, %s, %s)', (new_id_p, title, content, privacidad, time, id_pertenece[0],))
    

    listaHashtags = hashtag.split( );
    for hashtag in listaHashtags:
      if hashtag[0]!='#':
        return False

    
    for hashtag in listaHashtags:
      query.execute('select id_c from categoria where categoria=%s',(hashtag,))
      result=query.fetchone()
      if result:
        query.execute('insert into p_c (id_p, id_c) values (%s, %s)', (new_id_p, result[0],))
      else:
        query.execute('select id_c from categoria order by id_c desc;')
        result = query.fetchone()
        new_id_c = int(result[0] + 1)
        query.execute('insert into categoria (id_c, categoria) values (%s, %s)', (new_id_c, hashtag,))
        query.execute('insert into p_c (id_p, id_c) values (%s, %s)', (new_id_p, new_id_c,))
      
    connection.commit()
    print 'pastie added'
    query.close()
    connection.close()
    return True

  def verificar_hashtags(self, buscar=None):
    listaBuscar = buscar.split( );
    for buscar in listaBuscar:
      if buscar[0]!='#':
        print "Todas las categorias deben comenzar por '#'"
        return False

    return True

  def search(self,buscar=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    flagEnc=0

    listaBuscar = buscar.split( );

    for buscar in listaBuscar:
      if buscar[0]!='#':
        print "Todas las categorias deben comenzar por '#'"
        return False

    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda

      query.execute('select u.name_usuario,p.title, p.time, p.contenido,p.id_p from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.id_u=u.id_p order by p.time desc',(buscar,))
      result=query.fetchone()
      if result!=None: ##Si se encuentra pasties con el hashtag a buscar
        flagEnc=1
        query.execute('select u.name_usuario,p.title, p.time, p.contenido,p.id_p from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.id_u=u.id_p order by p.time desc',(buscar,))
        result=query.fetchall()

        ##Para recorrer todos los pasties que cumplen un criterio de busqueda
        for row in result:
          print row
      
          ##Para mostrar todos los hashtags asociados a un pastie
          query.execute('select c.categoria from categoria c, p_c where p_c.id_p=%s and p_c.id_c=c.id_c',(row[4],))
          result_p_c=query.fetchall()
          for row_c in result_p_c:
            print row_c[0]
    
    connection.commit()
    query.close()
    connection.close()

    if flagEnc==1:
      return True
    else:
      print "No se encontraron pasties que cumplan el criterio de busqueda"
      return False

  def busqueda_pasties(self, buscar=None, usuario=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from pastie where contenido like %buscar% and privacidad=%s order by time desc', ('publico',))
    contenido = query.fetchall()
    query.execute('select * from pastie,users where contenido like %buscar% and privacidad=%s and pastie.id_u=users.id_p and users.name_usuario=%s order by pastie.time desc',  ('privado',usuario,))
    contenido = contenido + query.fetchall()
    return contenido

  def busqueda_contar(self, buscar=None, usuario=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select count(id_p) from pastie where contenido like %buscar%')
    cant = query.fetchone()
    return  cant[0] 
  def busqueda_hashtag(self, buscar=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from categoria where categoria like %buscar% order by id_c desc', (buscar,))
    hashtags = query.fetchall()
    return hashtags

  def buscar_owners(self, buscar=None, owner=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select name_usuario from users,pastie where users.id_p=pastie.id_u and pastie.contenido like %buscar% and privacidad=%s order by pastie.time desc', ('publico',))
    public = query.fetchall()
    query.execute('select name_usuario from users,pastie where name_usuario=%s users.id_p=pastie.id_u and pastie.contenido like %buscar% and privacidad=%s order by pastie.time desc', (owner,'privacidad',))

   i=0 (luinel,)
   i=1 (dara,)

    

  def search_owner(self,buscar=None,usuario=None,tipo=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    result=[]
    listaBuscar = buscar.split( );
    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda
      if tipo=='anonimo':
        query.execute('select u.name_usuario from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
        result.append(query.fetchall())
    connection.commit()
    query.close()
    connection.close()
    return result

  def search_time(self,buscar=None,usuario=None,tipo=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    result=[]
    listaBuscar = buscar.split( );
    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda
      if tipo=='anonimo':
        query.execute('select p.time from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
        result.append(query.fetchall())
    connection.commit()
    query.close()
    connection.close()
    return result

  def search_title(self,buscar=None,usuario=None,tipo=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    result=[]
    listaBuscar = buscar.split( );
    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda
      if tipo=='anonimo':
        query.execute('select p.title from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
        result.append(query.fetchall())
    connection.commit()
    query.close()
    connection.close()
    return result

  def search_content(self,buscar=None,usuario=None,tipo=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    result=[]
    listaBuscar = buscar.split( );
    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda
      if tipo=='anonimo':
        query.execute('select p.contenido from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
        result.append(query.fetchall())    
    connection.commit()
    query.close()
    connection.close()
    return result

  def search_hashtags(self,buscar=None,usuario=None,tipo=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    resultHashtags=[]
    listaBuscar = buscar.split( );

    for buscar in listaBuscar: ##Para buscar por cada hashtag escrito en la busqueda
      print "BUSCARE POR EL HASHTAG"
      print buscar
      if tipo=='anonimo':
        query.execute('select p.id_p from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
        result=query.fetchone()
        if result!=None: ##Si se encuentra pasties con el hashtag a buscar
          query.execute('select p.id_p from pastie p, categoria c, p_c, users u where c.categoria=%s and c.id_c=p_c.id_c and p_c.id_p=p.id_p and p.privacidad=%s and p.id_u=u.id_p order by p.time desc',(buscar,'publico'))
          result=query.fetchall()
          print "LOS PASTIES SON:"
          print result
          ##Para recorrer todos los pasties que cumplen un criterio de busqueda
          for row in result:
            print row
            ##Para mostrar todos los hashtags asociados a un pastie
            query.execute('select c.categoria from categoria c, p_c where p_c.id_p=%s and p_c.id_c=c.id_c',(row[0],))
            print query.fetchall()
            resultHashtags.append(query.fetchall())
            print resultHashtags

    connection.commit()
    query.close()
    connection.close()
    return resultHashtags


  def cambio_pass(self,pass_act=None, pass_nva=None, pass_verif=None, owner=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select password from users where name_usuario=%s',(owner,))
    clave=query.fetchone()
    if clave[0]==pass_act:
      if pass_nva==pass_verif:
        query.execute('update users set password=%s where name_usuario=%s', (pass_nva,owner,))
      else:
        print "Contrasena Nueva y Contrasena Nueva repetida deben ser iguales"
        return 2
    else:
      print "Contrasena actual suministrada no es correcta"
      return 3

    connection.commit()
    query.close()
    connection.close()
    return 1


  def pasties(self):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from pastie where privacidad=%s order by time desc', ('publico',))
    cant = query.fetchall()
    return cant

  def own_pasties(self, owner=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from pastie,users where pastie.id_u=users.id_p and users.name_usuario=%s order by time desc', (owner,))
    cant = query.fetchall()
    return cant    

  def pastie_edit(self,id_pastie=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select * from pastie where id_p=%s', (id_pastie,))
    pastie = query.fetchone()
    return pastie

  def own_hashtags(self, owner=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select categoria,pastie.id_p from categoria,p_c,pastie,users where categoria.id_c=p_c.id_c and p_c.id_p=pastie.id_p and pastie.id_u=users.id_p and users.name_usuario=%s group by categoria,pastie.id_p order by pastie.id_p desc', (owner,))
    #select categoria,pastie.id_p  from categoria,p_c,pastie where categoria.id_c = p_c.id_c and p_c.id_p = pastie.id_p and pastie.privacidad='publico' group by categoria,pastie.id_p;
    hashtags = query.fetchall()
    return hashtags

  def owners(self):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select name_usuario from users,pastie where users.id_p=pastie.id_u and pastie.privacidad=%s order by pastie.time desc', ('publico',))
    owners = query.fetchall()
    return owners

  def hashtags(self):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select categoria,pastie.id_p from categoria,p_c,pastie where categoria.id_c=p_c.id_c and p_c.id_p=pastie.id_p and pastie.privacidad=%s group by categoria,pastie.id_p order by pastie.id_p desc', ('publico',))
    #select categoria,pastie.id_p  from categoria,p_c,pastie where categoria.id_c = p_c.id_c and p_c.id_p = pastie.id_p and pastie.privacidad='publico' group by categoria,pastie.id_p;
    hashtags = query.fetchall()
    return hashtags

  def count(self):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select count(id_p) from pastie where privacidad=%s', ('publico',))
    cant = query.fetchone()
    return cant[0]

  def own_count(self,owner=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select count(pastie.id_p) from pastie,users where pastie.id_u=users.id_p and users.name_usuario=%s', (owner,))
    cant = query.fetchone()
    return cant[0]    

  def fix(self, hashtags=None):
    tam = len(hashtags)
    print 'estoy en fixxxx------- y el tamm es----'
    print tam 
    hashtags_fixed=[]
    max_pastie = hashtags[tam-1][1]
    min_pastie_id = hashtags[0][1]
    apilados = 0
    if tam == 0:
      return ['#NoTienesPasties']
    for i in range(0,max_pastie):
      i = apilados
      pastie_id = hashtags[i][1]
      categoria = []
      for j in range(i,tam):
        j = apilados
        if hashtags[j][1]==pastie_id:
          categoria.append(hashtags[j][0])
          categoria.append(' ')
          apilados = apilados + 1
      categorias_pastie = ""
      tam_new = len(categoria)
      for k in range(0,tam_new):
        categorias_pastie = categorias_pastie + categoria[k]
      hashtags_fixed.append(categorias_pastie)
    return hashtags_fixed
    
  def fix_own(self, hashtags=None):
    print 'entre a fix own me mandaron'
    print hashtags
    tam = len(hashtags)
    hashtags_fixed = []
    concat=""
    apilados = 0
    if tam == 0:
      return ['#NoTienesPasties']
    if tam == 1:
      concat = concat + hashtags[0][0]
      hashtags_fixed.append(concat)
      return hashtags_fixed
    for i in range(0,tam-1):
      i=apilados
      if i > tam-1:
        break
      aux = hashtags[i][1]
      concat = ""
      for k in range (i,tam):
        if hashtags[k][1]==aux:
          apilados = apilados + 1
          concat = concat + hashtags[k][0] + " "
      hashtags_fixed.append(concat)
    return hashtags_fixed

  def remove(self,id_remove=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('delete from p_c where id_p=%s', (id_remove,))
    query.execute('delete from pastie where id_p=%s', (id_remove,))
    connection.commit()
    query.close()

  def categorias_edit(self, id_edit=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('select categoria from categoria,p_c,pastie where categoria.id_c=p_c.id_c and p_c.id_p=pastie.id_p and pastie.id_p=%s', (id_edit,))
    categoria = query.fetchall()
    print 'estas son las del query'
    print categoria
    print 'con un id'
    print id_edit
    print categoria[0][0]
    tam = len(categoria)
    categorias = ""
    if tam == 1:
      categorias = categorias + categoria[0][0]
      return categorias
    for i in range(0,tam):
      categorias = categorias + categoria[i][0] + " "
    return categorias



  def edit(self, id_edit=None, title=None, contenido=None, categorias=None, privacidad=None):
    connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
    query = connection.cursor()
    query.execute('update pastie set title=%s, contenido=%s, privacidad=%s where id_p=%s', (title,contenido,privacidad,id_edit,))
    query.execute('delete from p_c where id_p=%s',(id_edit))

    listaHashtags = categorias.split( );

    for hashtag in listaHashtags:
      if hashtag[0]!='#':
        return False

    for hashtag in listaHashtags:
      query.execute('select id_c from categoria where categoria=%s',(hashtag,))
      result=query.fetchone()
      if result:
        query.execute('insert into p_c (id_p, id_c) values (%s, %s)', (id_edit, result[0],))
      else:
        query.execute('select id_c from categoria order by id_c desc;')
        result = query.fetchone()
        new_id_c = int(result[0] + 1)
        query.execute('insert into categoria (id_c, categoria) values (%s, %s)', (new_id_c, hashtag,))
        query.execute('insert into p_c (id_p, id_c) values (%s, %s)', (id_edit, new_id_c,))
    
    connection.commit()
    query.close()
    connection.close()
    return True
