import cam
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt

class SurpriseMenuClient:
    def __init__(self):
        self.worker = cam.Client("https://digibp.herokuapp.com/engine-rest")
        self.worker.subscribe("GetSurpriseMenu", self.get_surprise_menu_callback, "saechsiluute")
        self.worker.polling()

    def get_surprise_menu_callback(self, taskid, response):
        try:
            duc_url = response[0]['variables']['doc_url']['value']
        except:
            doc_url = False

        try:
            swissmedic_id = response[1]['variables']['swissmedic_id']['value']
        except:
            swissmedic_id = False
        
        if doc_url:
            score = 0.6
         else:
            score = 0.01
        
        if swissmedic_id in input_file:
		    swissmedic_id = swissmedic_id
	    else:
		    swissmedic_id = "Error: Swissmedic ID is not in accordance with Approved Drug Information"

        variables = {"score": score, "swissmedic_id": swissmedic_id}
        self.worker.complete(taskid, **variables)


if __name__ == '__main__':
    SurpriseMenuClient()
