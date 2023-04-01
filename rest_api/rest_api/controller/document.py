import os
import logging
from typing import List
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from haystack.document_stores import BaseDocumentStore
from haystack.schema import Document

from rest_api.utils import get_app, get_pipelines
from rest_api.config import LOG_LEVEL, FILE_UPLOAD_PATH
from rest_api.schema import FilterRequest


logging.getLogger("haystack").setLevel(LOG_LEVEL)
logger = logging.getLogger("haystack")


router = APIRouter()
app: FastAPI = get_app()
document_store: BaseDocumentStore = get_pipelines().get("document_store", None)


@router.post("/documents/get_by_filters", response_model=List[Document], response_model_exclude_none=True)
def get_documents(filters: FilterRequest):
    """
    This endpoint allows you to retrieve documents contained in your document store.
    You can filter the documents to retrieve by metadata (like the document's name),
    or provide an empty JSON object to clear the document store.
    (GET documents from Elatic)

    Example of filters:
    `'{"filters": {{"name": ["some", "more"], "category": ["only_one"]}}'`

    To get all documents you should provide an empty dict, like:
    `'{"filters": {}}'`
    """
    docs = document_store.get_all_documents(filters=filters.filters)
    for doc in docs:
        doc.embedding = None
    return docs


@router.post("/documents/delete_by_filters", response_model=bool)
def delete_documents(filters: FilterRequest):
    """
    This endpoint allows you to delete documents contained in your document store.
    You can filter the documents to delete by metadata (like the document's name),
    or provide an empty JSON object to clear the document store.
    (Don't delete source file in Haystack)

    Example of filters:
    `'{"filters": {{"name": ["some", "more"], "category": ["only_one"]}}'`

    To get all documents you should provide an empty dict, like:
    `'{"filters": {}}'`
    """
    document_store.delete_documents(filters=filters.filters)
    return True

# Delete single document from filesystem and elastic index
@router.delete("/documents/{file_id}", response_model=bool)
def delete_document(file_id: str):
    """
    This endpoint allows you to delete a document from Haystack filesystem and elastic index.

    Example of file_id:
    `'some_file_id'`
    """
    # Delete the file from the haystack file system
    file_path = Path(FILE_UPLOAD_PATH) / file_id
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    os.remove(file_path)

    # Delete the elastic index
    document_store.delete_documents(filters={"file_id": file_id})

    return True

# Download the file from the URL
@router.get("/files/{file_id}")
def download_document(file_id: str):
    """
    This endpoint allows you to download a document from the document store.

    Example of file_id:
    `'some_file_id'`
    """
    file_path = Path(FILE_UPLOAD_PATH) / file_id
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path)