from json import dumps
from os import getenv
from unittest import TestCase, main

from dotenv import load_dotenv
from requests import get, post, Session


class TestAPIEndpoints(TestCase):
    def make_test(self, response, type_awaited, expected_keys=None, received_keys=None, code_405_allowed=False):
        """
        Test générique pour valider une réponse d'API :
        - Vérifie le code HTTP (200 ou 405 si autorisé)
        - Vérifie le type du body
        - Optionnellement : compare les clés attendues
        """
        if code_405_allowed:
            self.assertIn(response.status_code, [200, 405])
            if response.status_code == 405:
                print("⚠️ 405 accepté pour cette opération")
                body = response.json()
                print("💬 Reçu :", dumps(obj=body, indent=4, ensure_ascii=False))
                return
        else:
            self.assertEqual(response.status_code, 200)

        body = response.json()
        print("💬 Reçu :", dumps(obj=body, indent=4, ensure_ascii=False))

        self.assertEqual(type(body), type_awaited)

        if expected_keys is not None and received_keys is not None:
            self.assertEqual(
                second=set(received_keys),
                first=set(expected_keys),
                msg="⛔ Les clés reçues ne correspondent pas exactement à celles attendues."
            )

    def test_show_members(self):
        response = get(
            url=f"{getenv('BACKEND_URL')}/api/user/show_members",
            headers={
                "Accept": "application/json"
            },
            timeout=5
        )
        self.make_test(
            response=response,
            type_awaited=list,
            expected_keys=['user_ID', 'nom', 'prenom', 'pseudo', 'mail', 'image', 'biographie'],
            received_keys=list(response.json()[0].keys())
        )

    def test_add_friend(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/add_friend?user_id=1&friend_id=2",
            headers={
                "Accept": "application/json"
            },
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["message"],
            received_keys=list(response.json().keys()),
            code_405_allowed=True
        )

    def test_user_create(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/create",
            headers={
                "Accept": "application/json"
            },
            json={
                "f_name": "Test",
                "l_name": "NomTest",
                "username": "test",
                "email": "giorgiosdoussis@gmail.com",
                "bio": "Ceci est un test API",
                "password": "passwordtry"
            },
            timeout=5
        )
        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["code", "message", "detail"],
            received_keys=list(response.json().keys()),
            code_405_allowed=True
        )

    def test_reset_request(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/reset_password_request",
            headers={
                "Accept": "application/json"
            },
            json={
                "username": "string"
            },
            timeout=5
        )
        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["code", "message"],
            received_keys=list(response.json().keys())
        )

    def test_reset_password(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/reset_password",
            headers={
                "Accept": "application/json"
            },
            json={
                "token": input("TOKEN: "),
                "password": input("PASSWORD: ")
            },
            timeout=5
        )
        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["message", "code", "erreur"],
            received_keys=list(response.json().keys())
        )

    def test_debug_true(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/system/debug?debug_mode=true",
            headers={
                "Accept": "application/json"
            }
        )
        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["message"],
            received_keys=list(response.json().keys())
        )

    def test_debug_false(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/system/debug?debug_mode=false",
            headers={
                "Accept": "application/json"
            }
        )
        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["message"],
            received_keys=list(response.json().keys())
        )

    def test_login(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/login",
            headers={"Accept": "application/json"},
            json={
                "username": "Trisouille",  # adapte selon ta DB
                "password": "user123"
            },
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["success", "code", "message"],
            received_keys=list(response.json().keys())
        )

    def test_delete_friend(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/delete_friend/?user_id=1&friend_id=2",
            headers={
                "Accept": "application/json"
            },
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["message"],
            received_keys=list(response.json().keys()),
            code_405_allowed=True
        )

    def test_logout(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/user/logout",
            headers={
                "Accept": "application/json"
            },
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["code", "message"],
            received_keys=list(response.json().keys()),
            code_405_allowed=True
        )

    def test_send_mail(self):
        response = post(
            url=f"{getenv('BACKEND_URL')}/api/mail/send/",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json={
                "email": "dorian.kwizera@gmail.com",
                "subject": "Test unitaire",
                "file": "Bonjour jeune buveur",
                "extra": {}
            },
            timeout=5
        )

        print("Status code:", response.status_code)
        print("Raw response:", response.text)

        try:
            body = response.json()
            print("💬 JSON reçu :", dumps(body, indent=4, ensure_ascii=False))
        except Exception as e:
            print("⛔ Erreur de décodage JSON :", e)

    def test_is_friend(self):
        response = get(
            url=f"{getenv('BACKEND_URL')}/api/user/is_friend?username_a=Trisouille&username_b=DKwiz",
            headers={
                "Accept": "application/json"
            },
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict
        )

    def test_get_current_user(self):
        session = Session()

        login_response = session.post(
            url=f"{getenv('BACKEND_URL')}/api/user/login",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"username": "Trisouille", "password": "user123"},
            timeout=5
        )
        #print("Réponse login:", login_response.json())
        self.assertEqual(login_response.status_code, 200)

        response = session.get(
            url=f"{getenv('BACKEND_URL')}/api/user/me",
            headers={"Accept": "application/json"},
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=["user"],
            received_keys=list(response.json().keys())
        )

    def test_get_profile(self):
        session = Session()

        login_response = session.post(
            url=f"{getenv('BACKEND_URL')}/api/user/login",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json={
                "username": "Trisouille",
                "password": "user123"
            },
            timeout=5
        )
        #print("Réponse login:", login_response.json())
        self.assertEqual(login_response.status_code, 200)

        response = session.get(
            url=f"{getenv('BACKEND_URL')}/api/user/profil",
            headers={"Accept": "application/json"},
            timeout=5
        )

        self.make_test(
            response=response,
            type_awaited=dict,
            expected_keys=[
                "user_ID", "nom", "prenom", "pseudo",
                "mail", "image", "biographie"
            ],
            received_keys=list(response.json().keys())
        )


if __name__ == '__main__':
    load_dotenv()
    main()
