import sudoku_controller as sc
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)



@app.route('/create-game',methods=['GET'])
def create_game():
    s = sc.SudokuGame('Adam')
    return str(s)
    # str(s.puzzle_2d)return 'hello world'


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# class ISudoku:
#     def __init__(self):
#         s=sc.SudokuGame(  )
#     def create_game(self,name):
#         s=SudokuGame(name)