from flask import Flask, Response, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import json
import cx_Oracle
import config
from flask_login import LoginManager, login_user, login_required
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from flask_cors import CORS

username = 'sys'
password = '123456789CCC'
ip = 'localhost'
port = 1521
SID = 'xe'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)
encoding = 'UTF-8'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ('oracle+cx_oracle://system:123456789CCC@' +
                                         dsn_tns)
CORS(app)
app.config['SECRET_KEY'] = password

db = SQLAlchemy(app)

lm = LoginManager(app)





# db.create_all()
#
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    phone = db.Column(db.String(15))

    # db.create_all()

    @property
    def is_autenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def to_json(self):
        return {"id": self.id, "username": self.username, "name": self.name, "email": self.email,
                "password": self.password,
                "phone": self.phone}


class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    description = db.Column(db.String(300))
    status = db.Column(db.String(1))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=user_id)

    def to_json(self):
        return {"id": self.id, "pet_name": self.pet_name, "type": self.type, "description": self.description,
                "status": self.status,
                "user_id": self.user_id,
                }


@app.route("/")
def home():
    connection = cx_Oracle.connect('system', '123456789CCC', dsn_tns)
    return jsonify(status='success', db_version=connection.version)


# # login usuário

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    body = request.get_json()
    username = StringField(username=body["username"], validators=[DataRequired()])
    password = PasswordField(password=body["password"], validators=[DataRequired()])

    if request.method == 'POST':

        user = User.query.filter_by(username=body["username"]).first()
        if user and user.password == body["password"]:
            result = login_user(user)
            if (result):
                return gera_response(200, "usuario", user.to_json(), "Logado com sucesso")
            else:
                return gera_response(401, "usuario", {}, "Sem autorização")
        else:
            return gera_response(400, "usuario", {}, "Inavalid Login")
    return gera_response(500, "usuario", {}, "Impossível fazer login, entre em contato com a assistência")



# Selecionar Tudo Usuário
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = User.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json)


# Selecionar Tudo PET
@app.route("/pets", methods=["GET"])
def seleciona_pets():
    pets_objetos = Pet.query.all()
    pets_json = [pets.to_json() for pets in pets_objetos]

    return gera_response(200, "pets", pets_json)


###########################################################
# Selecionar todos os PETs com usuarios
@app.route("/pets/user", methods=["GET"])
def seleciona_pets_and_users():
    pets_and_users_objetos = Pet.query.join(User, Pet.user_id == User.id).add_columns(Pet.id,
                                                                                      Pet.pet_name, Pet.type,
                                                                                      Pet.status,
                                                                                      Pet.description, Pet.user_id,
                                                                                      User.name, User.phone,
                                                                                      User.email)

    list = []

    for row in pets_and_users_objetos:
        map = {"pet_id": row[1], "pet_name": row[2], "type": row[3], "status": row[4], "description": row[5],
               "user_id": row[6], "name": row[7], "email": row[9], "phone": row[8]}
        list.append(map)

    return gera_response(200, "pets_users", list)


# Selecionar todos PETs com usuarios e status
@app.route("/pets/user/status=<status>", methods=["GET"])
def seleciona_pets_and_users_all_status(status):
    pets_and_users_objetos = Pet.query.join(User, Pet.user_id == User.id).add_columns(Pet.id,
                                                                                      Pet.pet_name, Pet.type,
                                                                                      Pet.status,
                                                                                      Pet.description, Pet.user_id,
                                                                                      User.name, User.phone,
                                                                                      User.email).filter(
        Pet.status == status)

    list = []

    for row in pets_and_users_objetos:
        map = {"pet_id": row[1], "pet_name": row[2], "type": row[3], "status": row[4], "description": row[5],
               "user_id": row[6], "name": row[7], "email": row[9], "phone": row[8]}
        list.append(map)

    return gera_response(200, "pets_users", list)


# Selecionar Tipo PET com usuarios
@app.route("/pets/user/type=<type>", methods=["GET"])
def seleciona_pets_and_users_type(type):
    pets_and_users_objetos = Pet.query.join(User, Pet.user_id == User.id).add_columns(Pet.id,
                                                                                      Pet.pet_name, Pet.type,
                                                                                      Pet.status,
                                                                                      Pet.description, Pet.user_id,
                                                                                      User.name, User.phone,
                                                                                      User.email).filter(
        Pet.type == type)

    list = []

    for row in pets_and_users_objetos:
        map = {"pet_id": row[1], "pet_name": row[2], "type": row[3], "status": row[4], "description": row[5],
               "user_id": row[6], "name": row[7], "email": row[9], "phone": row[8]}
        list.append(map)

    return gera_response(200, "pets_users", list)


# Selecionar Tudo PET com usuarios status
@app.route("/pets/user/type=<type>/status=<status>", methods=["GET"])
def seleciona_pets_and_users_status(type, status):
    pets_and_users_objetos = Pet.query.join(User,
                                            Pet.user_id == User.id).add_columns(Pet.id, Pet.pet_name, Pet.type,
                                                                                Pet.status, Pet.description,
                                                                                Pet.user_id,
                                                                                User.name, User.phone,
                                                                                User.email).filter(
        Pet.type == type).filter(Pet.status == status)

    list = []

    for row in pets_and_users_objetos:
        map = {"pet_id": row[1], "pet_name": row[2], "type": row[3], "status": row[4], "description": row[5],
               "user_id": row[6], "name": row[7], "email": row[9], "phone": row[8]}
        list.append(map)

    return gera_response(200, "pets_users", list)


#########################################################

# Selecionar Individual usuário
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = User.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)


###########################################################################

###Testar

# Selecionar filter status pet
@app.route("/pets/status=<status>", methods=["GET"])
def seleciona_pets_status(status):
    pet_objeto = Pet.query.filter_by(status=status)
    pets_json = [pets.to_json() for pets in pet_objeto]

    return gera_response(200, "pets", pets_json)


# Selecionar filter status pet
@app.route("/pets/type=<type>", methods=["GET"])
def seleciona_pets_type(type):
    pet_objeto = Pet.query.filter_by(type=type)

    pets_json = [pets.to_json() for pets in pet_objeto]
    return gera_response(200, "pets", pets_json)


############################################################################

# Cadastrar usuário
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = User(username=body["username"], name=body["name"], email=body["email"], password=body["password"],
                       phone=body["phone"])
        # usuario = User(username=body["username"], email=body["email"], password=body["password"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# Cadastrar PET
@app.route("/pet", methods=["POST"])
def cria_pet():
    body = request.get_json()

    try:
        pet = Pet(pet_name=body["pet_name"], type=body["type"], description=body["description"],
                  status=body["status"], user_id=body["user_id"],
                  )
        # usuario = User(username=body["username"], email=body["email"], password=body["password"])
        db.session.add(pet)
        db.session.commit()
        return gera_response(201, "pet", pet.to_json(), "Pet Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "pet", {}, "Erro ao cadastrar")


###########################################################################
# Atualizar Usuário
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = User.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if ('username' in body):
            usuario_objeto.username = body['username']
        if ('email' in body):
            usuario_objeto.email = body['email']
        if ('name' in body):
            usuario_objeto.name = body['name']
        if ('password' in body):
            usuario_objeto.password = body['password']
        if ('phone' in body):
            usuario_objeto.phone = body['phone']

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")


##################################################################################


# Atualizar Pet

@app.route("/pet/<id>", methods=["PUT"])
def atualiza_pet(id):
    pet_objeto = Pet.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if ('pet_name' in body):
            pet_objeto.pet_name = body['pet_name']
        if ('type' in body):
            pet_objeto.type = body['type']
        if ('description' in body):
            pet_objeto.description = body['description']
        if ('status' in body):
            pet_objeto.status = body['status']
        if ('user_id' in body):
            pet_objeto.user_id = body['user_id']

        db.session.add(pet_objeto)
        db.session.commit()
        return gera_response(200, "pet", pet_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")


################################################################################

# Deletar
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = User.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


# Deletar
@app.route("/pet/<id>", methods=["DELETE"])
def deleta_pet(id):
    pet_objeto = Pet.query.filter_by(id=id).first()

    try:
        db.session.delete(pet_objeto)
        db.session.commit()
        return gera_response(200, "pet", pet_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "pet", {}, "Erro ao deletar")


####################################################################################
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if (mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run(debug=True)
