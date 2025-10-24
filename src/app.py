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
  * {{ box-sizing:border-box; margin:0; padding:0; }}

  body {{
    min-height:100vh;
    font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;
    /* new background: soft yellow to light blue */
    background: radial-gradient(circle at 20% 20%, rgba(255,255,180,1) 0%, rgba(180,220,255,1) 60%, rgba(20,0,40,1) 100%);
    color:#fff;
    overflow:hidden;
    position:relative;
  }}

  /* bubble layer sits under content */
  #bubble-layer {{
    position:fixed;
    inset:0;
    z-index:0;
    pointer-events:none;
    overflow:hidden;
  }}

  /* bubble visual: tighter, clearer edge */
  .bubble {{
    position:absolute;
    width:var(--size);
    height:var(--size);
    left:var(--x);
    top:var(--y);
    border-radius:50%;
    /* core glow: pink/orange inner, but with a brighter highlight dot
       so it looks like a real bubble catching light */
    background:
      radial-gradient(circle at 30% 30%,
        rgba(255,255,255,0.8) 0%,
        rgba(255,0,255,0.55) 15%,
        rgba(255,128,0,0.4) 55%,
        rgba(0,0,0,0) 75%
      );
    /* less blur so it's sharper on yellow/blue bg */
    filter: blur(8px);
    animation: floatUp var(--duration) linear infinite;
    box-shadow:
      0 0 20px rgba(255,0,255,0.5),
      0 0 40px rgba(255,128,0,0.4);
  }}

  @keyframes floatUp {{
    0%   {{ transform:translateY(0) scale(1);   opacity:0.9; }}
    100% {{ transform:translateY(-150px) scale(1.08); opacity:0; }}
  }}

  /* content card */
  .content {{
    position:relative;
    z-index:2;
    padding:16px;
    display:flex;
    justify-content:center;
  }}

  .glass-wrap {{
    width:calc(100% - 32px);
    max-width:730px;
    background:rgba(0,0,0,0.32);
    -webkit-backdrop-filter:blur(12px);
    backdrop-filter:blur(12px);
    border-radius:20px;
    padding:20px 24px;
    box-shadow:
      0 30px 80px rgba(255,0,255,0.25),
      0 0 160px rgba(255,128,0,0.35) inset;
    border:1px solid rgba(255,0,255,0.25);
    color:#fff;
  }}

  .app-name {{
    font-size:2rem;
    font-weight:800;
    line-height:1.15;
    color:#fff;
    text-shadow:
      0 0 12px rgba(255,0,255,0.8),
      0 0 24px rgba(255,128,0,0.5);
  }}

  .visitors {{
    font-size:1.3rem;
    font-weight:700;
    line-height:1.3;
    color:#fff;
    text-shadow:
      0 0 10px rgba(255,0,255,0.7),
      0 0 20px rgba(255,128,0,0.4);
    margin-top:8px;
    margin-bottom:12px;
  }}

  /* playlists row: same 2-row layout you like */
  .playlist-grid {{
    display:flex;
    flex-wrap:wrap;
    row-gap:12px;
    column-gap:24px;
    font-size:1.1rem;
    font-weight:700;
    line-height:1.25;
  }}

  .playlist-grid a {{
    color:#9bb5ff;
    text-decoration:underline;
    text-shadow:
      0 0 10px rgba(155,181,255,.6),
      0 0 30px rgba(255,0,255,.4);
  }}

  /* "Single Track" header */
  .track-title {{
    font-size:2rem;
    font-weight:800;
    line-height:1.15;
    color:#fff;
    text-shadow:
      0 0 12px rgba(255,0,255,0.8),
      0 0 24px rgba(255,128,0,0.5);
    margin-top:20px;
  }}

  .tagline {{
    margin-top:16px;
    font-size:1.2rem;
    font-weight:700;
    line-height:1.3;
    color:#fff;
    text-shadow:
      0 0 8px rgba(255,0,255,0.6),
      0 0 16px rgba(255,128,0,0.4);
  }}
</style>
</head>
<body>

<div id="bubble-layer"></div>

<div class="content">
  <div class="glass-wrap">
    <div class="app-name">TimmyTime</div>
    <div class="visitors">Visitors: <span id="visitorCount">{current_count}</span></div>

    <div class="playlist-grid">
      <a href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b" target="_blank" rel="noopener noreferrer">Playlist 1</a>
      <a href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f" target="_blank" rel="noopener noreferrer">Playlist 2</a>
      <a href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44" target="_blank" rel="noopener noreferrer">Playlist 3</a>
      <a href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df" target="_blank" rel="noopener noreferrer">Playlist 4</a>
      <a href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2" target="_blank" rel="noopener noreferrer">Playlist 5</a>
      <a href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d" target="_blank" rel="noopener noreferrer">Feature Track</a>
    </div>

    <div class="track-title">Single Track</div>

    <div class="tagline">
      App made by iPhone 17 Pro Max • Timmy Bubbles
    </div>
  </div>
</div>

<script>
(function makeBubbles(){{
  const layer=document.getElementById('bubble-layer');
  const COUNT=40;

  function rpct(){{return (Math.random()*100)+'%';}}
  function rand(a,b){{return a+Math.random()*(b-a);}}

  for(let i=0;i<COUNT;i++) {{
    const b=document.createElement('div');
    b.className='bubble';

    const size=rand(40,90);      // smaller bubbles
    const dur=rand(8,18);        // easy float

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
