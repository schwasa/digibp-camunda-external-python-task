import cam
#import random


class SurpriseMenuClient:
    def __init__(self):
        self.worker = cam.Client("https://digibp.herokuapp.com/engine-rest")
        self.worker.subscribe("GetSurpriseMenu", self.get_surprise_menu_callback, "saechsiluute")
        self.worker.polling()

    def get_surprise_menu_callback(self, taskid, response):
        try:
            vegetarian_guests = response[0]['variables']['vegetarian']['value']
        except:
            vegetarian_guests = False

        try:
            doc_url = response[1]['variables']['doc_url']['value']
        except:
            doc_url = False
            
        if vegetarian_guests:
            score = 0.6
        else:
            score = 0.1

        variables = {"score": score}
        self.worker.complete(taskid, **variables)


if __name__ == '__main__':
    SurpriseMenuClient()
