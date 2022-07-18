class Journalentries():
    def __init__(self, id, date, concept, entry, mood_id):
        self.id = id
        self.date = date
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.mood = None
        self.tags = None
    