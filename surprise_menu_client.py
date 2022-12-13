import cam
from text import TfidfVectorizer
from pairwise import cosine_similarity
import docx2txt
import gdown

class SurpriseMenuClient:
    def __init__(self):
        self.worker = cam.Client("https://digibp.herokuapp.com/engine-rest")
        self.worker.subscribe("GetSurpriseMenu", self.get_surprise_menu_callback, "saechsiluute")
        self.worker.polling()

    def get_surprise_menu_callback(self, taskid, response):
        '''First get the variables from the process'''
        try:
            doc_url = response[0]['variables']['doc_url']['value']
        except:
            doc_url = False

        try:
            swissmedic_id = response[0]['variables']['swissmedic_id']['value']
        except:
            swissmedic_id = False

        try:
            case_id = response[0]['variables']['case_id']['value']
        except:
            case_id = False

        '''Download the document to local storage to access properly'''
        output = "{0}_InputDoc.docx".format(case_id)
        gdown.download(doc_url, output, quiet=False, fuzzy=True)

        '''Document comparing based on Tfidf'''

        base_document = docx2txt.process(output)
        documents = [docx2txt.process("Benchmark.docx")]

        vectorizer = TfidfVectorizer()

        # To make uniformed vectors, both documents need to be combined first.
        documents.insert(0, base_document)
        embeddings = vectorizer.fit_transform(documents)

        cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()

        highest_score = 0
        highest_score_index = 0
        for i, score in enumerate(cosine_similarities):
            if highest_score < score:
                highest_score = score
                highest_score_index = i

        comp_score = highest_score
        doc_check_message = 'Document was successfully checked'

        if doc_url == False:
            comp_score = 0
            doc_check_message = 'doc_url is missing'

        variables = {"comp_score": comp_score, "swissmedic_id": swissmedic_id, "doc_check_message": doc_check_message}
        self.worker.complete(taskid, **variables)


if __name__ == '__main__':
    SurpriseMenuClient()
