from datetime import datetime

class Project:
    def __init__(self, title, details, total_target, start_date, end_date, owner):
        self.title = title
        self.details = details
        self.total_target = total_target
        self.start_date = start_date
        self.end_date = end_date
        self.owner = owner
        self.created_at = datetime.now()
        self.current_amount = 0

    @staticmethod
    def validate_dates(start_date, end_date):
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            return start < end and start > datetime.now()
        except ValueError:
            return False

    def to_dict(self):
        return {
            'title': self.title,
            'details': self.details,
            'total_target': self.total_target,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'owner': self.owner.email,
            'current_amount': self.current_amount,
            'created_at': self.created_at.isoformat()
        }

