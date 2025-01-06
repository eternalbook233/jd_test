from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import declarative_base

# 创建映射基类
Base = declarative_base()


class BrandTable(Base):
    __tablename__ = 'brand'
    brandId = Column(String(10), primary_key=True)
    brandName = Column(String(30))


class SkuTable(Base):
    __tablename__ = 'skuInfo'
    wareId = Column(String(12), primary_key=True)
    saleState = Column(Integer)
    name = Column(String(75))
    modifyTime = Column(TIMESTAMP)


class SkuInfoTable(Base):
    __tablename__ = 'sku_info'
    sku = Column(String(12), primary_key=True)
    skuName = Column(String(75))
    skuCat1 = Column(String(10))
    oneLevelId = Column(String(10))
    skuCat2 = Column(String(35))
    twoLevelId = Column(String(10))
    skuCat3 = Column(String(25))
    categoryId = Column(String(10))
    brand_name = Column(String(30))
    skuPrice = Column(Integer)
    skuPrice_b = Column(Integer)
    skuStatus = Column(String(100))
    Status = Column(String(1))
    stockResp = Column(String(2))
    modifyTime = Column(TIMESTAMP)


class SkuCShow(Base):
    __tablename__ = 'sku_CShow'
    sku = Column(String(12), primary_key=True)
    skuName = Column(String(75))
    CShow = Column(String(6))


# 创建EP数据库
def create_table(shop_name):
    """
    创建 '未入EP查询列表' 表格。
    """
    # 创建引擎，添加 if_exists='append' 参数
    engine = create_engine(f'mysql://root:Qq233333@8.137.77.225/{shop_name}', echo=True, pool_pre_ping=True,
                           pool_recycle=3600)
    # engine = create_engine(f'mysql://root:Qq233333@wtet.site/juecai', echo=True, pool_pre_ping=True, pool_recycle=3600)
    # 使用 Base.metadata.create_all 创建表，只会创建不存在的表
    Base.metadata.create_all(bind=engine, checkfirst=True)
    return engine
