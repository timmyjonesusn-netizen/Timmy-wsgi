import os
from flask import Flask, jsonify, Response
from threading import Lock

app = Flask(__name__)

visitor_count = 0
lock = Lock()

def increment_counter():
    global visitor_count
    with lock:
        visitor_count += 1
        return visitor_count

@app.route("/", methods=["GET"])
def home():
    current_count = increment_counter()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TimmyTime</title>
<style>
  * {{box-sizing:border-box;margin:0;padding:0}}
  body {{
    min-height:100vh;
    font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;
    background:radial-gradient(circle at 20% 20%,#2b003b 0%,#0a001a 70%);
    color:#fff;overflow:hidden;position:relative;
  }}
  #bubble-layer {{position:fixed;inset:0;z-index:0;pointer-events:none}}
  .bubble {{
    position:absolute;border-radius:50%;
    width:var(--size);height:var(--size);
    left:var(--x);top:var(--y);
    background:radial-gradient(circle at 40% 40%,
      rgba(255,0,255,0.55) 0%,
      rgba(255,128,0,0.35) 60%,
      rgba(0,0,0,0) 80%);
    filter:blur(15px);
    animation:floatUp var(--duration) linear infinite;
  }}
  @keyframes floatUp {{
    0%{{transform:translateY(0)scale(1);opacity:.9}}
    100%{{transform:translateY(-150px)scale(1.1);opacity:0}}
  }}
  .content {{position:relative;z-index:2;padding:16px;display:flex;justify-content:center}}
  .glass-wrap {{
    width:calc(100%-32px);max-width:730px;
    background:rgba(0,0,0,.25);
    -webkit-backdrop-filter:blur(12px);
    backdrop-filter:blur(12px);
    border-radius:20px;padding:20px 24px;
    box-shadow:0 30px 80px rgba(255,0,255,.25),
               0 0 160px rgba(255,128,0,.35) inset;
    border:1px solid rgba(255,0,255,.25);
  }}
  .app-name {{font-size:2rem;font-weight:800;text-shadow:0 0 12px rgba(255,0,255,.8)}}
  .visitors {{font-size:1.3rem;font-weight:700}}
  .playlist-grid {{
    display:flex;flex-wrap:wrap;gap:16px;
    font-size:1.1rem;font-weight:700
  }}
  .playlist-grid a {{
    color:#9bb5ff;text-decoration:underline;
    text-shadow:0 0 10px rgba(155,181,255,.6)
  }}
  .track-title {{font-size:2rem;font-weight:800;margin-top:10px}}
  .tagline {{margin-top:12px;font-size:1.2rem;font-weight:700;
    text-shadow:0 0 8px rgba(255,0,255,.6)}}
</style>
</head>
<body>
<div id="bubble-layer"></div>
<div class="content">
  <div class="glass-wrap">
    <div class="app-name">TimmyTime</div>
    <div class="visitors">Visitors: <span id="visitorCount">{current_count}</span></div>

    <div class="playlist-grid">
      <a href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b" target="_blank">Playlist 1</a>
      <a href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f" target="_blank">Playlist 2</a>
      <a href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44" target="_blank">Playlist 3</a>
      <a href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df" target="_blank">Playlist 4</a>
      <a href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2" target="_blank">Playlist 5</a>
      <a href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d" target="_blank">Feature Track</a>
    </div>

    <div class="track-title">Single Track</div>
    <div class="tagline">App made by iPhone 17 Pro Max • Timmy Bubbles</div>
  </div>
</div>

<script>
(function makeBubbles(){{
  const layer=document.getElementById('bubble-layer');
  const COUNT=40;
  function rpct(){{return Math.random()*100+'%';}}
  function rand(a,b){{return a+Math.random()*(b-a);}}
  for(let i=0;i<COUNT;i++){{
    const b=document.createElement('div');
    b.className='bubble';
    const size=rand(40,90);
    const dur=rand(8,18);
    b.style.setProperty('--size',size+'px');
    b.style.setProperty('--x',rpct());
    b.style.setProperty('--y',rpct());
    b.style.setProperty('--duration',dur+'s');
    layer.appendChild(b);
  }}
}})();
</script>
</body>
</html>"""
    return Response(html, mimetype="text/html")

@app.route("/count")
def get_count():
    with lock:
        return jsonify({"count": visitor_count})

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
