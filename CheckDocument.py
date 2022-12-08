import cam

class CheckDocument:
    def __init__(self):
        self.worker = cam.Client("https://digibp.herokuapp.com/engine-rest")
        self.worker.subscribe("CheckDocument", self.get_surprise_menu_callback, "saechsiluute")
        self.worker.polling()

    def check_document(self, taskid, response):
        try:
            vegetarian_guests = response[0]['variables']['input']['value']
        except:
            vegetarian_guests = False

        if vegetarian_guests:
            score = "True"
        else:
            score = "False"

        variables = {"score": score}
        self.worker.complete(taskid, **variables)


if __name__ == '__main__':
    CheckDocument()