import psycopg2
from datetime import *
import math

class User:
  def __init__(self, name, active=True):
        self.name = name
        connection = psycopg2.connect('dbname=ati_database user=ati password=ati host=localhost')
        query = connection.cursor()
        query.execute('select count(usuario) from sess where usuario=%s',(name,))
        existe = query.fetchone()
        print 'existe es '
        print existe[0]
        if existe[0]>=1:
          print 'este usuario ya existe'
          query.execute('select sess from sess where usuario=%s', (name,))
          self.id = query.fetchone()
          print self.id
        else:
          query.execute('select count(sess) from sess')
          row = query.fetchone()
          print 'el sess es'
          print row[0]
          new_row = row[0]+1
          self.id = new_row
          print 'insertare el id'
          print new_row
          query.execute('insert into sess values(%s,%s)',(new_row,name,))
        connection.commit()
        query.close()
        connection.close()
        self.active = active

  def is_active(self):
      return self.active

  def is_anonymous(self):
      return False

  def is_authenticated(self):
      return True

  def get_id(self):
    return self.id