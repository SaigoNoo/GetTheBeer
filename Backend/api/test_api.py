from json import dumps
from os import getenv
from unittest import TestCase, main

from dotenv import load_dotenv
from requests import get, post


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
            expected_keys=["mode", "detail"],
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

    def

if __name__ == '__main__':
    load_dotenv()
    main()
