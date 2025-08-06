import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# === CONFIG ===
FONT_BOLD_ITALIC = "fonts/Montserrat-ExtraBoldItalic.ttf"
FONT_BOLD = "fonts/Montserrat-ExtraBold.ttf"
FONT_REGULAR = "fonts/Montserrat-Regular.ttf"
FONT_SEMIBOLD = "fonts/Montserrat-SemiBold.ttf"

st.set_page_config(page_title="Job Image Generator")
st.title("📌 Job Post Image Designer")

# === Select Variant ===
variant = st.selectbox("Choose Image Variant", ["Variant 1", "Variant 2", "Variant 3"])

# === Load Template and Settings Based on Variant ===
if variant == "Variant 1":
    TEMPLATE_PATH = "./template/2.png"
    template = Image.open(TEMPLATE_PATH)

    role_x, role_y, role_font_size = 210, 1050, 150
    skills_x, skills_y, skills_font_size = 210, 1530, 100
    contact_x, contact_y, contact_font_size = 250, 2450, 50
    email_x, email_y, email_font_size = 250, 2380, 50
    location_x, location_y, location_font_size = 250, 2520, 50

    color_role = "#3F1561"
    color_skills = "black"
    color_others = "#fff"
    draw_skills_label = False
    font_role_path = FONT_BOLD

elif variant == "Variant 2":
    TEMPLATE_PATH = "./template/Job_Post_TEMP.png"
    template = Image.open(TEMPLATE_PATH)

    role_x, role_y, role_font_size = 210, 1050, 100
    skills_x, skills_y, skills_font_size = 210, 1200, 70
    contact_x, contact_y, contact_font_size = 200, 1680, 36
    email_x, email_y, email_font_size = 200, 1730, 36
    location_x, location_y, location_font_size = 200, 1780, 36

    color_role = "black"
    color_skills = "black"
    color_others = "black"
    draw_skills_label = True
    font_role_path = FONT_BOLD_ITALIC

else:  # Variant 3
    TEMPLATE_PATH = "./template/3.png"
    template = Image.open(TEMPLATE_PATH)

    role_x, role_y, role_font_size = 1200, 1150, 70
    skills_x, skills_y, skills_font_size = 1380, 1470, 60
    contact_x, contact_y, contact_font_size = 220, 1850, 50
    email_x, email_y, email_font_size = 220, 1780, 50
    location_x, location_y, location_font_size = 220, 1920, 50

    color_role = "#ffffff"
    color_skills = "#fff"
    color_others = "#fff"
    draw_skills_label = False
    font_role_path = FONT_BOLD

# === Input Fields ===
role = st.text_input("Job Role", value="Python Developer")
skills = st.text_area("Required Skills (comma-separated)", value="Python, Django, APIs")
contact = st.text_input("Contact Number", value="+91 9016768065")
email = st.text_input("Email Address", value="divyeshsarvaiya2@gmail.com")
location = st.text_input("Job Location", value="Surat")
logo_file = st.file_uploader("Upload Logo Image", type=["png", "jpg", "jpeg", "webp"])

# === SIDEBAR LOGO CONTROLS (shared) ===
st.sidebar.header("🎛️ Logo Controls")
logo_x = st.sidebar.slider("Logo X", 0, 2000, 150)
logo_y = st.sidebar.slider("Logo Y", 0, 2000, 400)
logo_size = st.sidebar.slider("Logo Size", 0.0, 2000.0, 800.0)

# === Validation ===
if not all([role.strip(), skills.strip(), contact.strip(), email.strip(), location.strip(), logo_file]):
    st.error("⚠️ Please fill in all fields and upload the logo to generate and download the image.")
else:
    # === Create Canvas ===
    canvas = template.copy()
    draw = ImageDraw.Draw(canvas)

    # === Load Fonts ===
    font_role = ImageFont.truetype(font_role_path, role_font_size)
    font_skills_bold = ImageFont.truetype(FONT_SEMIBOLD, skills_font_size)
    font_skills_normal = ImageFont.truetype(FONT_REGULAR, skills_font_size)
    font_contact = ImageFont.truetype(FONT_REGULAR, contact_font_size)
    font_email = ImageFont.truetype(FONT_REGULAR, email_font_size)
    font_location = ImageFont.truetype(FONT_REGULAR, location_font_size)

    # === Format Skills Conditionally ===
    if variant == "Variant 3":
        formatted_skills = ",\n".join([s.strip() for s in skills.split(",") if s.strip()])
        selected_skills_font = font_skills_bold
    else:
        formatted_skills = skills
        selected_skills_font = font_skills_normal

    # === Draw Text ===
    # Draw the job role

    draw.text((role_x, role_y), role, font=font_role, fill=color_role)



    if draw_skills_label:
        draw.text((skills_x, skills_y), "Skills:", font=font_skills_bold, fill="#3c83bb")
        label_bbox = draw.textbbox((0, 0), "Skills:", font=font_skills_bold)
        label_width = label_bbox[2] - label_bbox[0]
        draw.text((skills_x + label_width + 10, skills_y), formatted_skills, font=selected_skills_font, fill=color_skills)
    else:
        draw.text((skills_x, skills_y), formatted_skills, font=selected_skills_font, fill=color_skills)

    draw.text((contact_x, contact_y), contact, font=font_contact, fill=color_others)
    draw.text((email_x, email_y), email, font=font_email, fill=color_others)
    draw.text((location_x, location_y), location, font=font_location, fill=color_others)


    # === Add Logo ===
    try:
        logo = Image.open(logo_file).convert("RGBA")
        orig_w, orig_h = logo.size
        scale = min(logo_size / orig_w, logo_size / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        logo = logo.resize((new_w, new_h), Image.LANCZOS)
        canvas.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        st.warning("⚠️ Couldn't load uploaded logo")
        st.text(f"Error: {e}")

    # === Show & Download ===
    st.image(canvas, caption="✅ Generated Job Post", use_column_width=True)

    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    st.download_button(
        label="📥 Download Image",
        data=img_bytes,
        file_name="job_post.png",
        mime="image/png"
    )
