import requests
from sqlalchemy.orm import sessionmaker
import createTable
from shopInfo import shopInfo
from 获取商品类目 import getcategory

headers_s, shop_name, Cookie = shopInfo()
# 获取已有引擎
engine = createTable.create_table(shop_name)
# 创建Session
Session = sessionmaker(bind=engine)
session = Session()
# 分页遍历SKU
page_size = 1
page_number = 1  # 下面是（X，1） 就填几
headers = {
    'vsp60cookies': 'vsp_api=35C7E14F072917A332DA32850DD883BB;vsp_user_group=B227B06FC1D69F8DC0B955735AA55628C6EABD65F0A63E6ED72060C09A227F9F5D5CF926967D9A5C8CD17A66A82B68478EAC5D3117A38023012C969A993BE2096AB7B3DC32C53FD362A889C0B30C52F760D1E9FD8C4415E4B1C59B52E55C18DD61A89BD42096C642B3097F13A372C889B41EE99FF10AAA07F33209BB2938E807C737D33976177C2624348FA7B2E19490',
}
cookies = {
    'vsp_api': '35C7E14F072917A332DA32850DD883BB'
}
while True:

    products = session.query(createTable.SkuTable).limit(page_size).offset((page_number - 1) * page_size).all()
    if not products:
        break
    page_number += 1
    for product in products:
        sku = product.wareId
        modify_time = product.modifyTime
        if product.saleState != 1:
            continue
        response = requests.get(
            f'https://api.m.jd.com/?appid=vsp60&functionId=vsp_index_sku_getAsynDetail&body=%7B%22skuId%22:%22{sku}%22,%22skuNum%22:1,%22provinceId%22:1,%22cityId%22:72,%22countyId%22:2819,%22townId%22:0,%22addressId%22:0,%22addressDetail%22:%22%E5%8C%97%E4%BA%AC%E6%9C%9D%E9%98%B3%E5%8C%BA%E4%B8%89%E7%8E%AF%E5%88%B0%E5%9B%9B%E7%8E%AF%E4%B9%8B%E9%97%B4%22%7D&cthr=1&loginType=14&t=1699855410466',
            headers=headers)
        result_j = response.json()
        response2 = requests.get(
            f"https://vapi.jd.com/index/sku/getDetail?skuId=100103147296&skuSpuVopPoolSwitch=1&p=&provinceId=1&cityId=72&countyId=2819&townId=0&addressId=0",
            cookies=cookies)
        result_j2 = response2.json()
        # print(result_j)
        # print(result_j2)
        info = None

        try:
            oneLevelId = result_j2['result']['categoryNavigate']['oneLevelId']
            twoLevelId = result_j2['result']['categoryNavigate']['twoLevelId']
            categoryId = result_j2['result']['categoryNavigate']['categoryId']
            skuName = result_j['result']['name']
            skuPrice = result_j['result']['skuPrice']['readPrice']
            skuPrice_b = result_j['result']['skuPrice']['purchasePrice']  # 协议价
            if skuPrice_b is None:
                skuPrice_b = 0
            skuStatus = result_j['result']['saleStateResp']['reasonList']
            category = getcategory(sku)
            skuCat1, skuCat2, skuCat3, brand_name = category[:4]
            Status = result_j['result']['saleStateResp']['saleState']
            stockResp = result_j['result']['stockResp']['state']
            info = createTable.SkuInfoTable(sku=sku, skuName=skuName, skuCat1=skuCat1, skuCat2=skuCat2, skuCat3=skuCat3,
                                            brand_name=brand_name, skuPrice=skuPrice, skuPrice_b=skuPrice_b,
                                            skuStatus=str(skuStatus),
                                            Status=Status, stockResp=stockResp, oneLevelId=oneLevelId,
                                            twoLevelId=twoLevelId, categoryId=categoryId,modifyTime = modify_time)
        except Exception as e:
            info = createTable.SkuInfoTable(sku=sku, skuName=None, skuCat1=None, skuCat2=None, skuCat3=None,
                                            brand_name=None, skuPrice=None, skuPrice_b=-1, skuStatus=None,
                                            Status=None, stockResp=None, oneLevelId=None,
                                            twoLevelId=None, categoryId=None,modifyTime =None)
            break
        finally:
            print(info)
            session.merge(info)  # 添加这一行
            session.commit()
            session.close()
