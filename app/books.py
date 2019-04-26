from flask import Blueprint, current_app, request, jsonify, url_for
from .serializer import BookSchema
from .model import Book


bp_books = Blueprint('books', __name__)


@bp_books.route('/list', methods=['GET'])
def list():
    bs =  BookSchema(many=True)
    result = Book.query.all()
    return bs.jsonify(result), 200


@bp_books.route('/detail/<id>', methods=['GET'])
def getone(id):
    bs = BookSchema()
    book =  Book.query.filter(Book.id == id)
    return bs.jsonify(book.first())


@bp_books.route('/create', methods=['POST'])
def create():
    bs = BookSchema()
    book , error = bs.load(request.json)
    current_app.db.session.add(book)
    current_app.db.session.commit()
    return bs.jsonify(book), 201

@bp_books.route('/update/<id>', methods=['POST'])
def update(id):
    bs = BookSchema()
    book =  Book.query.filter(Book.id == id)
    book.update(request.json)
    current_app.db.session.commit()
    return bs.jsonify(book.first())


@bp_books.route('/delete', methods=['POST'])
def delete():
    id = request.json.get('id')
    Book.query.filter(Book.id == id).delete()
    current_app.db.session.commit()
    return url_for('books.list')


