# 📚 **QuizWhiz**: AI-Powered Quiz Generator from PDF

## **Introduction**
Welcome to **QuizWhiz**! 🚀 This app allows you to generate quiz questions from any PDF document. Whether you're a teacher, student, or content creator, this tool helps create quizzes in **MCQ** or **Long Questions** format. 

It leverages **Google's Generative AI (Gemini)** to generate questions based on the content of your uploaded PDF document.

### **Key Features**:
- **PDF to Text Extraction**: Upload any PDF, and the app will extract the text for question generation.
- **Quiz Question Generation**: Generate **MCQ** or **Long Questions** based on the extracted text.
- **Customizable Difficulty**: Choose the difficulty level: Easy, Medium, or Hard.
- **Downloadable Quiz**: After generating the questions, you can download them in a text format.

## **Key Technologies**
- **Streamlit**: Used for building the interactive web app interface.
- **Google Generative AI (Gemini)**: Used for generating quiz questions from text.
- **PyPDF2**: For extracting text from uploaded PDF files.
- **dotenv**: For securely loading environment variables like API keys.

## **Getting Started 🚀**
Ready to generate quiz questions from a PDF? Follow the steps below.

### **Clone the Repository:**

```bash
git clone https://github.com/Astha70/QuizWhiz
```
### **Create and Activate Virtual Environment (Optional):**

If you prefer to isolate project dependencies, create a virtual environment using tools like venv or conda. Activate the environment before proceeding.

```Bash

python -m venv venv
source venv/bin/activate  # Unix/macOS
source venv\Scripts\activate  # Windows
```
### **Install Dependencies:**

Install the required libraries using pip:

```Bash
pip install -r requirements.txt
```

### **Set Up APIs:**
The app uses the Google Gemini API for generating quiz questions and set them up in the environment variables or configuration files.

### **Run the App Locally:**

Start the Streamlit app to experience WanderWise:

```Bash
streamlit run app.py
```

## **Deployment 🌐**
For wider accessibility, consider deploying your app on a platform like Streamlit Cloud. Follow the platform's specific instructions for deployment.

## **Contributing 🤝**
We welcome contributions from the community! Feel free to fork the repository, make your changes, and submit a pull request.
