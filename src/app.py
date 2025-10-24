import os
from flask import Flask, jsonify, Response
from threading import Lock

app = Flask(__name__)

# -----------------------
# VISITOR COUNTER (memory)
# -----------------------
visitor_count = 0
lock = Lock()

def increment_counter():
    global visitor_count
    with lock:
        visitor_count += 1
        return visitor_count

# -----------------------
# MAIN PAGE ROUTE
# -----------------------
@app.route("/", methods=["GET"])
def home():
    current_count = increment_counter()

    # full HTML with bubbles + playlists + counter
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TimmyTime</title>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    min-height: 100vh;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    background: radial-gradient(circle at 20% 20%, #2b003b 0%, #0a001a 70%);
    color: #fff;
    overflow-x: hidden;
    overflow-y: auto;
    position: relative;
  }}

  #bubble-layer {{
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }}

  .bubble {{
    position: absolute;
    width: var(--size);
    height: var(--size);
    left: var(--x);
    top: var(--y);
    border-radius: 50%;
    background: radial-gradient(circle at 40% 40%,
      rgba(255,0,255,0.85) 0%,
      rgba(255,0,140,0.6) 40%,
      rgba(255,140,0,0.5) 70%,
      rgba(0,0,0,0) 75%
    );
    filter: blur(20px);
    animation: floatUp var(--duration) linear infinite;
  }}

  @keyframes floatUp {{
    0% {{
      transform: translateY(0) scale(1);
      opacity: 1;
    }}
    100% {{
      transform: translateY(-200px) scale(1.1);
      opacity: 0;
    }}
  }}

  .content {{
    position: relative;
    z-index: 2;
    padding: 16px;
    max-width: 100%;
    color: #fff;
    text-shadow: 0 0 12px rgba(255,0,255,0.6),
                 0 0 22px rgba(255,128,0,0.4);
    line-height: 1.25;
    font-weight: 600;
  }}

  .top-bar {{
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }}

  .left-col {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 1.1rem;
  }}

  .app-name {{
    font-size: 1.4rem;
    font-weight: 700;
  }}

  .visitors {{
    font-size: 1.2rem;
    font-weight: 700;
  }}

  .playlist-row {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    font-size: 1.1rem;
    font-weight: 600;
    text-decoration: underline;
    color: #8da0ff;
    row-gap: 4px;
    column-gap: 12px;
  }}

  .playlist-row a {{
    color: #8da0ff;
  }}

  .tracks {{
    margin-top: 8px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
  }}

  .track-title {{
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
  }}

  .feature-link {{
    font-size: 1.3rem;
    font-weight: 600;
    text-decoration: underline;
    color: #8da0ff;
  }}

  .tagline {{
    margin-top: 8px;
    font-size: 1.2rem;
    font-weight: 600;
    color: rgba(255,255,255,0.8);
    text-shadow: 0 0 8px rgba(255,0,255,0.6),
                 0 0 16px rgba(255,128,0,0.4);
  }}

  .glass-wrap {{
    background: rgba(0,0,0,0.28);
    -webkit-backdrop-filter: blur(6px);
    backdrop-filter: blur(6px);
    border-radius: 12px;
    padding: 12px 14px 16px;
    max-width: 100%;
    box-shadow: 0 20px 60px rgba(255,0,255,0.2),
                0 0 120px rgba(255,128,0,0.4) inset;
  }}

  .spacer {{
    height: 120vh;
  }}

  a {{
    -webkit-tap-highlight-color: rgba(255,255,255,0.2);
  }}
</style>
</head>
<body>

<div id="bubble-layer"></div>

<div class="content">
  <div class="glass-wrap">

    <div class="top-bar">
      <div class="left-col">
        <div class="app-name">TimmyTime</div>

        <div class="visitors">Visitors: <span id="visitorCount">{current_count}</span></div>

        <div class="playlist-row">
          <a href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b" target="_blank" rel="noopener noreferrer">
            Playlist 1
          </a>

          <a href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f" target="_blank" rel="noopener noreferrer">
            Playlist 2
          </a>

          <a href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44" target="_blank" rel="noopener noreferrer">
            Playlist 3
          </a>

          <a href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df" target="_blank" rel="noopener noreferrer">
            Playlist 4
          </a>

          <a href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2" target="_blank" rel="noopener noreferrer">
            Playlist 5
          </a>
        </div>
      </div>
    </div>

    <div class="tracks">
      <div class="track-title">Single Track</div>

      <a class="feature-link"
         href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d"
         target="_blank"
         rel="noopener noreferrer">
        Feature Track
      </a>
    </div>

    <div class="tagline">
      App made by iPhone 17 Pro Max • Timmy Bubbles
    </div>

  </div>
</div>

<div class="spacer"></div>

<script>
(function makeBubbles() {{
  const layer = document.getElementById('bubble-layer');
  const BUBBLE_COUNT = 40;

  function randPct() {{
    return (Math.random() * 100) + '%';
  }}

  function rand(min, max) {{
    return min + Math.random() * (max - min);
  }}

  for (let i = 0; i < BUBBLE_COUNT; i++) {{
    const b = document.createElement('div');
    b.className = 'bubble';

    const size = rand(70, 220);
    const duration = rand(6, 14);

    b.style.setProperty('--size', size + 'px');
    b.style.setProperty('--x', randPct());
    b.style.setProperty('--y', randPct());
    b.style.setProperty('--duration', duration + 's');

    layer.appendChild(b);
  }}
}})();
</script>

</body>
</html>
"""
    return Response(html, mimetype="text/html")


# -------------
# API for count
# -------------
@app.route("/count", methods=["GET"])
def get_count():
    with lock:
        return jsonify({"count": visitor_count})


# -------------
# MAIN EXECUTE
# -------------
if __name__ == "__main__":
    # Render gives us a PORT env var. Default to 10000 locally.
    port = int(os.environ.get("PORT", 10000))
    # MUST listen on 0.0.0.0 so Render can reach it
    app.run(host="0.0.0.0", port=port)
