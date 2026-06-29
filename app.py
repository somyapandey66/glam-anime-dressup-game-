!pip install gradio google-generativeai matplotlib pillow
import google.generativeai as genai
GEMINI_API_KEY = "your_gemini_api_key_here"  
genai.configure(api_key=GEMINI_API_KEY)
print("✅ API Key set!")
import gradio as gr
import google.generativeai as genai
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, FancyArrowPatch
import numpy as np
import io
from PIL import Image

# ── Draw anime character ─────────────────────────────────────────────────────
def draw_character(skin_done=False, makeup=None, outfit=None):
    fig, ax = plt.subplots(1, 1, figsize=(5, 8))
    fig.patch.set_facecolor('#1a0033')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Background sparkles
    for _ in range(30):
        x, y = np.random.uniform(0, 10), np.random.uniform(0, 16)
        ax.plot(x, y, '*', color=np.random.choice(['#FFD700','#FF69B4','#DA70D6','#fff']),
                markersize=np.random.uniform(2, 6), alpha=0.5)

    # Skin tone
    skin_color = '#FFE4C4' if not skin_done else '#FFDAB9'
    glow_color = '#FFD700' if skin_done else None

    # Glow aura if skincare done
    if skin_done:
        glow = Ellipse((5, 10.5), 4.5, 6, color='#FFD70022', zorder=0)
        ax.add_patch(glow)

    # OUTFIT / BODY
    outfit_colors = {
        "Sparkling Ball Gown 💎": ('#9B59B6', '#D7BDE2'),
        "Sleek Satin Slip 🌙":    ('#2C3E50', '#85C1E9'),
        "Floral Fairy Dress 🌸":  ('#FF85A1', '#FFD1DC'),
        "Power Suit Glam 💼":     ('#1C2833', '#F0B27A'),
        "Sequin Mini Dress 🪩":   ('#C0392B', '#F1948A'),
        "Royal Velvet Gown 👑":   ('#154360', '#A9CCE3'),
    }
    body_color = '#E91E93' if outfit is None else outfit_colors.get(outfit, ('#E91E93','#F48FB1'))[0]
    accent_color = '#FF69B4' if outfit is None else outfit_colors.get(outfit, ('#E91E93','#F48FB1'))[1]

    # Dress / body
    dress = plt.Polygon([[3,5],[7,5],[8,2],[2,2]], color=body_color, zorder=3)
    ax.add_patch(dress)
    # Dress shine
    shine = plt.Polygon([[4.5,5],[5.5,5],[6,2],[4,2]], color=accent_color, alpha=0.4, zorder=4)
    ax.add_patch(shine)
    # Bodice
    bodice = FancyBboxPatch((3.8, 5), 2.4, 1.8, boxstyle="round,pad=0.1", color=body_color, zorder=3)
    ax.add_patch(bodice)

    # Sparkles on dress if outfit chosen
    if outfit:
        for _ in range(12):
            sx, sy = np.random.uniform(2.5, 7.5), np.random.uniform(2.2, 6.5)
            ax.plot(sx, sy, '*', color='#FFD700', markersize=5, alpha=0.8, zorder=5)

    # NECK
    neck = FancyBboxPatch((4.6, 6.7), 0.8, 0.7, color=skin_color, zorder=4)
    ax.add_patch(neck)

    # HEAD
    head = Ellipse((5, 8.5), 3.2, 3.5, color=skin_color, zorder=5)
    ax.add_patch(head)

    # HAIR (anime style)
    hair_color = '#1a0010'
    # Main hair top
    hair_top = Ellipse((5, 9.8), 3.4, 2, color=hair_color, zorder=4)
    ax.add_patch(hair_top)
    # Side hair left
    side_l = plt.Polygon([[2.1,8],[3.5,6.5],[3.2,9.5]], color=hair_color, zorder=4)
    ax.add_patch(side_l)
    # Side hair right
    side_r = plt.Polygon([[7.9,8],[6.5,6.5],[6.8,9.5]], color=hair_color, zorder=4)
    ax.add_patch(side_r)
    # Hair bangs
    bangs = plt.Polygon([[3.3,9.2],[6.7,9.2],[6.2,8],[4.8,7.8],[3.8,8]], color=hair_color, zorder=6)
    ax.add_patch(bangs)

    # Hair highlight
    highlight = Ellipse((4.5, 9.8), 0.5, 0.3, color='#555', alpha=0.5, zorder=7)
    ax.add_patch(highlight)

    # MAKEUP EYES
    eye_color = '#1a1a2e'
    makeup_colors = {
        "Natural Glow 🌿":    ('#7DCEA0', '#A9DFBF'),
        "Soft Glam ✨":       ('#F9E79F', '#FAD7A0'),
        "Bold Red Lip 💋":    ('#E74C3C', '#F1948A'),
        "Smoky Eye 🖤":       ('#2C3E50', '#717D7E'),
        "Kawaii Blush 🍑":    ('#FDEBD0', '#F9C0C0'),
        "Full Glam Queen 👸": ('#8E44AD', '#D2B4DE'),
    }
    iris_color = '#6C3483' if makeup is None else makeup_colors.get(makeup, ('#6C3483','#D2B4DE'))[0]
    shadow_color = '#B7950B' if makeup is None else makeup_colors.get(makeup, ('#6C3483','#D2B4DE'))[1]

    # Eye shadow
    if makeup:
        lshadow = Ellipse((3.8, 8.4), 1.0, 0.4, color=shadow_color, alpha=0.6, zorder=6)
        rshadow = Ellipse((6.2, 8.4), 1.0, 0.4, color=shadow_color, alpha=0.6, zorder=6)
        ax.add_patch(lshadow)
        ax.add_patch(rshadow)

    # Eyes whites
    leye = Ellipse((3.8, 8.2), 0.9, 0.7, color='white', zorder=7)
    reye = Ellipse((6.2, 8.2), 0.9, 0.7, color='white', zorder=7)
    ax.add_patch(leye); ax.add_patch(reye)
    # Iris
    liris = Circle((3.8, 8.2), 0.32, color=iris_color, zorder=8)
    riris = Circle((6.2, 8.2), 0.32, color=iris_color, zorder=8)
    ax.add_patch(liris); ax.add_patch(riris)
    # Pupil
    lpupil = Circle((3.85, 8.2), 0.15, color='#0a0010', zorder=9)
    rpupil = Circle((6.25, 8.2), 0.15, color='#0a0010', zorder=9)
    ax.add_patch(lpupil); ax.add_patch(rpupil)
    # Eye shine
    ax.plot(3.7, 8.32, 'o', color='white', markersize=4, zorder=10)
    ax.plot(6.1, 8.32, 'o', color='white', markersize=4, zorder=10)
    # Lashes
    for lx in [3.3, 3.5, 3.7, 3.9, 4.1, 4.3]:
        ax.plot([lx, lx-0.05], [8.58, 8.78], color='#0a0010', linewidth=1.5, zorder=10)
    for rx in [5.7, 5.9, 6.1, 6.3, 6.5, 6.7]:
        ax.plot([rx, rx-0.05], [8.58, 8.78], color='#0a0010', linewidth=1.5, zorder=10)

    # EYEBROWS
    ax.plot([3.3, 4.3], [8.85, 8.9], color='#1a0010', linewidth=2.5, zorder=10)
    ax.plot([5.7, 6.7], [8.9, 8.85], color='#1a0010', linewidth=2.5, zorder=10)

    # NOSE
    ax.plot([5.0, 4.85], [7.7, 7.55], color='#c8956c', linewidth=1, zorder=9)
    ax.plot([4.85, 5.05], [7.55, 7.55], color='#c8956c', linewidth=1, zorder=9)

    # LIPS / MOUTH
    lip_color = '#E74C3C' if (makeup and 'Red' in makeup) else '#E88FA0'
    lip_color = '#9B59B6' if (makeup and 'Glam Queen' in makeup) else lip_color
    mouth = Ellipse((5, 7.25), 0.9, 0.38, color=lip_color, zorder=9)
    ax.add_patch(mouth)
    # Upper lip line
    ax.plot([4.55, 5.0], [7.3, 7.38], color='#c0392b', linewidth=1, zorder=10)
    ax.plot([5.0, 5.45], [7.38, 7.3], color='#c0392b', linewidth=1, zorder=10)

    # BLUSH
    if makeup and ('Kawaii' in makeup or 'Glam' in makeup or 'Soft' in makeup):
        lblush = Ellipse((3.4, 7.85), 0.9, 0.4, color='#FFB6C1', alpha=0.5, zorder=8)
        rblush = Ellipse((6.6, 7.85), 0.9, 0.4, color='#FFB6C1', alpha=0.5, zorder=8)
        ax.add_patch(lblush); ax.add_patch(rblush)

    # ARMS
    larm = FancyBboxPatch((2.2, 5.2), 0.7, 2, boxstyle="round,pad=0.2", color=skin_color, zorder=3)
    rarm = FancyBboxPatch((7.1, 5.2), 0.7, 2, boxstyle="round,pad=0.2", color=skin_color, zorder=3)
    ax.add_patch(larm); ax.add_patch(rarm)

    # Crown if outfit is Royal
    if outfit and 'Royal' in outfit:
        crown_pts = [[4.0,10.6],[4.3,11.3],[5.0,10.8],[5.7,11.3],[6.0,10.6]]
        crown = plt.Polygon(crown_pts, color='#FFD700', zorder=11)
        ax.add_patch(crown)
        ax.plot(5.0, 11.1, '*', color='#FF0000', markersize=10, zorder=12)

    # Stage label
    stage_text = ""
    if not skin_done:
        stage_text = "🌸 Before Skincare"
    elif skin_done and makeup is None:
        stage_text = "✨ Skincare Done!"
    elif makeup and outfit is None:
        stage_text = f"💄 {makeup}"
    elif outfit:
        stage_text = f"👑 Ready for Contest!"

    ax.text(5, 1.2, stage_text, ha='center', va='center', fontsize=11,
            color='#FFD700', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a0033', edgecolor='#FFD700', alpha=0.8))

    ax.text(5, 15.5, "✨ Glam Anime Dress-Up ✨", ha='center', fontsize=13,
            color='#FF69B4', fontweight='bold')

    plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#1a0033')
    plt.close()
    buf.seek(0)
    return Image.open(buf)


# ── AI Beauty Contest Judge ──────────────────────────────────────────────────
def get_ai_score(skincare, makeup, outfit):
    skincare_list = ', '.join(skincare) if skincare else 'nothing'
    prompt = f"""You are a DRAMATIC and glamorous anime beauty contest judge on a glitzy runway show.

The contestant chose:
- Skincare: {skincare_list}
- Makeup: {makeup}
- Outfit: {outfit}

Give scores (each out of 100) for Glow, Glam, and Style.
Then write a dramatic 3-sentence verdict — be expressive and fun!
Give her a fabulous queen title.

Use EXACTLY this format (no extra text):
✨ GLOW SCORE: [number]/100
💄 GLAM SCORE: [number]/100
👗 STYLE SCORE: [number]/100
⭐ TOTAL: [sum]/300

👑 TITLE: [creative queen title]

📢 VERDICT: [3 dramatic sentences about her look]

🏆 WINNER STATUS: [either "CROWNED CHAMPION! 👑" or "Runner-Up 🌸" based on total score above 230]
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ API Error: {str(e)}\n\nMake sure your Gemini API key is correct in Cell 2!"


# ── State storage ─────────────────────────────────────────────────────────────
state = {"skincare": [], "makeup": None, "outfit": None}


# ── Gradio App ────────────────────────────────────────────────────────────────
with gr.Blocks(
    title="✨ Glam Anime Dress-Up Game",
    theme=gr.themes.Base(),
    css="""
    body { background: #1a0033 !important; }
    .gradio-container { background: linear-gradient(135deg, #1a0033, #3d0066) !important; }
    h1, h2, h3, label { color: #FFD700 !important; }
    .gr-button-primary { background: linear-gradient(90deg,#E91E93,#9B59B6) !important; color: white !important; font-weight: bold !important; border: none !important; }
    .gr-button { background: #3d0066 !important; color: #FFD700 !important; border: 1px solid #FFD700 !important; }
    """
) as game:

    gr.Markdown("# 👑 ✨ Glam Anime Dress-Up & Beauty Contest ✨ 👑")
    gr.Markdown("### Transform your anime girl and win the runway! 💖")

    with gr.Row():
        # Left: Character display
        with gr.Column(scale=1):
            char_img = gr.Image(
                value=draw_character(),
                label="Your Anime Girl",
                show_download_button=False,
                interactive=False,
                height=500
            )

        # Right: Game panels
        with gr.Column(scale=1):

            # Stage 1
            with gr.Group(visible=True) as s1:
                gr.Markdown("## 🌸 Stage 1: Skincare Routine")
                gr.Markdown("Pick products to get that glass-skin glow!")
                skincare_input = gr.CheckboxGroup(
                    choices=["Gentle Cleanser 🧴","Rose Toner 🌹","Vitamin C Serum ✨",
                             "Hyaluronic Moisturizer 💧","SPF Sunscreen ☀️","Eye Cream 👁️"],
                    label="Choose skincare products (pick at least 1)"
                )
                err1 = gr.Markdown("")
                btn1 = gr.Button("Next: Makeup 💄 →", variant="primary", size="lg")

            # Stage 2
            with gr.Group(visible=False) as s2:
                gr.Markdown("## 💄 Stage 2: Makeup Look")
                gr.Markdown("Choose your signature style!")
                makeup_input = gr.Radio(
                    choices=["Natural Glow 🌿","Soft Glam ✨","Bold Red Lip 💋",
                             "Smoky Eye 🖤","Kawaii Blush 🍑","Full Glam Queen 👸"],
                    label="Pick your makeup look"
                )
                err2 = gr.Markdown("")
                btn2 = gr.Button("Next: Outfit 👗 →", variant="primary", size="lg")

            # Stage 3
            with gr.Group(visible=False) as s3:
                gr.Markdown("## 👗 Stage 3: Choose Your Dress")
                gr.Markdown("Pick the dress that slays the runway!")
                outfit_input = gr.Radio(
                    choices=["Sparkling Ball Gown 💎","Sleek Satin Slip 🌙",
                             "Floral Fairy Dress 🌸","Power Suit Glam 💼",
                             "Sequin Mini Dress 🪩","Royal Velvet Gown 👑"],
                    label="Pick your outfit"
                )
                err3 = gr.Markdown("")
                btn3 = gr.Button("🏆 Enter Beauty Contest! →", variant="primary", size="lg")

            # Results
            with gr.Group(visible=False) as s_result:
                gr.Markdown("## 🏆 Beauty Contest Results!")
                result_text = gr.Markdown("")
                btn_restart = gr.Button("🔄 Play Again!", size="lg")

    # ── Button functions ──────────────────────────────────────────────────────
    def do_stage1(skincare):
        if not skincare:
            return (gr.update(visible=True), gr.update(visible=False),
                    gr.update(visible=False), gr.update(visible=False),
                    "⚠️ Please pick at least one skincare product!", draw_character())
        img = draw_character(skin_done=True)
        return (gr.update(visible=False), gr.update(visible=True),
                gr.update(visible=False), gr.update(visible=False), "", img)

    def do_stage2(skincare, makeup):
        if not makeup:
            return (gr.update(visible=False), gr.update(visible=True),
                    gr.update(visible=False), gr.update(visible=False),
                    "⚠️ Please choose a makeup look!", draw_character(skin_done=True))
        img = draw_character(skin_done=True, makeup=makeup)
        return (gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=True), gr.update(visible=False), "", img)

    def do_stage3(skincare, makeup, outfit):
        if not outfit:
            return (gr.update(visible=False), gr.update(visible=False),
                    gr.update(visible=True), gr.update(visible=False),
                    "⚠️ Please choose an outfit!", draw_character(skin_done=True, makeup=makeup), "")
        img = draw_character(skin_done=True, makeup=makeup, outfit=outfit)
        score = get_ai_score(skincare, makeup, outfit)
        return (gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=True), "", img, score)

    def do_restart():
        return (gr.update(visible=True), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=False),
                [], None, None, "", "", draw_character())

    btn1.click(do_stage1,
               inputs=[skincare_input],
               outputs=[s1, s2, s3, s_result, err1, char_img])

    btn2.click(do_stage2,
               inputs=[skincare_input, makeup_input],
               outputs=[s1, s2, s3, s_result, err2, char_img])

    btn3.click(do_stage3,
               inputs=[skincare_input, makeup_input, outfit_input],
               outputs=[s1, s2, s3, s_result, err3, char_img, result_text])

    btn_restart.click(do_restart,
                      outputs=[s1, s2, s3, s_result,
                                skincare_input, makeup_input, outfit_input,
                                err1, err2, char_img])

game.launch(share=True, debug=True)
