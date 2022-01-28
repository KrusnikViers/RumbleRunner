from base.database.session_scope import SessionScope


class DBHelpers:
    @staticmethod
    def select_and_update_by_tg_id(model, tg_id: int, **kwargs):
        session = SessionScope.session()
        instance = session.query(model).filter(model.tg_id == tg_id).first()
        if not instance:
            instance = model(tg_id=tg_id, **kwargs)
            session.add(instance)
            session.commit()
            return instance
        changed = False
        for key, value in kwargs.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)
                changed = True
        if changed:
            session.commit()
        return instance
