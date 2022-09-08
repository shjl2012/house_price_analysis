# house_price_prediction
旨在利用實價登錄資料獲得房屋的位置和房地產特徵，環域分析250m、500m、750m以內房屋周遭環境之六大指標，再以機器學習模型預測房價。

### 六大指標
* 1 醫療設施 - 醫院、診所、牙醫、藥局
* 2 經濟指標 - 便利商店、速食店
* 3 教育資源 - 學校、大專院校、圖書館
* 4 公共安全 - 警局、消防局、加油站、宮廟
* 5 自然環境 - 公園綠地、水岸、墓地
* 6 交通運輸 - 捷運站、火車站、輕軌站、公車站


## 使用套件
* pandas、geopandas、sklearn、tensorflow

## 資料來源
* 政府開放資料(https://data.gov.tw/)
* 社會經濟資料服務平台(https://segis.moi.gov.tw/)
* 內政部實價登錄網站(https://lvr.land.moi.gov.tw/)
* OpenStreetMap(https://www.openstreetmap.org/)

## 作業流程

### 1. 資料挖掘

    1.1 於實價登錄網站上下載成交房屋資料之價格與基本資訊(交易年份、地址、屋齡、格局、電梯)
  
    1.2 於政府開放資料集以及OSM中取得六大指標之資料(醫療設施、經濟指標、教育資源、公共安全、自然環境、交通運輸)


### 2. 資料清洗

    2.1 對於取得的房屋資料、醫療設施資料、教育資源內不具備坐標的檔案以爬蟲的方式做空間資訊轉換
    
    2.2 透過縣市界移除轉址錯誤的地方以及過濾特殊交易的標的(如二等親的交易...等)，刪除不需要的欄位


### 3. 資料採礦

    3.1 針對實價登錄資料製做250m，500m，750m的緩衝區，並處理與周遭設施的相互關係
    
    3.2 手動過濾不同縣市間的一些資料差異(如台北市沒有輕軌、基隆市沒有捷運...等)
    
    
### 4. 資料分析

    模型測試標準按照House+ 好時價(https://www.houseplus.tw/faq)所述之規範，通常以平均絕對誤差百分比（MAPE）及命中率（Hit Rate）這兩項作為判定模型好壞的評估指標。
    
    3.1 測試類神經網路、隨機森林以及類神經網路混合隨機森林
    
    3.2 平均絕對誤差百分比- Mean Absolute Percentage Error, MAPE:
        MAPE為大量個案估價之平均誤差值，計算方式為衡量估計值（估值）與評估值（實際成交價）間之差異程度後，取其絕對誤差的平均值，而MAPE數值愈小表示模型估計效果愈精準。一般實務研究上MAPE以小於15%為標準，而house_price_prediction在預測新北市的模型MAPE為9.21%。
    
    3.3 命中率- Hit Rate:
        一般實務研究上，誤差在10%的命中率為50%，而誤差在20%的命中率為80%才符合自動大量估價模型命中率的標準。而house_price_prediction模型在預測新北市命中率誤差10%範圍內達到62.4%水準，誤差20%範圍內達到89.0%水準。

    3.4 因房屋具有異質性，可能因土地使用分區、登記方式、建材、交易樣態等實際情形而產生價格差異，估價結果僅能作為客觀條件下的參考，不代表特定的房屋價格。


