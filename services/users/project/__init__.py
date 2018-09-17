#Services/users/project/__init__.py
from flask import Flask,jsonify

#instanciar app
app=Flask(__name__)

#estableciendo configuracion
app.config.from_object("project.config.DevelopmentConfig")

@app.route("/users/ping",methods=['GET'])
def ping_pong():
	return jsonify({
		'estado':'satisfactorio',
		'mensaje':'pong!!'
		})