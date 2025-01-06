import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
import createTable
from shopInfo import shopInfo

headers, shop_name, Cookie = shopInfo()
params = {
    '_source': 'pop',
}
response = requests.get('https://vcgoods.jd.com/sub_item/item/initItemListPage', params=params, headers=headers)
print(response.text)
# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(response.text, 'html.parser')
# 定位<select>标签
select_tag = soup.find('select', {'id': 'brandIdList'})
# 定位所有<option>标签
options = select_tag.find_all('option')
# 输出所有选项的值
# 创建数据库表
engine = createTable.create_table(shop_name)
# SQLAlchemy: 创建会话
Session = sessionmaker(bind=engine)
session = Session()
# 将每个<option>元素保存到数据库
for option in options:
    brand_value = option['value']
    brand_name = option.text
    new_option = createTable.BrandTable(brandId=brand_value,
                                        brandName=brand_name)  # 使用BrandTable类
    session.merge(new_option)
# 提交更改
session.commit()
# 关闭会话
session.close()
