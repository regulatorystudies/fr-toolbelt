from .agencies import AgencyMetadata, AgencyData
from .dockets import RegsDotGovData, Dockets
from .presidents import Presidents
from .rin import RegInfoData


class PreprocessingError:
    pass


def process_documents(documents: list[dict], which: str | list | tuple = "all", docket_data_source: str = "dockets"):
    """_summary_

    Args:
        documents (list[dict]): Documents to process.
        which (str | list | tuple, optional): _description_. Defaults to "all".
        docket_data_source (str, optional): _description_. Defaults to "dockets".

    Raises:
        PreprocessingError: _description_

    Returns:
        _type_: _description_
    """
    # dictionary of alternative sources
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
                documents = v(documents, metadata, schema).process_data()
            else:
                documents = v(documents).process_data()
    
    elif isinstance(which, str) and (which in clean_fields.keys()):
        documents = clean_fields[which](documents).process_data()
    
    elif isinstance(which, (list, tuple)):
        valid_fields = (w for w in which if w in clean_fields.keys())
        for field in valid_fields:
            documents = clean_fields[field](documents).process_data()
    
    else:
        raise PreprocessingError
    
    return documents
