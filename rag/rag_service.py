"""RAG summarize service for retrieving context and generating final answers."""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from rag.vector_store import VectorStoreService
from utils.logger_handler import logger
from utils.prompt_loader import load_rag_prompts


class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()
        self._docs_ready = False

    def _init_chain(self):
        return self.prompt_template | self.model | StrOutputParser()

    def _ensure_docs_loaded(self):
        if self._docs_ready:
            return

        try:
            self.vector_store.load_document()
        except Exception as exc:
            # Keep app usable even if first-time indexing fails.
            logger.warning(f"[RagSummarizeService]load document failed: {exc}")
        finally:
            self._docs_ready = True

    def retrieve_docs(self, query: str) -> list[Document]:
        self._ensure_docs_loaded()
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retrieve_docs(query)
        context_lines = []

        for idx, doc in enumerate(context_docs, start=1):
            context_lines.append(
                f"[参考资料{idx}] 参考内容: {doc.page_content} | 参考元数据: {doc.metadata}"
            )

        context = "\n".join(context_lines)

        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )
