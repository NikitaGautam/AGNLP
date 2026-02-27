from distutils.log import debug
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from scrapper import GetAllUrl
import os
from flask_executor import Executor
import threading
import re

app = Flask(__name__)
alias = ""
executor = Executor(app)

@app.route("/")
def index():
    return render_template("index.html")

def get_all_keywords(keyword):
    exclude_words = {"AND", "OR", "the", "and", "or"}
    words = re.findall(r'\b\w+\b', keyword)
    filtered_words = [word for word in words if word not in exclude_words]
    return filtered_words

# Do Form Validation
@app.route("/keysearch", methods=['GET', 'POST'])
def keysearch():
    global alias
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        alias = request.form.get('alias', 'test')
        scopus_count  = request.form.get('scopus', 5000)
        science_count  = request.form.get('science', 5000)
        wos_count  = request.form.get('wos', 5000)
        start  = request.form.get('start', 2024)
        end = request.form.get('end', 2024)
        scholar_option = request.form['option']
        allData = "DATA"
        aliasPath = os.path.join(allData, alias)
        alias = aliasPath

        all_words = get_all_keywords(keyword)
        
        if os.path.exists(aliasPath):
            return render_template('scrapper.html', error=str("Alias name cannot be reused. Please select another alias."))
        
        # thread = threading.Thread(target=GetAllUrl(keyword, alias, scopus_count, science_count, start, end, scholar_option).start_execution(),)
        # thread.start()
        check, message = GetAllUrl(keyword, alias, scopus_count, science_count, start, end, scholar_option, wos_count, all_words).start_execution()
        if not check:
            # print(message)
            # if message == "'search-results'" or message == "search-results":
            #     message = "Exception occured during execution, please recheck your search keyword."
            # message = "Exception occured during execution, please recheck your search keyword."
            return render_template('scrapper.html', error=str(message))

        else:
            if message == "Completed":
                message = "Number of search keywords is long for scienceDirect. Please check your search equation. Completed processing using scopus."
                return render_template('scrapper.html', error=str(message))

            else:
                return redirect(url_for('download_page'))

        return redirect(url_for('download_page'))
        # executor.submit(GetAllUrl(keyword, alias, scopus_count, start, end).start_execution())

    if request.method == 'GET':
        return render_template("scrapper.html")


@app.route('/download_file/<path:filename>')
def download_file(filename):
    filename = "DATA/"+filename
    return send_file(filename, as_attachment=True)


@app.route('/download_page')
def download_page(): 
    folder_path = alias
    zip_filename = alias+'.zip'

    import zipfile
    # Create a ZIP file containing all files in the folder
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    

    # return render_template('downloads.html', file1_path=zip_filename)
    import glob
    files = []

    # Iterate over files in the directory
    for file_path in glob.glob(os.path.join(os.getcwd(), "DATA/", '*.zip')):
        files.append(file_path)
    return render_template('downloads.html', files=files)
    
    
    # file1_path = alias+"/scopus-abstracts.csv"
    # file2_path = alias+"/scopus-selected.tsv"
    
    # file3_path = alias+"/fil_scholarall.csv"
    # combined_all  = alias+"/selected.tsv"
    
    # file4_path =  alias+"/scholar-selected.tsv"
    
    # file5_path = alias+"/sciencedirect-abstracts.csv"
    # file6_path = alias+"/sciencedirect-selected.tsv"
    
    # return render_template('downloads.html', file1_path=file1_path, file2_path=file2_path,
    #                        file3_path=file3_path, file4_path=file4_path,
    #                        combined_all=combined_all, file5_path=file5_path, file6_path=file6_path)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

