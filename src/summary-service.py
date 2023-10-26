from flask import Flask, request, render_template
from transformers import pipeline
import enchant
from googletrans import Translator

source_lang = "en"
target_lang = "fr"

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, src=source_lang, dest=target_lang).text
    return translated_text

def split_text(text, max_length):
    chunks = []
    words = text.split()
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) <= max_length:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def correct_text(text):
    checker = enchant.Dict("fr_FR")
    words = text.split()
    corrected_words = []

    for word in words:
        if not checker.check(word):
            suggestions = checker.suggest(word)
            if suggestions:
                corrected_word = suggestions[0]
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)

    corrected_text = ' '.join(corrected_words)
    return corrected_text


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def accueil():
    options = [
        {'value': 't5-base', 'label': 'Google T5 Base'},
        {'value': 'facebook/bart-large-cnn', 'label': 'Facebook BART'},
        {'value': 't5-small', 'label': 'Google T5 Small (Rapide)'},
    ]

    if request.method == 'POST':
        texte = request.form['texte']
        modele = request.form['modele']
        
        summarizer = pipeline("summarization", model=modele)
        
        chunks = []  # Liste pour stocker les morceaux du texte
        chunk_size = 512  # Taille maximale d'un morceau
        
        # Séparer le texte en paragraphes
        paragraphs = texte.split('\n\n')
        
        try:
            # Traiter chaque paragraphe
            for paragraph in paragraphs:
                # Vérifier si le paragraphe dépasse la limite de 512
                if len(paragraph) > chunk_size:
                    # Diviser le paragraphe en morceaux de taille équivalente
                    num_chunks = len(paragraph) // chunk_size + 1
                    chunk_length = len(paragraph) // num_chunks
                    for i in range(num_chunks):
                        start = i * chunk_length
                        end = (i + 1) * chunk_length
                        chunks.append(paragraph[start:end])
                else:
                    chunks.append(paragraph)
        
            summaries = []  # Liste pour stocker les résumés partiels
        
            # Générer des résumés pour chaque morceau
            for chunk in chunks:
                summary = summarizer(chunk, max_length=275, min_length=10, do_sample=True)
                summaries.append(summary[0]['summary_text'])
                
            # Combinaison des résumés partiels
            sum_text = ' '.join(summaries)
            
            text_chunks = split_text(sum_text, 500)
            translated_chunks = []
            corrected_chunks = []

            for part_text in text_chunks:
                translated_text = translate_text(part_text,source_lang, target_lang)
                translated_chunks.append(translated_text)

            for part_text in translated_chunks:
                corrected_text = correct_text(part_text)
                corrected_chunks.append(corrected_text)

            combined_text = ' '.join(corrected_chunks)
            
            

        except Exception as e:
                combined_text = 'Erreur de résumé : ' + str(e)
             
        return render_template('text_summarization.html', texte_synthetise=combined_text, modele=modele, texte=texte, options=options )
    
    return render_template('text_summarization.html')
