import pytest

async def test_post_word(client):
    '''Тест ручки добавления слова'''
    response = await client.post("/words/", json={"word": "apple", "word_translate": "яблоко"})
    assert response.status_code == 201
    assert response.json()["word"] == "apple"
    assert response.json()["word_translate"] == "яблоко"

async def test_get_word(client, test_words):
    '''Тест ручки получения слова'''
    response = await client.get("/words/1")
    assert response.status_code == 200
    assert response.json()["word"] == "apple"
    assert response.json()["word_translate"] == "яблоко"

async def test_get_word_error(client, test_words):
    '''Тест ручки получения несуществующего слова'''
    response = await client.get("/words/300")
    assert response.status_code == 404

async def test_get_all_words(client, test_words):
    '''Тест ручки получения всех слов'''
    response = await client.get("/words/")
    assert response.status_code == 200
    assert len(response.json()) == 2

async def test_patch_word_translate(client, test_words):
    '''Тест ручки обновления слова (перевод)'''
    response = await client.patch("/words/1", json={"word": "apple", "word_translate": "яблочко_вкусное"})
    assert response.status_code == 200
    assert response.json()["word"] == "apple"
    assert response.json()["word_translate"] == "яблочко_вкусное"

async def test_patch_word(client, test_words):
    '''Тест ручки обновления слова (само слово)'''
    response = await client.patch("/words/1", json={"word": "talk", "word_translate": "яблоко"})
    assert response.status_code == 200
    assert response.json()["word"] == "talk"
    assert response.json()["word_translate"] == "яблоко"

async def test_patch_word_error(client, test_words):
    '''Тест ручки обновления несуществующего слова'''
    response = await client.patch("/words/300", json={"word": "apple", "word_translate": "яблоко"})
    assert response.status_code == 404

async def test_delete_word(client, test_words):
    '''Тест ручки удаления слова'''
    response = await client.delete("/words/1")
    assert response.status_code == 204
    response1 = await client.get(f"/words/{1}")
    assert response1.status_code == 404

async def test_delete_word_error(client, test_words):
    '''Тест ручки удаления несуществующего слова'''
    response = await client.delete("/words/300")
    assert response.status_code == 404

async def test_delete_words(client, test_words):
    '''Тест ручки удаления всех слов'''
    response = await client.delete("/words/")
    assert response.status_code == 204

