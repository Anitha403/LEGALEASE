from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, DocumentResponse

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        print("DEBUG: /generate called")
        print("DEBUG: Model:", generator.model)
        print("DEBUG: API key loaded:", bool(generator.api_key))

        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        print("DEBUG: Gemini generation successful")

        return DocumentResponse(
            document_type=request.document_type,
            content=content,
        )

    except Exception as exc:
        print("=" * 60)
        print("GENERATE ERROR:")
        print(type(exc).__name__)
        print(str(exc))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=f"Gemini generation error: {type(exc).__name__}: {exc}",
        ) from exc