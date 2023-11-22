from sqlalchemy.orm import declared_attr


class UserRelationMixin:
    @declared_attr
    def user_id(self):
        return
