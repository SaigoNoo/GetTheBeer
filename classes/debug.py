class Debug:
    def __init__(self, mode: bool = True):
        self.mode = mode

    def print(self, text: str, app_module: str = "MAIN"):
        if self.mode:
            print(f"[Debug: {app_module}] $> {text}")

    def save(self, text: str):
        if self.mode:
            pass
            """
            Pourra servir pour stocker...
            """
