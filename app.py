from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram Video Downloader</title>

<style>
body{
margin:0;
font-family:Arial;
background:#f5f5f5;
}

/* HEADER */
.header{
background:linear-gradient(90deg,#0066ff,#00bfff);
color:#fff;
padding:15px 20px;
display:flex;
justify-content:space-between;
align-items:center;
font-size:18px;
font-weight:bold;
box-shadow:0 3px 10px rgba(0,0,0,0.2);
}

/* MENU */
.menu{position:relative;}
.menu-btn{cursor:pointer;font-size:24px;}
.menu-content{
display:none;
position:absolute;
right:0;
top:45px;
background:#222;
border-radius:8px;
min-width:180px;
overflow:hidden;
z-index:999;
}
.menu-content a{
display:block;
padding:10px;
color:#fff;
text-decoration:none;
border-bottom:1px solid #333;
}
.menu-content a:hover{
background:#0066ff;
}

/* TITLE */
.title-box{text-align:center;padding:20px 10px 5px;}
.title-box h1{font-size:22px;margin:0;color:#111;}
.title-box p{color:#555;font-size:14px;margin-top:5px;}

/* ADS */
.ad{
background:#e4e6eb;
margin:15px;
padding:15px;
text-align:center;
border-radius:8px;
color:#777;
font-weight:bold;
}

/* MAIN BOX */
.container{
max-width:420px;
margin:20px auto;
background:#fff;
padding:20px;
border-radius:10px;
box-shadow:0 0 15px rgba(0,0,0,0.1);
}

input{
width:100%;
padding:12px;
border:1px solid #ccc;
border-radius:6px;
}

button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:6px;
background:linear-gradient(90deg,#0066ff,#00bfff);
color:#fff;
font-weight:bold;
font-size:15px;
cursor:pointer;
transition:0.3s;
}

button:hover{
opacity:0.9;
}

/* RESULT */
.result{margin-top:15px;text-align:center;}

.qbtn{
display:inline-block;
margin:5px;
padding:8px 16px;
background:#111;
color:#fff;
border-radius:25px;
font-size:13px;
cursor:pointer;
transition:0.3s;
}

.qbtn:hover{
background:#0066ff;
}

/* CONTENT */
.content{
max-width:800px;
margin:20px auto;
background:#fff;
padding:20px;
border-radius:10px;
line-height:1.6;
color:#111;
}

/* FOOTER */
.footer{
background:#111;
color:#aaa;
text-align:center;
padding:25px;
margin-top:20px;
font-size:14px;
}

.footer a{
color:#00bfff;
text-decoration:none;
margin:0 5px;
}

.page{display:none;}
.active{display:block;}

.contact-form{
display:flex;
flex-direction:column;
}

.contact-form input,
.contact-form textarea{
margin-bottom:10px;
padding:10px;
border:1px solid #ccc;
border-radius:6px;
}

.contact-form button{
background:#0066ff;
color:#fff;
font-weight:bold;
}
</style>
</head>

<body>

<!-- HEADER -->
<div class="header">
<span>📥 Instagram Downloader</span>
<div class="menu">
<span class="menu-btn" onclick="toggleMenu()">⋮</span>
<div class="menu-content" id="menu">
<a href="#" onclick="showPage('home')">Home</a>
<a href="#" onclick="showPage('privacy')">Privacy Policy</a>
<a href="#" onclick="showPage('terms')">Terms & Conditions</a>
<a href="#" onclick="showPage('contact')">Contact</a>
</div>
</div>
</div>

<!-- HOME -->
<div id="home" class="page active">
<div class="title-box">
<h1>Download Instagram Videos Fast & Secure</h1>
<p>Paste your Instagram video link below and download instantly.</p>
</div>

<div class="ad">Top Ad Space</div>

<div class="container">
<input type="text" id="url" placeholder="Paste Instagram Video Link">
<button onclick="getVideo()">Download Video</button>
<div id="result" class="result"></div>
</div>

<div class="ad">Middle Ad Space</div>

<div class="content">
<h2>About This Tool</h2>
<p>This Instagram Video Downloader allows you to download Instagram videos, reels, and IGTV in high quality. It is fast, secure, and works on all devices.</p>

<h2>How to Use</h2>
<ul>
<li>Copy Instagram video link</li>
<li>Paste it above</li>
<li>Select quality and download</li>
</ul>

<p>This tool is for personal use only.</p>
</div>
</div>

<!-- PRIVACY -->
<div id="privacy" class="page content">
<h2>Privacy Policy</h2>
<p>We do not store any personal data. All downloads are processed securely.</p>
</div>

<!-- TERMS -->
<div id="terms" class="page content">
<h2>Terms & Conditions</h2>
<p>This tool is for personal and educational use only. Users are responsible for usage.</p>
</div>

<!-- CONTACT -->
<div id="contact" class="page content">
<h2>Contact Us</h2>
<form class="contact-form">
<input type="text" placeholder="Your Name" required>
<input type="email" placeholder="Your Email" required>
<textarea placeholder="Your Message" rows="5" required></textarea>
<button type="submit">Send Message</button>
</form>
</div>

<!-- FOOTER -->
<div class="footer">
© 2026 Instagram Downloader |
<a href="#" onclick="showPage('privacy')">Privacy</a> |
<a href="#" onclick="showPage('terms')">Terms</a> |
<a href="#" onclick="showPage('contact')">Contact</a>
</div>

<script>
function toggleMenu(){
let m = document.getElementById("menu");
m.style.display = (m.style.display=="block")?"none":"block";
}

function showPage(id){
document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
document.getElementById(id).classList.add("active");
window.scrollTo(0,0);
}

async function getVideo(){
let url = document.getElementById("url").value;
let result = document.getElementById("result");

if(!url){
alert("Paste link first");
return;
}

result.innerHTML = "Processing...";

try{
let res = await fetch("/analyze",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({url:url})
});

let data = await res.json();

if(data.success){
let html = "<h3>Select Quality:</h3>";
data.links.forEach(v=>{
html += `<span class="qbtn" onclick="downloadVideo('${v.url}')">${v.quality}</span>`;
});
result.innerHTML = html;
}else{
result.innerHTML = "Video not found";
}

}catch(e){
result.innerHTML = "Server error";
}
}

function downloadVideo(link){
let a=document.createElement("a");
a.href=link;
a.setAttribute("download","video.mp4");
document.body.appendChild(a);
a.click();
a.remove();
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_UI)

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json.get("url")
    try:
        ydl_opts = {'quiet': True, 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            links = []
            for f in formats:
                if f.get("vcodec") != "none":
                    h = f.get("height", 0)
                    if h >= 2160: q = "4K"
                    elif h >= 1080: q = "1080p"
                    elif h >= 720: q = "HD"
                    else: q = "SD"
                    if not any(x["quality"] == q for x in links):
                        links.append({"quality": q, "url": f["url"]})
            return jsonify({"success": True, "links": links})
    except:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)