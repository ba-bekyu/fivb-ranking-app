from flask import Flask, render_template, request

app = Flask(__name__)

# 試合結果ごとのスコア値（SSV）
score_map = {
    "3-0": 1.5,
    "3-1": 1.0,
    "3-2": 0.5,
    "2-3": -0.5,
    "1-3": -1.0,
    "0-3": -1.5
}

def calculate_expected_result(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 600))

def calculate_point_change(rating_a, rating_b, result, mwf=1.0):
    ssv = score_map[result]
    emr = calculate_expected_result(rating_a, rating_b)
    wr = ssv - emr
    change = round(wr * mwf * 8, 2)
    return change, -change

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        team_a = request.form["team_a"]
        team_b = request.form["team_b"]
        rating_a = float(request.form["rating_a"])
        rating_b = float(request.form["rating_b"])
        match_result = request.form["match_result"]

        change_a, change_b = calculate_point_change(rating_a, rating_b, match_result)
        result = f"{team_a}: {change_a:+.2f} ポイント, {team_b}: {change_b:+.2f} ポイント"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
