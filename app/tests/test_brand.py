
async def test_get_brands_returns_200(client):
    response = await client.get('api/v1/brands/')
    assert response.json()['success'] == True
    assert response.status_code == 200

async def test_get_brands_returns_307(client):
    response = await client.get('api/v1/brands') # redirect на api/v1/brands/
    assert response.status_code == 307

async def test_get_brands_returns_list(client):
    response = await client.get('api/v1/brands/')
    assert isinstance(response.json()['brands'], list)

async def test_create_brand_returns_201(client):
    response = await client.post(
        'api/v1/brands/',
        json={
            'name': 'Leo',
        }
    )
    assert response.status_code == 201

async def test_get_brand_returns_404(client):
    response = await client.get('api/v1/brands/1')
    assert response.status_code == 404

async def test_create_brand_returns_422(client):
    response = await client.post(
        'api/v1/brands/',
        json={},
    )
    assert response.status_code == 422

