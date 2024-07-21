from datetime import datetime

class ThemeParkAttractionShowTime:

  def __init__(self,
               start_time: datetime,
               end_time: datetime
  ):
    self.start_time = start_time
    self.end_time = end_time

  def to_json(self):
    return {
      "start_time": self.start_time,
      "end_time": self.end_time,
    }