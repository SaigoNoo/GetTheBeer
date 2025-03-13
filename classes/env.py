class Env:
    """
    Gestion du fichier .env
    """

    def __init__(
            self,
            server=None,
            username=None,
            password=None,
            dbname=None,
            port=None
    ):
        self.server = "localhost" if server == "" else server
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = "3306" if port == "" else port

    def store_values(self, master_password: str):
        temp = (
            f"DB_SERVER={self.server}\n"
            f"DB_USERNAME={self.username}\n"
            f"DB_PASSWORD={self.password}\n"
            f"DB_NAME={self.dbname}\n"
            f"DB_PORT={self.port}\n"
            f"BACKEND_MASTER_PASSWORD={master_password}"
        )
        with open(file=".env", mode="w", encoding="utf-8") as env:
            return env.write(temp)

    @staticmethod
    def get_value(key: str = None):
        temp = {}
        with open(file=".env", mode="r", encoding="utf-8") as env:
            for line in env.readlines():
                key_dict, value_dict = line.strip().split("=")
                temp[key_dict.strip()] = value_dict.strip()
        return temp if key is None else temp[key]
