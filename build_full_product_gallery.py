import os
import sys
import shutil
import requests
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\followUPSHEET\healing_touch"
GALLERY_DIR = os.path.join(BASE_DIR, "media_assets", "product gallery")
RAW_DIR = os.path.join(BASE_DIR, "media_assets", "raw_products")
NOTEBOOK_PIC_DIR = os.path.join(BASE_DIR, "media_assets", "notebooklm_hub", "pic")

os.makedirs(GALLERY_DIR, exist_ok=True)
os.makedirs(NOTEBOOK_PIC_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def download_file(url, target_path):
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(target_path, "wb") as f:
                f.write(r.content)
            # Verify with Pillow
            with Image.open(target_path) as im:
                im.verify()
            print(f"[OK] Downloaded: {os.path.basename(target_path)} ({len(r.content)} bytes)")
            return True
        else:
            print(f"[FAIL] HTTP {r.status_code} for {url}")
            return False
    except Exception as e:
        print(f"[ERR] {url}: {e}")
        return False

# ==========================================
# 1. BUPY Silicone Scar Sheets (Already has 5 user photos, ensure completeness)
# ==========================================
bupy_dir = os.path.join(GALLERY_DIR, "bupy-silicone-scar-sheet")
os.makedirs(bupy_dir, exist_ok=True)
# Also add user raw product with roll side by side if exists
bupy_roll_side = os.path.join(RAW_DIR, "WhatsApp Image 2026-10-24 at 12.12.30 AM.jpeg")
if os.path.exists(bupy_roll_side):
    shutil.copy2(bupy_roll_side, os.path.join(bupy_dir, "6_bupy_box_with_roll_real.jpg"))
    print("[OK] Added bupy_box_with_roll_real to bupy gallery")

# ==========================================
# 2. 3M Micropore Tan Tape 1533-0
# ==========================================
print("\n--- Processing 3M Micropore Tan Tape 1533-0 ---")
micropore_dir = os.path.join(GALLERY_DIR, "3m-micropore-tan-tape-1533-0")
os.makedirs(micropore_dir, exist_ok=True)

# Photo 1: User's real photo showing rolls on box REF 1533-0
raw_m1 = os.path.join(RAW_DIR, "WhatsApp Image 2026-10-24 at 12.12.31 AM (1).jpg")
if os.path.exists(raw_m1):
    shutil.copy2(raw_m1, os.path.join(micropore_dir, "1_box_and_tan_rolls_real.jpg"))
    print("[OK] Copied 1_box_and_tan_rolls_real.jpg")

# Photo 2: User's real photo holding roll in hand
raw_m2 = os.path.join(RAW_DIR, "WhatsApp Image 2026-10-24 at 12.12.32 AM.jpeg")
if os.path.exists(raw_m2):
    shutil.copy2(raw_m2, os.path.join(micropore_dir, "2_single_roll_profile_hand_real.jpg"))
    print("[OK] Copied 2_single_roll_profile_hand_real.jpg")

# Photo 3: User's real photo open tray box
raw_desk = os.path.join(RAW_DIR, "WhatsApp Image 2026-10-24 at 12.12.26 AM.jpg")
if os.path.exists(raw_desk):
    with Image.open(raw_desk) as desk_im:
        # Crop the 3M open box in the foreground/center
        w, h = desk_im.size
        crop_box = (int(w*0.28), int(h*0.50), int(w*0.95), int(h*0.98))
        cropped = desk_im.crop(crop_box)
        cropped.save(os.path.join(micropore_dir, "3_box_tray_pack_real.jpg"), quality=95)
        print("[OK] Cropped & saved 3_box_tray_pack_real.jpg")

# Photo 4: Clean medical supplies studio shot
download_file(
    "http://medicalsuppliesfast.com/cdn/shop/files/3M-8815330_7c296d88-243f-4f9d-b226-5cb1d8afd6c3.jpg?v=1750110239",
    os.path.join(micropore_dir, "4_clinical_product_view.jpg")
)

# Photo 5: Clean eBay packaging view
download_file(
    "https://i.ebayimg.com/images/g/Ne4AAOSwWnBnWw7p/s-l500.jpg",
    os.path.join(micropore_dir, "5_specifications_packaging_ref1533.jpg")
)

# ==========================================
# 3. 3M Tegaderm + Pad Waterproof Dressing
# ==========================================
print("\n--- Processing 3M Tegaderm + Pad ---")
tegaderm_dir = os.path.join(GALLERY_DIR, "3m-tegaderm-plus-pad")
os.makedirs(tegaderm_dir, exist_ok=True)

# Photo 1: Retail box packaging (Walmart high-res 302KB)
download_file(
    "https://i5.walmartimages.com/seo/3M-3586-Tegaderm-Pad-Transparent-Film-Dressing-Non-Adherent-Pad-Size-1-3-4-x-2-3-8-For-Wound-Care-Cuts-IV-Sites-Waterproof-Sterile-Non-Allergic-Adhes_03bcb308-9122-40ca-997d-a723c9fd3bb7.4d59a88ffc70414ba93b506070cfd45e.jpeg",
    os.path.join(tegaderm_dir, "1_retail_box_packaging.jpg")
)

# Photo 2: Dressing film and absorbent pad (TigerMedical)
download_file(
    "https://tigermedical.com/cdn/shop/files/MMM3582_cd838d3c-b1c4-4a1b-ab63-d66a5da26e42_868x700.jpg?v=1692012145",
    os.path.join(tegaderm_dir, "2_dressing_film_and_absorbent_pad.jpg")
)

# Photo 3: Official Solventum product overview (121KB)
download_file(
    "https://assets.solventum.com/is/image/mmmspinco/B00035881_transition_ms_Tegaderm-Pad-Kamen_A1C1_R",
    os.path.join(tegaderm_dir, "3_official_solventum_product_overview.jpg")
)

# Photo 4: User's real inventory sterile envelope from desk
if os.path.exists(raw_desk):
    with Image.open(raw_desk) as desk_im:
        w, h = desk_im.size
        crop_box = (0, int(h*0.50), int(w*0.55), int(h*0.78))
        cropped = desk_im.crop(crop_box)
        cropped.save(os.path.join(tegaderm_dir, "4_sterile_pouch_envelope_real.jpg"), quality=95)
        print("[OK] Cropped & saved 4_sterile_pouch_envelope_real.jpg")

# Photo 5: Consumer box packaging view
download_file(
    "https://media.praxisdienst.com/praxident-prod-public-files/media/c9/e8/a6/1740369321/22387-604557_58-opsite-spray-s00ml-smithnephew.jpg?ts=1792098557", # fallback will be replaced below if needed
    os.path.join(tegaderm_dir, "5_temp.jpg")
)
# Let's get an alternate high-res dressing view or copy
if os.path.exists(os.path.join(tegaderm_dir, "5_temp.jpg")):
    os.remove(os.path.join(tegaderm_dir, "5_temp.jpg"))

# Let's get a 5th photo for tegaderm:
download_file(
    "http://medicalsuppliesfast.com/cdn/shop/files/3M-8815330_7c296d88-243f-4f9d-b226-5cb1d8afd6c3.jpg?v=1750110239", # will check alternate
    os.path.join(tegaderm_dir, "5_temp.jpg")
)
if os.path.exists(os.path.join(tegaderm_dir, "5_temp.jpg")):
    os.remove(os.path.join(tegaderm_dir, "5_temp.jpg"))

# Save a clean crop of the desk showing Tegaderm sterile pouch with ruler and specs
if os.path.exists(raw_desk):
    with Image.open(raw_desk) as desk_im:
        w, h = desk_im.size
        crop_box = (0, int(h*0.52), int(w*0.48), int(h*0.75))
        cropped = desk_im.crop(crop_box)
        cropped.save(os.path.join(tegaderm_dir, "5_sterile_pouch_specifications_table.jpg"), quality=95)
        print("[OK] Saved 5_sterile_pouch_specifications_table.jpg")

# ==========================================
# 4. Smith & Nephew Opsite Spray
# ==========================================
print("\n--- Processing Smith & Nephew Opsite Spray ---")
opsite_dir = os.path.join(GALLERY_DIR, "smith-nephew-opsite-spray")
os.makedirs(opsite_dir, exist_ok=True)

# Photo 1: Praxisdienst clean studio aerosol can (95KB)
download_file(
    "https://media.praxisdienst.com/praxident-prod-public-files/media/c9/e8/a6/1740369321/22387-604557_58-opsite-spray-s00ml-smithnephew.jpg?ts=1792098557",
    os.path.join(opsite_dir, "1_opsite_spray_can_studio.jpg")
)

# Photo 2: Lavabis Medical studio can front (73KB)
download_file(
    "http://lavabis.com/cdn/shop/products/IMG_9420.jpg?v=1668361106",
    os.path.join(opsite_dir, "2_opsite_can_and_actuator_lavabis.jpg")
)

# Photo 3: Lavabis Medical studio can angle & label (66KB)
download_file(
    "http://lavabis.com/cdn/shop/products/IMG_9421.jpg?v=1668361106",
    os.path.join(opsite_dir, "3_opsite_can_angle_and_label_lavabis.jpg")
)

# Photo 4: Saudi Medical Store 240ml packaging view (25KB)
download_file(
    "https://saudimedicalstore.com/wp-content/uploads/2025/10/-wbs-yt-240.png",
    os.path.join(opsite_dir, "4_opsite_240ml_saudi_medical.jpg")
)

# Photo 5: User's real inventory can from desk
if os.path.exists(raw_desk):
    with Image.open(raw_desk) as desk_im:
        w, h = desk_im.size
        crop_box = (int(w*0.80), int(h*0.48), w, int(h*0.75))
        cropped = desk_im.crop(crop_box)
        cropped.save(os.path.join(opsite_dir, "5_opsite_spray_inventory_real.jpg"), quality=95)
        print("[OK] Cropped & saved 5_opsite_spray_inventory_real.jpg")

# ==========================================
# 5. Silicone Nostril Retainer
# ==========================================
print("\n--- Processing Silicone Nostril Retainer ---")
nostril_dir = os.path.join(GALLERY_DIR, "silicone-nostril-retainer")
os.makedirs(nostril_dir, exist_ok=True)

# Photo 1: eBay high-resolution studio photo of retainer pair (91KB)
download_file(
    "https://i.ebayimg.com/images/g/UFwAAOSw1ttnwVkL/s-l1200.jpg",
    os.path.join(nostril_dir, "1_silicone_nostril_retainer_pair_highres.jpg")
)

# Photo 2: Rhinoplasty Instruments clinical view 1 (13KB)
download_file(
    "https://rhinoplastyinstruments.com/wp-content/uploads/2025/04/nasal-retainer-1.jpg",
    os.path.join(nostril_dir, "2_nasal_retainer_clinical_view1.jpg")
)

# Photo 3: Rhinoplasty Instruments clinical view 2 (13KB)
download_file(
    "https://rhinoplastyinstruments.com/wp-content/uploads/2025/04/nasal-retainer-2.jpg",
    os.path.join(nostril_dir, "3_nasal_retainer_clinical_view2.jpg")
)

# Photo 4: Rhinoplasty Instruments clinical view 3 (13KB)
download_file(
    "https://rhinoplastyinstruments.com/wp-content/uploads/2025/04/nasal-retainer-3.jpg",
    os.path.join(nostril_dir, "4_nasal_retainer_clinical_view3.jpg")
)

# Photo 5: User's real inventory box from desk
if os.path.exists(raw_desk):
    with Image.open(raw_desk) as desk_im:
        w, h = desk_im.size
        crop_box = (int(w*0.78), int(h*0.71), w, int(h*0.86))
        cropped = desk_im.crop(crop_box)
        cropped.save(os.path.join(nostril_dir, "5_nostril_retainer_box_inventory_real.jpg"), quality=95)
        print("[OK] Cropped & saved 5_nostril_retainer_box_inventory_real.jpg")

# ==========================================
# Synchronize to notebooklm_hub/pic
# ==========================================
print("\n--- Synchronizing to notebooklm_hub/pic ---")
for root, dirs, files in os.walk(GALLERY_DIR):
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            prod_folder = os.path.basename(root)
            src_fp = os.path.join(root, f)
            dest_fp = os.path.join(NOTEBOOK_PIC_DIR, f"{prod_folder}_{f}")
            shutil.copy2(src_fp, dest_fp)

print("Synchronized all gallery images to notebooklm_hub/pic successfully!")
