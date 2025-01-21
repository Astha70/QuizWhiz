import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# API key for Generative AI
GOOGLE_API_KEY = os.getenv('GEM_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def generate_quiz_questions(document_text, num_questions, question_type, difficulty):
    prompt_prefix = f"Generate {num_questions} "
    if question_type == "MCQ":
        prompt_prefix += "multiple-choice "
    elif question_type == "Long Questions":
        prompt_prefix += "short-answer "

     # Improved difficulty handling in the prompt
    if difficulty.lower() == "hard":
        prompt_prefix += "challenging and complex "
    elif difficulty.lower() == "medium":
        prompt_prefix += "moderately difficult "
    else:
        prompt_prefix += "relatively easy "

    prompt_prefix += f"quiz questions with answers based on the following document.\n"

    if question_type == "MCQ":
        prompt_template = """
        Format each question like this:

        **Question N:** [The question text]
        (a) [Option A]
        (b) [Option B]
        (c) [Option C]
        (d) [Option D]
        **Answer:** [Correct Answer Text]
        """
    elif question_type == "Long Questions":
        prompt_template = """
        Format each question like this:

        **Question N:** [The question text]
        **Answer:** [The answer]
        """

    prompt = prompt_prefix + prompt_template + f"\nDocument:\n{document_text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating quiz questions: {e}")
        return None

def parse_quiz_questions(quiz_text, question_type):
    questions = []
    split_pattern = r'(?=\*\*Question \d+:\*\*)'
    question_blocks = re.split(split_pattern, quiz_text)
    question_blocks = [block.strip() for block in question_blocks if block.strip()]

    for block in question_blocks:
        question_data = {}
        # Extract question number and text
        question_match = re.match(r"\*\*Question \d+:\*\*\s*\n*(.+?)(?=\n\([abcd]\)|\n\*\*Answer:\*\*|$)", block, re.DOTALL)
        if question_match:
            question_data["question"] = question_match.group(1).strip()
        else:
            continue  # Skip if no question text found

        if question_type == "MCQ":
            options = {}
            for option_match in re.finditer(r"\(([abcd])\) (.*?)(?=\n|$)", block):
                options[option_match.group(1)] = option_match.group(2).strip()
            question_data["options"] = options
            answer_match = re.search(r"\*\*Answer:\*\* \(([abcd])\)(.*)", block)
            if answer_match:
                question_data["answer"] = f"({answer_match.group(1)}){answer_match.group(2).strip()}"
        elif question_type == "Long Questions":
            answer_match = re.search(r"\*\*Answer:\*\*\s*\n*(.+)", block, re.DOTALL)
            if answer_match:
                question_data["answer"] = answer_match.group(1).strip()

        if question_data.get("question"):
            questions.append(question_data)

    return questions

def clear_selections():
    st.session_state.uploaded_file = None
    st.session_state.question_type = "MCQ"
    st.session_state.difficulty = "Easy" 
    st.session_state.num_questions = 5 
    if 'generated_questions' in st.session_state:
        del st.session_state.generated_questions

def main():
    st.title("QuizWhiz")

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Generator Options")
        uploaded_file = st.file_uploader("Import or drag and drop your PDF", type="pdf")
        question_type = st.radio("Type of Questions", ["MCQ", "Long Questions"])
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of Questions", 1, 10, 5)

        lft, rgt = st.columns(2, vertical_alignment="bottom")

        if lft.button("Generate", use_container_width=True):
            if uploaded_file is not None:
                document_text = extract_text_from_pdf(uploaded_file)
                if document_text:
                    with st.spinner("Generating questions..."):
                        quiz_text = generate_quiz_questions(document_text, num_questions, question_type, difficulty)
                    if quiz_text:
                        st.session_state.generated_questions = parse_quiz_questions(quiz_text, question_type)
                    else:
                        st.error("Failed to generate quiz questions.")
            else:
                st.warning("Please upload a PDF document.")
        if rgt.button("Clear Ques", on_click=clear_selections):
                pass

    with right_column:
        st.subheader("Generated Questions")
        show_answers = st.toggle("Show Answers", value=False)

        if "generated_questions" in st.session_state and st.session_state.generated_questions:
            for i, question_data in enumerate(st.session_state.generated_questions):
                with st.container(border=True):
                    st.markdown(f"**Question {i+1}:** {question_data['question']}")

                    if question_type == "MCQ":
                        for option_key, option_value in question_data["options"].items():
                            st.markdown(f"({option_key}) {option_value}")
                        if show_answers:
                            st.markdown(f"**Answer:** {question_data['answer']}")
                    elif question_type == "Long Questions":
                        if show_answers:
                            st.markdown(f"**Answer:** {question_data['answer']}")
                        else:
                            st.caption("Answer:")
                            st.markdown("*" * 10)  # Placeholder for hidden answer

        st.markdown("") # Add some spacing
        col1, col2, _ = st.columns([1,1,4]) # Adjust widths as needed
        with col2:
            if st.session_state.get('generated_questions'): # Only show if questions are generated
                data_to_download = []
                for i, q_data in enumerate(st.session_state.generated_questions):
                    data_to_download.append(f"**Question {i+1}:** {q_data['question']}\n")
                    if question_type == "MCQ":
                        for option_key, option_value in q_data["options"].items():
                            data_to_download.append(f"({option_key}) {option_value}\n")
                        data_to_download.append(f"**Answer:** {q_data['answer']}\n\n")
                    elif question_type == "Long Questions":
                        data_to_download.append(f"**Answer:** {q_data['answer']}\n\n")

                download_string = "\n".join(data_to_download)
                st.download_button(
                    label="Download",
                    data=download_string.encode('utf-8'),
                    file_name="quiz_questions.txt",
                    mime="text/plain",
                )

    # Inject CSS for scrollable columns
    st.markdown(
        """
        <style>
        div.streamlit-container .element-container:nth-child(2) > div:nth-child(1) > div:nth-child(1) {
            overflow-y: auto;
            max-height: 80vh; 
            padding-right: 10px;
        }
        div.streamlit-container .element-container:nth-child(3) > div:nth-child(1) > div:nth-child(1) {
            overflow-y: auto;
            max-height: 80vh;
            padding-left: 10px;
        }

        div.stDownloadButton > button {
            white-space: nowrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()