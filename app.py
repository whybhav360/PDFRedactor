import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from pytesseract import Output
from PIL import Image 
import io
import platform

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Mac
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

# -------------------- OCR WITH BOUNDING BOXES --------------------
def ocr_with_boxes(image, keywords, page_width, page_height):
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

# -------------------- PROCESS PAGE (render + OCR) --------------------
def process_page_for_ocr_redaction(page, keywords):
    pix = page.get_pixmap(dpi=300)  # high-res render
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return ocr_with_boxes(img, keywords, page.rect.width, page.rect.height)

# -------------------- REDACTION LOGIC --------------------
def redact_pdf(input_pdf, keywords):
    doc = fitz.open(stream=input_pdf.read(), filetype="pdf")
    keywords = [kw.lower().strip() for kw in keywords if kw.strip()]

    total_pages = len(doc)
    progress_bar = st.progress(0.0)

    for page_num, page in enumerate(doc, start=1):
        # native text redaction
        native_text = page.get_text("text").lower()
        for keyword in keywords:
            if keyword in native_text:
                areas = page.search_for(keyword)
                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))

        # OCR-based redaction
        ocr_areas = process_page_for_ocr_redaction(page, keywords)
        for area in ocr_areas:
            page.add_redact_annot(area, fill=(0, 0, 0))

        page.apply_redactions()
        progress_bar.progress(page_num / total_pages)

    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)
    return output_buffer

# -------------------- Session-state helpers for keywords --------------------
def add_keyword_from_input():
    """Callback for text_input on_change: add typed keyword, then clear input."""
    val = st.session_state.new_kw_input.strip()
    if not val:
        return
    # Avoid duplicates (case-insensitive)
    existing_lower = [k.lower() for k in st.session_state.keywords]
    if val.lower() not in existing_lower:
        st.session_state.keywords.append(val)
    # clear the input box
    st.session_state.new_kw_input = ""

def remove_keyword(idx):
    """Callback to remove keyword by index."""
    if 0 <= idx < len(st.session_state.keywords):
        st.session_state.keywords.pop(idx)

# -------------------- Streamlit UI --------------------
def main():
    st.title("🔒 PDF Redaction Tool")
    

    # init session state
    if "keywords" not in st.session_state:
        st.session_state.keywords = []
    if "new_kw_input" not in st.session_state:
        st.session_state.new_kw_input = ""

    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

    st.subheader("Enter Keywords to Redact")
    # This text_input uses on_change callback to add the keyword and clear the field
    st.text_input(
        "Type a word and press Enter",
        key="new_kw_input",
        on_change=add_keyword_from_input,
        placeholder="e.g., confidential, password, secret",
    )

    # Display keywords as clickable chips (buttons). Arrange into 6 columns per row.
    st.write("### Words to be Redacted:")
    if st.session_state.keywords:
        cols = st.columns(6)
        for idx, keyword in enumerate(st.session_state.keywords):
            col = cols[idx % 6]
            # Each button has a unique key and calls remove_keyword(idx)
            col.button(f"❌ {keyword}", key=f"remove_{idx}", on_click=remove_keyword, args=(idx,))
    else:
        st.info("No keywords added yet. Type above and press Enter to add.")

    st.write("---")

    # Redact button
    if uploaded_pdf and st.session_state.keywords:
        if st.button("🚀 Start Redaction"):
            st.info("Processing your PDF. This may take a while depending on size...")
            output_buffer = redact_pdf(uploaded_pdf, st.session_state.keywords)

            st.success("✅ Redaction complete!")
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
