import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests para el servicio Users."""

    def test_users(self):
        """Nos aseguramos que la ruta localhost:5001/users/ping
        esta funcionando correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurando de que se pueda agregar un nuevo usuario a la db"""
        with self.client:
            response = self.client.post('/users', data=json.dumps({
                    "username": "abel",
                    "email": "abel.huanca@upeu.edu.pe"
                    }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            "abel.huanca@upeu.edu.pe a sido agregado!",
            data["message"])
        self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """ Asegurando de que se arroje un error
         si el objeto JSON está vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga invalida.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurando de que se produce un error si el
         objeto JSON no tiene una clave
         de nombre de usuario."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'abel.huanca@upeu.edu.pe'}),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga invalida.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegurando de que se haya producido
        un error si el correo electrónico ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                        'username': 'abel',
                        'email': 'abel.huanca@upeu.edu.pe'}),
                content_type='application/json',)
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'abel',
                    'email': 'abel.huanca@upeu.edu.pe'
                    }),
                content_type='application/json',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. Este correo ya existe.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Asegurando de que el usuario
        individual se comporte correctamente"""
        user = add_user('abel', 'abel.huanca@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('abel', data['data']['username'])
            self.assertIn('abel.huanca@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Asegurese de que se arroje un error
        si no se proporciona una identificacion."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('el usuario no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegurando se que se arroje un error si
        la identificacion no existe"""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('el usuario no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Asegurando de que todos los usuarios se
        comporten correctamente"""
        add_user('abel', 'abel.huanca@upeu.edu.pe')
        # user = add_user('fredy', 'abel.huanca@gmail.com')
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('abel', data['data']['users'][0]['username'])
            self.assertIn(
                'abel.huanca@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('fredy', data['data']['users'][1]['username'])
            self.assertIn(
                'abel.huanca@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
