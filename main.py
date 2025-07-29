import PyPDF2
import pyttsx3

def pdf_to_speech(
    pdf_path,
    output_audio="output.mp3",
    start_page=None,
    end_page=None,
    speech_rate=150,  # Default rate (normal: 150-200)
):
    try:
        # Initialize TTS engine
        engine = pyttsx3.init()
        
        # Set speech rate (adjust if too fast/slow)
        engine.setProperty("rate", speech_rate)
        
        # Open PDF
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # Set default page range (all pages)
            if start_page is None:
                start_page = 0
            if end_page is None:
                end_page = total_pages - 1
            
            # Validate page range
            if start_page < 0 or end_page >= total_pages:
                raise ValueError("Invalid page range!")
            
            print(f"Converting pages {start_page + 1} to {end_page + 1}...")
            
            # Extract text from selected pages
            full_text = ""
            for page_num in range(start_page, end_page + 1):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():
                    full_text += text + "\n"
                    print(f"Processed page {page_num + 1}/{total_pages}")
            
            if not full_text.strip():
                print("No text found in the selected pages.")
                return
            
            # Save to audio file instead of real-time speech
            engine.save_to_file(full_text, output_audio)
            engine.runAndWait()
            
            print(f"✅ Audio saved to: {output_audio}")
    
    except FileNotFoundError:
        print("❌ Error: PDF file not found!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        engine.stop()

# Example usage
pdf_to_speech(
    pdf_path="bok.pdf",          
    output_audio="output.mp3",   
    start_page=0,               
    end_page=None,               
    speech_rate=150,             
)