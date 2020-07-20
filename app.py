from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route('/data')
def index():
    print("Success")
    # return "TEST"
    return render_template('home.html') #render_template : html 형식 파일의 데이터를 텍스트 형식으로 바꿔서 날려줌


if __name__ == '__main__' :
    # app.run(host = '0.0.0.0', port = '8080')
    app.run()