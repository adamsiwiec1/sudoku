from sudoku_backend import Sudoku
from flask import Flask, render_template
from flask_restful import Resource, Api

app=Flask(__name__)
# self.api = Api(self.app)

sudoku=Sudoku('Adam')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', data=enumerate(sudoku.puzzle))

@app.route('/create-new-game', methods=['GET'])
def create_game():
    sudoku.new_game()
    return render_template('index.html', data=enumerate(sudoku.puzzle))

@app.route('/get-puzzle', methods=['GET'])
def get_puzzle():
    print(sudoku.puzzle)
    return render_template('index.html', data=enumerate(sudoku.puzzle))


@app.route('/get-solution', methods=['GET'])
def get_solution():
    print(sudoku.puzzle)
    return render_template('index.html', data=enumerate(sudoku.solution))

@app.route('/error', methods=['GET'])
def raise_error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)