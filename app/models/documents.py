# -*- coding: utf-8 -*-


from app import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    text = db.Column(db.Text())
    publish = db.Column(db.Boolean(), default=False)

    @staticmethod
    def get_document_by_id(id):
        return Document.query.filter_by(id=id).first()

    @staticmethod
    def get_all_documents():
        return Document.query.all()

    @staticmethod
    def add_documents(type, text):
        document = Document(type=type, text=text)
        db.session.add(document)
        db.session.commit()

    @staticmethod
    def update_document_by_id(id, type, text):
        document = Document.get_document_by_id(id)
        document.type = type
        document.text = text
        db.session.add(document)
        db.session.commit()

    @staticmethod
    def delete_document_by_id(id):
        document = Document.get_document_by_id(id)
        db.session.delete(document)
        db.session.commit()

    @staticmethod
    def xor_document_by_id(id):
        document = Document.get_document_by_id(id)
        document.publish = not document.publish
        db.session.add(document)
        db.session.commit()

    @staticmethod
    def generate_foke(count=5):
        import forgery_py
        from random import seed
        seed()
        for i in range(count):
            Document.add_documents(type=forgery_py.lorem_ipsum.word(),
                                   text=forgery_py.lorem_ipsum.sentence())

