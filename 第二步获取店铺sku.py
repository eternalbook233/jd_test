from datetime import datetime, timezone

import requests
from sqlalchemy.orm import sessionmaker
import createTable
from shopInfo import shopInfo

headers, shop_name, Cookie = shopInfo()
engine = createTable.create_table(shop_name)
# 创建Session
Session = sessionmaker(bind=engine)
session = Session()
# chunk_size = 100
# 分页遍历SKU
page_size = 1
page_number = 1
while True:
    brandIds = []
    brands = session.query(createTable.BrandTable).limit(page_size).offset((page_number - 1) * page_size).all()
    if not brands:
        break
    for brand in brands:
        brandId = brand.brandId
        brandIds.append(brandId)
    result_string = ','.join(brandIds)
    print(result_string)
    page_number += 1
    pageNo = 1
    try:
        while True:
            data = {
                '_brandIdList': '1',
                'saleState': '-1',
                'itemType': '-1',
                'brandIdList': result_string,
                'categoryIdList': '',
                'length': '1000',
                'page': pageNo,
                'sidx': 'wareId',
                'sord': 'desc',
            }
            response = requests.post('https://vcgoods.jd.com/sub_item/item/findItemList', headers=headers, data=data)
            response_json = response.json()
            # print(data)
            count_ = response_json['total']
            pageNo += 1
            data_list_ = response_json['jsonList']
            rows = [{'wareId': item['wareId'], 'saleState': item['saleState'], 'name': item['name'],
                     'modifyTime': datetime.fromtimestamp(item['modifyTime'] / 1000, tz=timezone.utc)  # 转换为时区感知的 UTC 时间
                     } for item in data_list_]
            for row in rows:
                skuInfo = createTable.SkuTable(**row)
                session.merge(skuInfo)
            # 在循环外部提交事务
            session.commit()
            if count_ < pageNo:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 关闭会话
        session.close()
