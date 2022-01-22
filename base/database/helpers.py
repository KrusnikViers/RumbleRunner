from sqlalchemy import orm


class DBHelpers:
    @staticmethod
    def select_and_update_by_tg_id(session: orm.Session, model, tg_id: int, **kwargs):
        instance = session.query(model).filter(model.tg_id == tg_id).first()
        if not instance:
            instance = model(tg_id=tg_id, **kwargs)
            session.add(instance)
            return instance
        for key, value in kwargs.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)
        return instance
