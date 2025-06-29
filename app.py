from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

def fetch_reel_row_no_login(reel_url: str) -> str:
    L = instaloader.Instaloader()
    shortcode = reel_url.rstrip('/').split('/')[-1]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    user = post.owner_username
    reel_link = post.video_url
    caption = post.caption or "Enjoy this reel"

    caption = caption.replace('\n', ' ').replace(';', ',')

    return f"{user};{reel_link};{caption}\n"

@app.route("/reel", methods=["GET"])
def get_reel():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        reel_row = fetch_reel_row_no_login(url)
        return jsonify({"result": reel_row})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Welcome to the Instagram Reel API (no login)!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
