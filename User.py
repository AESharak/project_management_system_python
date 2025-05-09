import re
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password, mobile_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile_phone = mobile_phone
        self.is_active = False
        self.created_at = datetime.now()
        self.projects = []

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_egyptian_phone(phone):
        pattern = r'^01[0125][0-9]{8}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_password(password):
        return len(password) >= 8

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'mobile_phone': self.mobile_phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
