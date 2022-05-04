from flask import Blueprint, jsonify, session, request, redirect
from flask_login import login_required, current_user
from backend.forms.new_board_form import NewBoardForm
from backend.models.board import Board
from backend.models import User
from backend.models.db import db
from backend.api.auth_routes import validation_errors_to_error_messages

board_routes = Blueprint('boards', __name__)


# R E A D  A L L
@board_routes.route('/', methods = [ 'GET' ])
@login_required
def read_all_boards():
    boards = Board.query.filter(Board.user_id == current_user.id).all()
    return {'boards': [board.to_dict() for board in boards]}


# R E A D O N E
@board_routes.route('/<int:id>', methods=['GET'])
def read_one_board(id):
    board = Board.query.get(id)
    return board.to_dict()

# C R E A T E
@board_routes.route('/new-board', methods = [ 'GET', 'POST' ])
def new_board():
    form = NewBoardForm()

    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        board = Board(
            user_id=form.data['user_id'],
            title=form.data['title'],
            avatar_id=form.data['avatar_id'],
            # workspace_id=form.data['workspace_id']
        )
        db.session.add(board)
        db.session.commit()
        return board.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


# U P D A T E
@board_routes.route('/<int:id>', methods = [ 'PUT' ])
def update_board(id):
    board = Board.query.get(id)

    title = request.json['title']
    avatar_id = request.json['avatar_id']

    board.title = title
    board.avatar_id = avatar_id

    db.session.commit()
    return board.to_dict()


# D E L E T E
@board_routes.route('/<int:id>', methods = [ 'DELETE' ])
def delete_board(id):
    board = Board.query.get(id)

    db.session.delete(board)
    db.session.commit()