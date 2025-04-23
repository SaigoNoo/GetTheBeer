class Debug:
    def __init__(self, mode: bool = False):
        self.mode = mode

    def print(self, text: str, app_module: str = "MAIN"):
        if self.mode:
            print(f"[{app_module}] $> {text} (DebugMode)")

    def save(self, text: str):
        if self.mode:
            pass
            """
            Pourra servir pour stocker...
            """
