from fastapi import FastAPI

from classes.debug import Debug


def load(app: FastAPI, debug: Debug) -> None:
    """
    Charger toutes les CALLS API
    """

    @app.post(
        path="/api/system/debug",
        description="Permet de définir le mode débug pour cette instance !",
        tags=["Debug"],
    )
    async def toggle_mode(debug_mode: bool):
        if debug.mode and debug_mode:
            pass
        elif debug.mode and not debug_mode:
            debug.mode = debug_mode
            return {
                "message": "Désactivation du mode debug"
            }
        elif not debug_mode and not debug_mode:
            pass
        else:
            debug.mode = debug_mode
            return {
                "message": "Activation du mode debug"
            }
