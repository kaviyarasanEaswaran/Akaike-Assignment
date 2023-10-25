pip install PyPDF2

import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Provide the path to your PDF file
pdf_file_path = "/content/drive/MyDrive/Colab Notebooks/chapter-2.pdf"

# Call the function to extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_file_path)

# Print the extracted text
print(extracted_text)

import re  

def remove_dates_times(text):
    # Define regex patterns for date and time formats
    date_pattern = r"\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b"  # Matches dates in formats like dd/mm/yyyy or dd-mm-yyyy
    time_pattern = r"\b\d{1,2}:\d{2}(:\d{2})?\s*(AM|PM)?\b"  # Matches times in formats like hh:mm:ss AM/PM or hh:mm AM/PM

    # Remove date and time patterns from the text
    text_without_dates = re.sub(date_pattern, "", text)
    text_without_dates_times = re.sub(time_pattern, "", text_without_dates)

    return text_without_dates_times

cleaned_text = remove_dates_times(extracted_text)

def clean_text(text):
    # Remove unwanted characters and extra whitespaces
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'\n', ' ', cleaned_text)
    cleaned_text = re.sub(r'\r', ' ', cleaned_text)
    cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

text=clean_text(cleaned_text)

text

import random
from string import ascii_lowercase

def generate_multiple_choice_question(question, options, correct_options):
    choices = [f"{option}. {text}" for option, text in zip(ascii_lowercase, options)]
    correct_choices = [option for option, is_correct in zip(ascii_lowercase, correct_options) if is_correct]
    correct_choices_formatted = " & ".join(correct_choices)
    question_with_choices = question + "\n" + "\n".join(choices) + "\nCorrect Options: (" + correct_choices_formatted + ")"

    return question_with_choices

def get_mca_questions(context):
    entities = context.split(",")
    entity_counts = {}
    
    for entity in entities:
        entity = entity.strip()
        if entity:
            entity_counts[entity] = entity_counts.get(entity, 0) + 1
    
    mca_questions = []
    question_count = 1
    
    for entity in entity_counts:
        # Filter out entities that occur less than a certain threshold
        if entity_counts[entity] < 2:
            continue
        
        question = f"Q{question_count}: Which of the following are related to {entity}? Choose two options."
        options = [entity]
        
        # Add two random distractors
        distractors = list(entity_counts.keys())
        distractors.remove(entity)
        random.shuffle(distractors)
        options.extend(distractors[:2])
        
        # Randomly assign correct options
        correct_options = [True, True, False, False]
        random.shuffle(correct_options)
        
        question_formatted = generate_multiple_choice_question(question, options, correct_options)
        mca_questions.append(question_formatted)
        
        question_count += 1
    
    return mca_questions

text1=get_mca_questions(text)

text1