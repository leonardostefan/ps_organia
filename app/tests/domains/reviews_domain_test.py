import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import HTTPException

# Ajuste este import conforme sua estrutura real
from app.domains.reviews import ReviewDomain


class ReviewsDomainTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """
        Configuração executada uma vez antes de todos os testes.
        """

        self.domain = ReviewDomain()
        self.session = MagicMock()
        self.review_input = MagicMock()
        self.review_input.dict.return_value = {"text": "Serviço muito bom!"}

    @patch("domains.reviews.review_crud.create")
    @patch.object(ReviewDomain, "_evaluate_text_sentiment", return_value="positiva")
    async def test_create_review_ok(self, mock_sentiment, mock_create):
        """
        Teste da criação e avaliação de uma review: `create_review`
        CASO: Sucesso
        ESPERADO: chamada dos método `_evaluate_text_sentiment` e `review_crud.create`,
            retorna um dicionario com a review criada.
        """

        mock_created = MagicMock()
        mock_created.to_response.return_value = {
            "id": 1,
            "text": "Serviço muito bom!",
            "sentiment": "positiva",
        }
        mock_create.return_value = mock_created

        result = await self.domain.create_review(self.review_input, self.session)

        mock_sentiment.assert_called_once()
        mock_create.assert_called_once()
        self.assertIn("id", result)
        self.assertEqual(result["sentiment"], "positiva")

    @patch("domains.reviews.review_crud.create", side_effect=Exception("Erro BD"))
    @patch.object(ReviewDomain, "_evaluate_text_sentiment", return_value="neutra")
    async def test_create_review_db_raise(self, mock_sentiment, mock_create):
        """
        Teste da criação e avaliação de uma review: `create_review`
        CASO: Erro na inserção no BD
        ESPERADO: chamada dos método `_evaluate_text_sentiment` e `review_crud.create`, porém da raise na chamada
            do create, deve retornar o mesmo raise sem tratamento.
        """
        with self.assertRaises(Exception) as context:
            await self.domain.create_review(self.review_input, self.session)
        self.assertIn("Erro BD", str(context.exception))
        mock_sentiment.assert_called_once()
        mock_create.assert_called_once()

    @patch("domains.reviews.review_crud.read_by_date_range", new_callable=AsyncMock)
    async def test_get_reviews_ok(self, mock_read):
        """
        Teste da listagem de reviews: `get_reviews`
        CASO: Sucesso
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, uma lista de dicionarios de reviews.
        """

        mock_review = MagicMock()
        mock_review.to_response.return_value = {"id": 1, "sentiment": "positiva"}
        mock_read.return_value = [mock_review]

        result = await self.domain.get_reviews(self.session, "2024-01-01", "2025-01-01")

        mock_read.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["sentiment"], "positiva")

    @patch("domains.reviews.review_crud.read_by_date_range", new_callable=AsyncMock)
    async def test_get_reviews_empty(self, mock_read):
        """
        Teste da listagem de reviews: `get_reviews`
        CASO: Sucesso, porém com lista vazia devido retorno vazio de `review_crud.read_by_date_range`
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, uma lista vazia.
        """

        mock_read.return_value = []
        result = await self.domain.get_reviews(self.session, "2024-01-01", "2025-01-01")
        mock_read.assert_called_once()
        self.assertEqual(result, [])

    @patch("domains.reviews.review_crud.read_one", new_callable=AsyncMock)
    async def test_get_reviews_by_id_ok(self, mock_read):
        """
        Teste da busca de review especifica: `get_review_by_id`
        CASO: Sucesso
        ESPERADO: chamada dos método `review_crud.read_one`, retorna uma dicionario da review.
        """
        mock_review = MagicMock()
        mock_review.to_response.return_value = {"id": 10, "sentiment": "neutra"}
        mock_read.return_value = mock_review

        result = await self.domain.get_review_by_id(10, self.session)
        mock_read.assert_called_once()
        self.assertEqual(result["id"], 10)

    @patch(
        "domains.reviews.review_crud.read_one",
        new_callable=AsyncMock,
        return_value=None,
    )
    async def test_get_reviews_by_id_not_found(self, mock_read):
        """
        Teste da busca de review especifica: `get_review_by_id`
        CASO: Not Found
        ESPERADO: chamada dos método `review_crud.read_one`, levanta um raise de HTTPException status 404.
        """
        with self.assertRaises(HTTPException) as context:
            await self.domain.get_review_by_id(99, self.session)
        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Review not found", context.exception.detail)

    @patch("domains.reviews.review_crud.read_by_date_range", new_callable=AsyncMock)
    async def test_get_report_ok(self, mock_read):
        """
        Teste da listagem de reviews: `get_review_by_id`
        CASO: Not Found
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, retorna dicionario com a contagem de itens
            "sentiment" (ex: `{"positiva": 13,"negativa": 6,"neutra": 3}`)
        """

        mock_r1 = MagicMock()
        mock_r1.to_response.return_value = {"sentiment": "positiva"}
        mock_r2 = MagicMock()
        mock_r2.to_response.return_value = {"sentiment": "negativa"}
        mock_r3 = MagicMock()
        mock_r3.to_response.return_value = {"sentiment": "positiva"}
        mock_read.return_value = [mock_r1, mock_r2, mock_r3]

        result = await self.domain.get_report("2024-01-01", "2025-01-01", self.session)
        self.assertEqual(result["positiva"], 2)
        self.assertEqual(result["negativa"], 1)
