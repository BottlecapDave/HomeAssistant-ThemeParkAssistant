class ThemePark:

  def __init__(self,
               id: str,
               name: str,
               destination_id: str,
               destination_name: str,
               destination_slug: str
  ):
    self.id = id
    self.name = name
    self.destination_id = destination_id
    self.destination_name = destination_name
    self.destination_slug = destination_slug

  def to_json(self):
    return {
      "id": self.id,
      "name": self.name,
      "destination_id": self.destination_id,
      "destination_name": self.destination_name,
      "destination_slug": self.destination_slug,
    }