import pandas as pd

def getcats(production):
    '''
    Get a dictionary containing all the references used
    by FAOSTAT
    '''
    #production = pd.read_csv(__loc__+'Crops.csv')
    class codes:pass

    codes.area = production[['Area Code','Area']].groupby('Area Code').first().sort_values('Area Code')['Area'].to_dict()
    codes.areacode = dict(zip(codes.area.values(),codes.area.keys()))

    codes.item = production[['Item Code','Item']].groupby('Item Code').first().sort_values('Item Code')['Item'].to_dict()
    codes.itemcode = dict(zip(codes.item.values(),codes.item.keys()))

    return codes
    #json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)
