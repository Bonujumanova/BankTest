class RequestSpecifications:
    @staticmethod
    def base_headers(self):
        return {
                "accept": "application/json",
                "Content-Type": "application/json"
            }

    @staticmethod
    def authorization_headers(self):
        ...