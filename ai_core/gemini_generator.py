from google import genai
from google.genai import types

from backend.config import get_settings


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI assistant for drafting legal-document templates.

Your task is to create clear, structured, editable
legal-document drafts from the user's supplied facts.

Do not invent personal data, amounts, dates, addresses,
laws, authorities, citations, or obligations that the user
did not provide.

Where information is missing and important, use a clearly
marked placeholder such as [INSERT DETAILS].

Use professional legal-document structure, but write in
understandable language.

Return plain text only.

Always include:

1. DOCUMENT TITLE
2. PARTIES
3. EFFECTIVE DATE
4. RECITALS / BACKGROUND when appropriate
5. DEFINITIONS when useful
6. MAIN TERMS / CLAUSES
7. CONFIDENTIALITY, TERMINATION, DISPUTE/LAW clauses
   only when appropriate
8. SIGNATURES

Include a short final section titled:

IMPORTANT NOTICE

The notice should state that the output is a draft for
review and is not a substitute for advice from a qualified
lawyer.

Do not claim that the document is legally valid in every
jurisdiction.
"""


class GeminiDocumentGenerator:

    def __init__(self):

        settings = get_settings()

        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model

        self.client = None

        if self.api_key:

            self.client = genai.Client(
                api_key=self.api_key
            )


    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:

        if not self.api_key or not self.client:

            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add it to the .env file and restart "
                "the backend."
            )


        prompt = f"""
Create a legal-document draft using ONLY the following
user-provided inputs.

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Additional instructions:

- Interpret semicolon-separated terms as separate
  requested clauses.

- Keep the supplied names, dates, and commercial
  terms accurate.

- Do not invent missing facts.

- Use placeholders for missing information.

- Make the document easy to edit.

- Do not use Markdown code fences.
"""


        response = self.client.models.generate_content(

            model=self.model,

            contents=prompt,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_INSTRUCTION,

                temperature=0.3,

                max_output_tokens=6000,
            ),
        )


        text = (
            response.text or ""
        ).strip()


        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        return text