from .agencies import AgencyMetadata, AgencyData
from .dockets import RegsDotGovData, Dockets
from .presidents import Presidents
from .rin import RegInfoData


class PreprocessingError:
    pass


def process_documents(documents: list[dict], which: str = "all", docket_data_source: str = "dockets"):

    source_dict = {
        "dockets": Dockets, 
        "regulations_dot_gov_info": RegsDotGovData
        }
    
    clean_fields = {
        "agencies": AgencyData, 
        "dockets": source_dict.get(docket_data_source, Dockets), 
        "presidents": Presidents, 
        "rin": RegInfoData, 
        }
    
    if which == "all":
    
        for k, v in clean_fields.items():
            if k == "agencies":
                metadata, schema = AgencyMetadata().get_agency_metadata()
                documents = v(documents, metadata, schema).process_agency_data()
            else:
                documents = v(documents).process_data()
    
    elif which in clean_fields.keys():
        documents = clean_fields[which](documents).process_data()
    
    else:
        raise PreprocessingError
    
    return documents
