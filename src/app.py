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
  * {{
    box-sizing:border-box;
    margin:0;
    padding:0;
  }}

  /* LAYER 1: full-screen sunrise background */
  body {{
    min-height:100vh;
    font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;
    background: radial-gradient(
      circle at 20% 20%,
      rgba(255,255,180,1) 0%,
      rgba(180,220,255,1) 60%,
      rgba(20,0,40,1) 100%
    );
    color:#fff;
    overflow:hidden;
    position:relative;
  }}

  /* LAYER 2: bubble field above the bg */
  #bubble-layer {{
    position:fixed;
    inset:0;
    z-index:0;
    pointer-events:none;
    overflow:hidden;
  }}

  /* CRYSTAL BUBBLES:
     - bright inner highlight
     - thin rim
     - minimal blur for clarity
     - gentle up + slight sideways drift
  */
  .bubble {{
    position:absolute;
    width:var(--size);
    height:var(--size);
    left:var(--x);
    top:var(--y);
    border-radius:50%;
    background:
      radial-gradient(circle at 30% 30%,
        rgba(255,255,255,0.95) 0%,       /* bright glint highlight */
        rgba(255,0,255,0.6) 20%,         /* hot pink core */
        rgba(255,128,0,0.45) 55%,        /* warm orange band */
        rgba(0,0,0,0) 75%                /* fade out edge */
      );
    /* very light blur just to soften the edge pixels */
    filter: blur(2px);

    /* faint neon aura + subtle dark rim for definition on light bg */
    box-shadow:
      0 0 12px rgba(255,0,255,0.7),
      0 0 24px rgba(255,128,0,0.5),
      0 0 2px rgba(0,0,0,0.6) inset;

    animation: floatDrift var(--duration) linear infinite;
  }}

  /* move up and drift sideways for life */
  @keyframes floatDrift {{
    0%   {{ transform:translate(0,0) scale(1);    opacity:0.95; }}
    100% {{ transform:translate(20px,-160px) scale(1.07); opacity:0; }}
  }}

  /* LAYER 3: the card on top */
  .content {{
    position:relative;
    z-index:2;
    padding:16px;
    display:flex;
    justify-content:center;
  }}

  /* glass card: stay warm/neutral so text is readable */
  .glass-wrap {{
    width:calc(100% - 32px);
    max-width:730px;

    background:
      radial-gradient(circle at 20% 20%,
        rgba(80,0,80,0.45) 0%,
        rgba(60,0,40,0.35) 40%,
        rgba(0,0,0,0) 70%
      ),
      rgba(0,0,0,0.30);

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

  /* HELPER: universal outlined text (white/pink headings) */
  .outlined-light {{
    color:#fff;
    text-shadow:
      0 0 10px rgba(255,0,255,0.7),
      0 0 20px rgba(255,128,0,0.4),
      /* black stroke around edges for pop */
      -1px -1px 0 rgba(0,0,0,1),
       1px -1px 0 rgba(0,0,0,1),
      -1px  1px 0 rgba(0,0,0,1),
       1px  1px 0 rgba(0,0,0,1);
  }}

  /* HELPER: outlined link text (blue links) */
  .outlined-link {{
    color:#9bb5ff;
    text-decoration:underline;
    text-shadow:
      0 0 6px rgba(155,181,255,.6),
      0 0 16px rgba(255,0,255,.4),
      -1px -1px 0 rgba(0,0,0,1),
       1px -1px 0 rgba(0,0,0,1),
      -1px  1px 0 rgba(0,0,0,1),
       1px  1px 0 rgba(0,0,0,1);
  }}

  .app-name {{
    font-size:2rem;
    font-weight:800;
    line-height:1.15;
  }}

  .visitors {{
    font-size:1.3rem;
    font-weight:700;
    line-height:1.3;
    margin-top:8px;
    margin-bottom:16px;
  }}

  .playlist-grid {{
    display:flex;
    flex-wrap:wrap;
    row-gap:12px;
    column-gap:24px;
    font-size:1.1rem;
    font-weight:700;
    line-height:1.25;
  }}

  .feature-track {{
    width:100%;
    font-size:1.1rem;
    font-weight:700;
    line-height:1.25;
    margin-top:16px;
  }}

  .track-title {{
    font-size:2rem;
    font-weight:800;
    line-height:1.15;
    margin-top:24px;
  }}

  .tagline {{
    margin-top:16px;
    font-size:1.2rem;
    font-weight:700;
    line-height:1.3;
  }}
</style>
</head>
<body>

<!-- bubbles under card -->
<div id="bubble-layer"></div>

<div class="content">
  <div class="glass-wrap">

    <div class="app-name outlined-light">TimmyTime</div>

    <div class="visitors outlined-light">
      Visitors: <span id="visitorCount">{current_count}</span>
    </div>

    <div class="playlist-grid">
      <a class="outlined-link"
         href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b"
         target="_blank" rel="noopener noreferrer">Playlist 1</a>

      <a class="outlined-link"
         href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f"
         target="_blank" rel="noopener noreferrer">Playlist 2</a>

      <a class="outlined-link"
         href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44"
         target="_blank" rel="noopener noreferrer">Playlist 3</a>

      <a class="outlined-link"
         href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df"
         target="_blank" rel="noopener noreferrer">Playlist 4</a>

      <a class="outlined-link"
         href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2"
         target="_blank" rel="noopener noreferrer">Playlist 5</a>
    </div>

    <div class="feature-track">
      <a class="outlined-link"
         href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d"
         target="_blank" rel="noopener noreferrer">Feature Track</a>
    </div>

    <div class="track-title outlined-light">Single Track</div>

    <div class="tagline outlined-light">
      App made by iPhone 17 Pro Max • Timmy Bubbles
    </div>

  </div>
</div>

<script>
(function makeBubbles(){{
  const layer = document.getElementById('bubble-layer');
  const COUNT = 40;

  function rpct() {{ return (Math.random()*100)+'%'; }}
  function rand(a,b) {{ return a + Math.random()*(b-a); }}

  for (let i=0; i<COUNT; i++) {{
    const b = document.createElement('div');
    b.className = 'bubble';

    // tighter size range = more "defined beads"
    const size = rand(40, 90);
    const dur  = rand(10, 20); // slower float for elegance

    b.style.setProperty('--size', size + 'px');
    b.style.setProperty('--x', rpct());
    b.style.setProperty('--y', rpct());
    b.style.setProperty('--duration', dur + 's');

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
