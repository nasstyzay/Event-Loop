from aiohttp import web
import json
from datetime import datetime

ads = []

async def get_ad(request):
    ad_id = int(request.match_info['id'])
    ad = next((ad for ad in ads if ad['id'] == ad_id), None)
    if ad:
        return web.json_response(ad)
    return web.HTTPNotFound(text='Ad not found')

async def create_ad(request):
    data = await request.json()
    ad_id = len(ads) + 1
    ad = {
        "id": ad_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "creation_date": datetime.utcnow().isoformat(),
        "owner": data.get("owner")
    }
    ads.append(ad)
    return web.json_response(ad, status=201)

async def delete_ad(request):
    ad_id = int(request.match_info['id'])
    global ads
    ads = [ad for ad in ads if ad['id'] != ad_id]
    return web.Response(text='Ad deleted successfully')


app = web.Application()
app.router.add_get('/ads/{id}', get_ad)
app.router.add_post('/ads', create_ad)
app.router.add_delete('/ads/{id}', delete_ad)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8080)

