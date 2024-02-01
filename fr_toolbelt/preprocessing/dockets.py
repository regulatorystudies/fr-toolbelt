# no imports; all native python
#from copy import deepcopy


class RegsDotGovData:

    def __init__(self, documents: list[dict], key: str = "regulations_dot_gov_info") -> None:
        self.documents = documents
        self.key = key

    def __extract_docket_info(self, document: dict) -> str | None:
        
        docket_info = document.get(self.key, {})
        
        if len(docket_info) == 0:
            values = None
        elif isinstance(docket_info, list):
            values = [docket.get("docket_id") for docket in docket_info]
        elif isinstance(docket_info, dict):
            values = [docket_info.get("docket_id")]

        if values is not None:
            values = "; ".join(v for v in values if v is not None)
        
        return values

    def __create_docket_key(self, document: dict, values: str = None) -> dict:
        document_copy = document.copy()
            
        document_copy.update({
            "docket_id": values, 
            })
        
        return document_copy
    
    def process_data(self) -> list[dict]:
        return [self.__create_docket_key(doc, values=self.__extract_docket_info(doc)) for doc in self.documents]


if __name__ == "__main__":
    
    pass
