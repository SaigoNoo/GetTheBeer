class LevelSystem:
    LEVEL_THRESHOLDS = [
        (1, "Noob du comptoir"), (10, "Baby Alcolo"), (20, "Apprenti Tavernier"),
        (30, "Buveur Confirmé"), (40, "Maître des Mousseux"), (50, "Junior Tavernier"),
        (60, "Ancien de la Brasserie"), (70, "Seigneur de la Chope"),
        (80, "Grand Sage du Houblon"), (90, "Légende des Bistrot"), (100, "Dieu de la Bière")
    ]

    def __init__(self, db):
        self.db = db

    def get_level_and_title(self, beers_won: int):
        level = 1
        title = "Noob du comptoir"

        for threshold, name in self.LEVEL_THRESHOLDS:
            if beers_won >= threshold:
                level = threshold
                title = name
            else:
                break

        return level, title

    def update_user_level(self, user_id: int):
        beers_won = self.db.call_function("get_user_beers", id=user_id)
        level, title = self.get_level_and_title(beers_won)

        self.db.call_procedure("update_user_level", id=user_id, level=level, title=title)
        return {"level": level, "title": title}