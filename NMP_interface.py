# ///////////////////////////////////////////////////////////////////////////
# AUTOMATIC INVOICE CHECKER /////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////


# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# Importing required libraries
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

# Streamlit-based user interface
# in terminal: streamlit run "C:\Users\landini\Desktop\Code\NMP\toshare\NMP_interface.py"
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import subprocess
import sys
import pandas as pd 
import numpy as np
import PyPDF2
import os
import streamlit as st
from io import BytesIO
import base64
import time
import streamlit.components.v1 as components
from PIL import Image
from pdf2image import convert_from_bytes
import easyocr
import nltk
# nltk.download("stopwords")                                ### we do it manually as the download functions clashes with the ECB firewall
# nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer 
# from nltk import pos_tag, word_tokenize
script_dir = os.path.dirname(os.path.abspath(__file__))         ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# try with st.altair_chart  !!!!!!!!!!!!!!!!!! or bokeh, plotly, pydeck

# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
# Initialization
# ------------------------------------------------------------------------------------------------------------------------------------------------------ #

if "home" not in st.session_state:
    st.session_state["home"] = False
if "NMPinvoicechecker" not in st.session_state:
    st.session_state["NMPinvoicechecker"] = False
if "info" not in st.session_state:
    st.session_state["info"] = False
if "chapter1" not in st.session_state:
    st.session_state["chapter1"] = False
if "chapter2" not in st.session_state:
    st.session_state["chapter2"] = False
if "chapter3" not in st.session_state:
    st.session_state["chapter3"] = False
if "chapter4" not in st.session_state:
    st.session_state["chapter4"] = False
if "control_excel_df" not in st.session_state:
    st.session_state["control_excel_df"] = False
if "text_df" not in st.session_state:
    st.session_state["text_df"] = False
if "invoice_ver" not in st.session_state:
    st.session_state["invoice_ver"] = False

# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# Page configuration    
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

# Page configuration                                    
icon_path = os.path.join(script_dir, "Images", "icon-ECB.png")     ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
st.set_page_config(
    page_title="CRE - NMP Invoice Checker",
    page_icon=icon_path,  
    layout="wide",
    initial_sidebar_state = "auto"
)

logo_path = os.path.join(script_dir, "Images", "European-Central-Bank.png") 
def logoandtitle():
# Import and convert the image to bytes
    def pil_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    image1 = Image.open(logo_path)

    # define position and dimension
    image1_64 = pil_to_base64(image1)

    # create a custom container 
    st.markdown(
        """
        <style>
        .container {
            display: flex;
            align-items: center; 
            padding: 10px;
        }
        .title { 
            font-size: 45px;
            font-weight: bold;
            font-family: "Roboto", sans-serif;
            margin-right: 20px
        }
        .logo {
            width: 400x;
            height: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Opening page settings
    # ECB logo 
    st.markdown(
        f"""
        <style>
        .container {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo {{
            width: 25%;  
            height: auto;
        }}
        </style>
        <div class="container">
            <img src="data:image/png;base64,{image1_64}" class="logo">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    # Title                                             ###### !!!! Specify for font "!important"
    st.markdown(
        f"""
        <style>
        .container1 {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -80px;
        }}
        .title1 {{
            font-size: 3.5em !important;
            font-weight: bold;
        }}
        </style>
        <div class="container1">
            <p class="title1">
            NMP INVOICE CHECKER
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("")

    # Subtitle                                   ###### !!!! Specify for font "!important"
    st.markdown(
        f"""
        <style>
        .container2 {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -60px;
        }}
        .title2 {{
            font-size: 2em !important;                   
            font-weight: bold;
        }}
        </style>
        <div class="container2">
            <p class="title2">
            Corporate Real Estate
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.sidebar.title("NAVIGATION")

if st.sidebar.button(label="Home", icon=":material/home_app_logo:", key = 101, type="tertiary", use_container_width=False):
    st.session_state["home"] = True
    st.session_state["NMPinvoicechecker"] = None
    st.session_state["info"] = None

if st.sidebar.button(label="NMP Invoice Checker", icon=":material/network_intel_node:", key = 102, type="tertiary", use_container_width=False):
    st.session_state["NMPinvoicechecker"] = True
    st.session_state["home"] = None 
    st.session_state["info"] = None

if st.sidebar.button(label="Info", icon=":material/search_insights:", key = 103, type="tertiary", use_container_width=False):
    st.session_state["info"] = True
    st.session_state["home"] = None
    st.session_state["NMPinvoicechecker"] = None

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# Home
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

mb_path = os.path.join(script_dir, "Images", "MB-3D.png")

if st.session_state["home"] == False and st.session_state["NMPinvoicechecker"] == False and st.session_state["info"] == False:
    st.session_state["home"] = True

if st.session_state.get("home"):
    logoandtitle()

    colhome1, colhome2 = st.columns([5, 5])
    
    with colhome1:
        st.write("")
        st.write("")
        st.write("")	
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(
        f"""
        <style>
        .container20 {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-end;
            text-align: right;
        }}
        .text20 {{
            font-size: 1em !important;
            font-weight: normal;
        }}
        </style>
        <div class="container20">
            <p class="text20">
            The CRE - NMP Invoice Checker is an advanced tool designed to streamline the process of managing and verifying invoices. By leveraging cutting-edge technologies such as text extraction, tokenization, and automated matching, this tool enables users to efficiently upload control files and invoices, extract relevant data, and validate the information against predefined criteria. With its user-friendly interface and robust functionality, the tool aims to enhance accuracy, reduce manual effort, and ensure compliance with corporate standards, making it an essential asset for Corporate Real Estate operations.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
        )

    with colhome2:
        st.write("")
        def pil_to_base64(image):
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()

        image2 = Image.open(mb_path)
        image2_64 = pil_to_base64(image2)

        st.markdown(
        f"""
        <style>
        .container10 {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo10 {{
            width: 50%;  
            height: auto;
        }}
        </style>
        <div class="container10">
            <img src="data:image/png;base64,{image2_64}" class="logo10">
        </div>
        """,
        unsafe_allow_html=True
        )
        
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# NMP Invoice Checker 
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
# Structure
# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
    
control_excel_df = pd.DataFrame()
text_df = pd.DataFrame() 
    
if st.session_state.get("NMPinvoicechecker"):
    logoandtitle()
    st.write("")
    st.write("")

    c1, c2, c3, c4 = st.columns([7, 7, 7, 7])
    with c1:
        if st.button(label="CONTROL FILE", icon=":material/dataset:", key = 1, type="primary", use_container_width=True):
                st.session_state["chapter1"] = True
                st.session_state["control_excel_df"] = control_excel_df
                st.session_state["chapter2"] = False
                st.session_state["chapter3"] = False
                st.session_state["chapter4"] = False
    with c2:
        if st.button(label="INVOICES", icon=":material/document_scanner:", key = 2, type="primary", use_container_width=True):
                st.session_state["chapter1"] = False
                st.session_state["chapter2"] = True
                st.session_state["text_df"] = text_df
                st.session_state["chapter3"] = False
                st.session_state["chapter4"] = False
    with c3:
        if st.button(label="VERIFICATION", icon=":material/join_left:", key = 3, type="primary", use_container_width=True):
                st.session_state["chapter1"] = False
                st.session_state["chapter2"] = False
                st.session_state["chapter3"] = True
                st.session_state["chapter4"] = False
    with c4:
        if st.button(label="VALIDATION", icon=":material/verified_user:", key = 4, type="primary", use_container_width=True):
                st.session_state["chapter1"] = False
                st.session_state["chapter2"] = False
                st.session_state["chapter3"] = False
                st.session_state["chapter4"] = True

# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
# CHAPTER 1: Upload your control excel file
# ------------------------------------------------------------------------------------------------------------------------------------------------------ #

# Control Excel file uploader
    if st.session_state.get("chapter1"):

        st.write("")
        st.write("")
        st.title("1) UPLOAD YOUR CONTROL FILE")
        control_excel = st.file_uploader(label = "", type=["xlsx", "csv"])
        if control_excel:
            if control_excel.name.endswith(".xlsx"):
                control_excel_rawdf = pd.read_excel(control_excel)
            else:
                control_excel_rawdf = pd.read_csv(control_excel)        #####!!!!!!!!!!!!!! Make the 

            selected_columns = st.multiselect("Select the columns to display", control_excel_rawdf.columns)
            control_excel_df = control_excel_rawdf[selected_columns]  

            if not control_excel_df.empty:                  
                st.dataframe(control_excel_df)
                st.session_state["control_excel_df"] = control_excel_df

# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# CHAPTER 2: UPLOAD YOUR INVOICES
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

# Invoice uploader
    if st.session_state.get("chapter2"):

        st.write("")
        st.write("")
        st.title("2) UPLOAD YOUR INVOICES")
        invoices_list = st.file_uploader("", type=["pdf"], accept_multiple_files=True)
        invoices_text_dataset = [] 

# Text extraction & tokenization model
        def extract_text():

# Function to extract text from a PDF file
            def extract_text_from_pdf(file):
                text = ""
                reader = PyPDF2.PdfReader(file)
                for page_number in range(len(reader.pages)):
                    page = reader.pages[page_number]
                    text += page.extract_text()
                return text

# DEF (easyocr)
# This is a for loop that iterates over each item in the result list:
# result is the output from the easyocr.Reader.readtext method, which returns a list of tuples.
# Each tuple in the list contains three elements:
# - bbox: The bounding box coordinates of the detected text in the image.
# - extracted_text: The actual text that was extracted from the image.
# - prob: The confidence score (probability) of the extracted text being correct.

            def extract_text_from_image_pdf(file, languages=["fr"]):
                images = convert_from_bytes(file.read())
                reader = easyocr.Reader(languages, model_storage_directory="C:\\Users\\landini\\.EasyOCR\\model", gpu=False)
                text = ""
                for image in images:
                    result = reader.readtext(image)
                    for (bbox, extracted_text, prob) in result:
                        text += extracted_text + '\n'
                return text

            for invoice in invoices_list:
                try:
                    content = extract_text_from_pdf(invoice)
                    if not content.strip():                                                           ###!!!!!!!!!
                        content = extract_text_from_image_pdf(invoice, languages=["fr"])
                except Exception as e:
                    content = f"Error extracting text: {e}"
                invoices_text_dataset.append([invoice.name, content, ""])

            text_df = pd.DataFrame(invoices_text_dataset, columns=["FileName", "Content", "Tokenized Text"])

# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# Tokenization and text adjustments 
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

# Remove hypthens 
#    text_df["Tokenized Text"] = text_df["!!!!Content"].str.replace("-", " ", regex = True)

# Remove punctuation and special characters 
#    text_df["Tokenized Text"] = text_df["Tokenized Text"].str.replace(r"[^\w\s]", " ", regex = True)                                                            ###!!!!!!!!!!!! Look at regex                                                                            ####!!!!!!!!!! (combine function with |)

# Define the function
            def tokenize_text(dataset, output_column, input_column): 
# Convert text to lowercase 
                dataset[output_column] = dataset[input_column].str.lower()
# Remove stopwords
                stop_words = [
# English 
                "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "he'd", "he'll", "her", "here", "hers", "herself", "he's", "him", "himself", "his", "how", "i", "i'd", "if", "i'll", "i'm", "in", "into", "is", "isn", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "i've", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn", "shouldn't", "should've", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "we'd", "we'll", "we're", "were", "weren", "weren't", "we've", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "your", "you're", "yours", "yourself", "yourselves", "you've",
# German 
                "aber", "alle", "allem", "allen", "aller", "alles", "als", "also", "am", "an", "ander", "andere", "anderem", "anderen", "anderer", "anderes", "anderm", "andern", "anderr", "anders", "auch", "auf", "aus", "bei", "bin", "bis", "bist", "da", "damit", "dann", "der", "den", "des", "dem", "die", "das", "dass", "daß", "derselbe", "derselben", "denselben", "desselben", "demselben", "dieselbe", "dieselben", "dasselbe", "dazu", "dein", "deine", "deinem", "deinen", "deiner", "deines", "denn", "derer", "dessen", "dich", "dir", "du", "dies", "diese", "diesem", "diesen", "dieser", "dieses", "doch", "dort", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "einig", "einige", "einigem", "einigen", "einiger", "einiges", "einmal", "er", "ihn", "ihm", "es", "etwas", "euer", "eure", "eurem", "euren", "eurer", "eures", "für", "gegen", "gewesen", "hab", "habe", "haben", "hat", "hatte", "hatten", "hier", "hin", "hinter", "ich", "mich", "mir", "ihr", "ihre", "ihrem", "ihren", "ihrer", "ihres", "euch", "im", "in", "indem", "ins", "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "kann", "kein", "keine", "keinem", "keinen", "keiner", "keines", "können", "könnte", "machen", "man", "manche", "manchem", "manchen", "mancher", "manches", "mein", "meine", "meinem", "meinen", "meiner", "meines", "mit", "muss", "musste", "nach", "nicht", "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "sehr", "sein", "seine", "seinem", "seinen", "seiner", "seines", "selbst", "sich", "sie", "ihnen", "sind", "so", "solche", "solchem", "solchen", "solcher", "solches", "soll", "sollte", "sondern", "sonst", "über", "um", "und", "uns", "unsere", "unserem", "unseren", "unser", "unseres", "unter", "viel", "vom", "von", "vor", "während", "war", "waren", "warst", "was", "weg", "weil", "weiter", "welche", "welchem", "welchen", "welcher", "welches", "wenn", "werde", "werden", "wie", "wieder", "will", "wir", "wird", "wirst", "wo", "wollen", "wollte", "würde", "würden", "zu", "zum", "zur", "zwar", "zwischen",
# French
                "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en", "et", "eux", "il", "ils", "je", "la", "le", "les", "leur", "lui", "ma", "mais", "me", "même", "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on", "ou", "par", "pas", "pour", "qu", "que", "qui", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "toi", "ton", "tu", "un", "une", "vos", "votre", "vous", "c", "d", "j", "l", "à", "m", "n", "s", "t", "y", "été", "étée", "étées", "étés", "étant", "étante", "étants", "étantes", "suis", "es", "est", "sommes", "êtes", "sont", "serai", "seras", "sera", "serons", "serez", "seront", "serais", "serait", "serions", "seriez", "seraient", "étais", "était", "étions", "étiez", "étaient", "fus", "fut", "fûmes", "fûtes", "furent", "sois", "soit", "soyons", "soyez", "soient", "fusse", "fusses", "fût", "fussions", "fussiez", "fussent", "ayant", "ayante", "ayantes", "ayants", "eu", "eue", "eues", "eus", "ai", "as", "avons", "avez", "ont", "aurai", "auras", "aura", "aurons", "aurez", "auront", "aurais", "aurait", "aurions", "auriez", "auraient", "avais", "avait", "avions", "aviez", "avaient", "eut", "eûmes", "eûtes", "eurent", "aie", "aies", "ait", "ayons", "ayez", "aient", "eusse", "eusses", "eût", "eussions", "eussiez", "eussent"
                ] 
                dataset[output_column] = dataset[output_column].apply(lambda x: " ".join(word for word in x.split() if word not in stop_words))
# Tokenization (without nltk)
                dataset[output_column] = dataset[output_column].str.split()

                return dataset[output_column]
            
            text_df["Tokenized Text"] = tokenize_text(text_df, "Tokenized Text", "Content")

# Store the dataset in session state
            st.session_state["text_df"] = text_df
            st.dataframe(text_df) 

# Progress bar  
#    def status_update():  
#        ri_time = 0 
#        cts_time = 0
#        tt_time = 0
#        for invoice in invoices_list:
#            ri_time += 1 
#            cts_time += 2
#            tt_time += 2    
#        with st.status("Extracting text", expanded=True) as status:
#            st.write("Retrieving invoices...")
#            time.sleep(ri_time)
#            st.write("Converting to strings...")
#            time.sleep(cts_time)
#            st.write("Tokenizing text...")
#            time.sleep(tt_time)
#            status.update(
#                label="Operation completed!", state="complete", expanded=False
#            )
#            status.empty()

# Multithreading
        if invoices_list:
#        status_update()
            extract_text()
            





















# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# CHAPTER 3: INVOICE VERIFICATION 
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

    if st.session_state.get("chapter3"):
        st.write("")
        st.write("")
        
        control_excel_df = st.session_state.get("control_excel_df")
        text_df = st.session_state.get("text_df")

        st.title("3) INVOICE VERIFICATION")
        st.write("Please select the criteria to match the invoices with the control Excel file. The machine will scrape the files looking for a match between the value related to the selected criteria in control Excel file and in the invoice bundle.")

        col1, col2 = st.columns([5, 5])
        with col1:
            st.title("MATCHING CRITERIA")
            try: 
                matching_criteria = st.multiselect("Select the matching criteria", control_excel_df.columns) 
            except NameError:
                st.write("Please upload the control Excel file before proceeding with the invoice verification")

        with col2:
            st.title("DATAFRAME STRUCTURE")
            try: 
                invoice_number = st.selectbox('Select "Invoice Number" corresponding colum', control_excel_df.columns)
                supplier = st.selectbox('Select "Supplier" corresponding column', control_excel_df.columns)
                amount = st.selectbox('Select "Amount" corresponding column', control_excel_df.columns) 

            except NameError:
                st.write("Please upload the control Excel file before proceeding with the invoice verification")

        matching_df = pd.DataFrame(columns=[invoice_number, supplier, amount, "FileName"])
        matched_invoices = set()

        if st.button(label = "Launch invoice verification", key = 5, type = "primary", use_container_width = True):
            st.session_state["invoice_ver"] = True
        if st.session_state["invoice_ver"] == True:

# Retrieve datasets from session state
            control_excel_df = st.session_state.get("control_excel_df")
            text_df = st.session_state.get("text_df")

            if not control_excel_df.empty and not text_df.empty:                        ### activate the matching only whether the two dataset are there 
                for index_text,row_text in text_df.iterrows():
                    tokenized_text = row_text["Tokenized Text"]
                    for index_control,row_control in control_excel_df.iterrows():
                        criteria_values = [row_control[col] for col in matching_criteria]          # !!!!!!! watch out for the reference to the columns of the correct dataset
                        if all(str(value).lower() in tokenized_text for value in criteria_values):
                            invoice_num = row_control[invoice_number]
                            if invoice_num not in matched_invoices:
                                matching_df = pd.concat([matching_df, pd.DataFrame({
                                    invoice_number : [row_control[invoice_number]],
                                    supplier: [row_control[supplier]],
                                    amount: [row_control[amount]],                                 # !!!!!! watch out for the reference to the rows of the correct dataset
                                    "FileName" : [row_text["FileName"]] 
                                    })
                                ], ignore_index = True)
                                matched_invoices.add(invoice_num)                                  # !!!!!!!!!!! create a set to create a firlter for a dataframe where if something is not unique or it is already in the set won't be granted acess to the dataframe                                                     
            st.session_state["matching_df"] = matching_df                
            st.dataframe(matching_df)
        else: 
            st.write("Please upload both the control Excel file and the invoices before proceeding with the invoice verification.")

# controlla che per assocciare tutti i criteri siamo met nel tokenized_text
# opzione edit data



























# ------------------------------------------------------------------------------------------------------------------------------------------------------#
# CHAPTER 4: VALIDATION
# ------------------------------------------------------------------------------------------------------------------------------------------------------#

    if st.session_state.get("chapter4"):
        st.write("")
        st.write("")

        st.title("4) VALIDATION")
        st.write("blablablablablablablablabla")
        validation_df = st.session_state.get("matching_df")
        st.dataframe(validation_df)












# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# Info (general info & chat bot)
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

if st.session_state.get("info"): 

    logoandtitle()
    st.write("")
    st.write("")

    st.markdown(
    """
    <div style="text-align: left; align-items: left;">

    # **NAVIGATION**
    The interface has a sidebar with navigation buttons to switch between different sections:

    -   **Home**
    -   **NMP Invoice Checker**
    -   **Info**

    ####
    
    # **HOME**
    The Home section is the default landing page of the interface. It displays the ECB logo and the title "NMP INVOICE CHECKER".

    ####

    # **NMP INVOICE CHECKER**
    This section is divided into four chapters:

    #### Upload Your Control File
    Navigate to NMP Invoice Checker: Click on the "NMP Invoice Checker" button in the sidebar.

    -   Click on the "CONTROL FILE" button.
    -   Upload your control Excel file (either .xlsx or .csv format).
    -   Select the columns you want to display from the uploaded file.
    -   The selected columns will be displayed in a table.

    #### Upload Your Invoices
    Navigate to NMP Invoice Checker: Click on the "NMP Invoice Checker" button in the sidebar.

    -   Click on the "INVOICES" button.
    -   Upload your invoices in PDF format.
    -   The text from the invoices will be extracted and tokenized.

    #### Invoice Verification
    Navigate to NMP Invoice Checker: Click on the "NMP Invoice Checker" button in the sidebar.

-    Click on the "VERIFICATION" button.
-    Select the matching criteria from the control Excel file columns.
-    Select the corresponding columns for "Invoice Number", "Supplier", and "Amount"
-    Click on the "Launch invoice verification" button to start the verification process.
    
    The matching results will be displayed in a table.

    #### Validation
    Navigate to NMP Invoice Checker: Click on the "NMP Invoice Checker" button in the sidebar.

    ####

    # **INFO**
    The Info section provides general information and a chat bot for assistance.
    </div>
    """,
    unsafe_allow_html=True
)