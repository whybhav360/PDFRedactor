import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from pytesseract import Output
from PIL import Image
import io
import platform
import re

# # -------------------- Tesseract setup --------------------
# if platform.system() == "Windows":
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# else:
#     pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"


# -------------------- OCR WITH BOUNDING BOXES --------------------
def ocr_with_boxes(image, keywords, page_width, page_height):
    """Run OCR and return bounding boxes of matching keywords."""
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    redaction_areas = []

    img_width, img_height = image.size
    keywords = [kw.lower().strip() for kw in keywords if kw.strip()]

    for i, text in enumerate(data["text"]):
        if not text or text.strip() == "":
            continue
        word = text.lower().strip()

        for keyword in keywords:
            if keyword in word:
                x, y, w, h = (
                    data["left"][i],
                    data["top"][i],
                    data["width"][i],
                    data["height"][i],
                )

                scale_x = page_width / img_width
                scale_y = page_height / img_height

                rect = fitz.Rect(
                    x * scale_x,
                    y * scale_y,
                    (x + w) * scale_x,
                    (y + h) * scale_y,
                )
                redaction_areas.append(rect)

    return redaction_areas


# -------------------- PROCESS PAGE --------------------
def process_page_for_ocr_redaction(page, keywords):
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return ocr_with_boxes(img, keywords, page.rect.width, page.rect.height)


# -------------------- REDACTION LOGIC --------------------
def redact_pdf(input_pdf, keywords):
    """Perform real (non-selectable) redaction on all text and OCR layers."""
    doc = fitz.open(stream=input_pdf.read(), filetype="pdf")
    keywords = [kw.lower().strip() for kw in keywords if kw.strip()]
    total_pages = len(doc)
    progress_bar = st.progress(0.0)

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")

        # Redact all matches in the native text layer (case-insensitive)
        for keyword in keywords:
            matches = re.finditer(re.escape(keyword), page_text, flags=re.IGNORECASE)
            for match in matches:
                rects = page.search_for(match.group(), quads=False)
                for rect in rects:
                    page.add_redact_annot(rect, fill=(0, 0, 0), text="")  # no text overlay

        # OCR-based detection for image-only pages
        ocr_areas = process_page_for_ocr_redaction(page, keywords)
        for area in ocr_areas:
            page.add_redact_annot(area, fill=(0, 0, 0), text="")

        # ✅ Apply redactions (actually removes text content)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

        progress_bar.progress(page_num / total_pages)

    # Save redacted output
    output_buffer = io.BytesIO()
    doc.save(output_buffer, deflate=True, garbage=4)
    doc.close()
    output_buffer.seek(0)
    return output_buffer


# -------------------- SESSION HELPERS --------------------
def add_keyword_from_input():
    val = st.session_state.new_kw_input.strip()
    if not val:
        return
    existing_lower = [k.lower() for k in st.session_state.keywords]
    if val.lower() not in existing_lower:
        st.session_state.keywords.append(val)
    st.session_state.new_kw_input = ""


def remove_keyword(idx):
    if 0 <= idx < len(st.session_state.keywords):
        st.session_state.keywords.pop(idx)


# -------------------- MAIN APP --------------------
def main():
    st.title("🔒 Secure PDF Redaction Tool")

    if "keywords" not in st.session_state:
        st.session_state.keywords = []
    if "new_kw_input" not in st.session_state:
        st.session_state.new_kw_input = ""

    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

    st.subheader("Enter Keywords to Redact")
    st.text_input(
        "Type a word and press Enter",
        key="new_kw_input",
        on_change=add_keyword_from_input,
        placeholder="e.g., confidential, password, secret",
    )

    st.write("### Words to be Redacted:")
    if st.session_state.keywords:
        cols = st.columns(6)
        for idx, keyword in enumerate(st.session_state.keywords):
            col = cols[idx % 6]
            col.button(f"❌ {keyword}", key=f"remove_{idx}", on_click=remove_keyword, args=(idx,))
    else:
        st.info("No keywords added yet. Type above and press Enter to add.")

    st.write("---")

    if uploaded_pdf and st.session_state.keywords:
        if st.button("🚀 Start Redaction"):
            st.info("Processing your PDF... please wait.")
            output_buffer = redact_pdf(uploaded_pdf, st.session_state.keywords)
            st.success("✅ Redaction complete! The text has been *permanently removed*.")

            st.download_button(
                "📥 Download Redacted PDF",
                data=output_buffer,
                file_name="redacted_output.pdf",
                mime="application/pdf",
            )
    elif uploaded_pdf and not st.session_state.keywords:
        st.warning("Please add at least one keyword to redact.")


if __name__ == "__main__":
    main()
