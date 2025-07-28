import unittest


class ReviewsDomainTest(unittest.TestCase):

    def setUp(cls):
        """Configuração executada uma vez antes de todos os testes."""

    def test_create_review_ok(self):
        """
        Teste da criação e avaliação de uma review: `create_review`
        CASO: Sucesso
        ESPERADO: chamada dos método `_evaluate_text_sentiment` e `review_crud.create`, retorna um dicionario com a review criada.
        """

    def test_create_review_db_raise(self):
        """
        Teste da criação e avaliação de uma review: `create_review`
        CASO: Erro na inserção no BD
        ESPERADO: chamada dos método `_evaluate_text_sentiment` e `review_crud.create`, porém da raise na chamada do reate, deve retornar o mesmo raise sem tratamento.
        """

    def test_get_reviews_ok(self):
        """
        Teste da listagem de reviews: `get_reviews`
        CASO: Sucesso
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, uma lista de dicionarios de reviews.
        """

    def test_get_reviews_empty(self):
        """
        Teste da listagem de reviews: `get_reviews`
        CASO: Sucesso, porém com lista vazia devido retorno vazio de `review_crud.read_by_date_range`
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, uma lista vazia.
        """

    def test_get_reviews_by_id_ok(self):
        """
        Teste da listagem de reviews: `get_review_by_id`
        CASO: Sucesso
        ESPERADO: chamada dos método `review_crud.read_one`, retorna uma dicionario de reviews.
        """

    def test_get_reviews_by_id_not_found(self):
        """
        Teste da listagem de reviews: `get_review_by_id`
        CASO: Not Found
        ESPERADO: chamada dos método `review_crud.read_one`, levanta um raise de HTTPException status 404.
        """

    def test_get_report_ok(self):
        """
        Teste da listagem de reviews: `get_review_by_id`
        CASO: Not Found
        ESPERADO: chamada dos método `review_crud.read_by_date_range`, retorna dicionario com a contagem de itens "sentiment" (ex: `{"positiva": 13,"negativa": 6,"neutra": 3}`)
        """
