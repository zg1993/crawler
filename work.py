# -*- coding: utf-8 -*-

import sys

'''
// 是否通过风控 0未通过 1通过 -1初始状态（用户还未认证）
const IsRiskEnum = {
  INIT: -1,
  PASS: 1,
  NOPASS: 0,
};

const IsRiskDict = {
  [IsRiskEnum.INIT]: "未认证",
  [IsRiskEnum.PASS]: "通过",
  [IsRiskEnum.NOPASS]: "未通过",
};
'''
dd = {
        'annotation': '// 是否通过风控 0未通过 1通过 -1初始状态（用户还未认证）',
        'name': 'IsRisk', 
         'value': [('INIT', -1, '未认证'),('pass', 1, '通过'),('nopass', 0, '未通过')]}

orderTypeDict = {
    'annotation': '// 0首次下单 1二次复购',
        'name': 'placeOrderType', 
         'value': [('first',  '首次下单'),('placeOrder2', '通过'),('nopass', '未通过')]}

orderPayTypeDict = {
        'annotation': '// 0 : 分期订单号  1：全额支付',
        'name': 'payType', 
         'value': [('Installment', 0, '分期订单号'),('full', 1, '全额支付')]}

billTypeDict = {
     'annotation': '// 1:修改账单分期金额 2:延迟账单到期 3:完结账单 4:线下履约',
        'name': 'billApproveType', 
         'value': [('modfiy', '1', '修改账单分期金额'),('delay', '2', '延迟账单到期'),
                   ('end', '3', '完结账单'),('offline', '4', '线下履约')]}

approveStatusDict = {
     'annotation': '''// { name: "全部", id: 0 },
    { name: "待审核", id: 1 },
    { name: "审核拒绝", id: 2 },
    { name: "待签合同", id: 3 },
    { name: "待支付", id: 4 },
    { name: "待发货", id: 5 },
    { name: "待收货", id: 6 },
    { name: "合约中", id: 7 },
    { name: "已取消", id: 8 },''',
        'name': 'OrderStatus', 
         'value': [('approving', 1, '待审核'),('reject', 2, '审核拒绝'),
                   ('signing', 3, '待签合同'),('paying', 4, '待支付'),('sending', 5, '待发货'),
                   ('receiving', 6, '待收货'),('contracting', 7, '合约中'),('canceled', 8, '已取消')
                   ]}


def writeFile():
    pass

def generateJsEnum(d, enumFilePath,autoIndex=False):
    # IsRisk 
    varName = d.get('name')
    varName = varName[0].upper() + varName[1:]
    # d.get('annotation', '')
    arrEnum = []
    arrDict = []
    enumStr = f'const {varName}Enum = {{'
    dictStr = f'const {varName}Dict = {{'
    arrDict.append(dictStr)
    arrEnum.append(enumStr)
    # print(s)
    if(autoIndex):
        for index, (enumName, viewLabel) in enumerate(d.get('value')):
            print(index)
            arrEnum.append(f'{enumName.upper()}: {index},')
            arrDict.append(f'[{varName}Enum.{enumName.upper()}]: "{viewLabel}",')
    else:
        for enumName, enumVal, viewLabel in d.get('value'):
            if  str == type(enumVal):
                enumVal = f'"{enumVal}"'
            arrEnum.append(f'{enumName.upper()}: {enumVal},')
            arrDict.append(f'[{varName}Enum.{enumName.upper()}]: "{viewLabel}",')
            # print(enumName, enumVal, viewLabel)
    arrEnum.append('};')
    arrDict.append('};')
    print('\n'.join(arrEnum))
    print('\n'.join(arrDict))
    content = '\n'.join(['\n'.join(arrEnum), '\n'.join(arrDict), 'export {',f'{varName}Enum,',f'{varName}Dict,\n' ])
    syncFiles(enumFilePath, content)

def syncFiles(enumFilePath, content):
    lines = []
    with open(enumFilePath, 'r+' ,encoding='utf-8') as f:
        # print('ffff', f.readlines())  
        for line in f.readlines():
            # print(line)
            if 'export {' in line:
                replace_content = content
                print(f'replace content: {replace_content}')
                lines.append(replace_content)
            else:
                lines.append(line)
    with open(enumFilePath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    p = r'C:\Users\Administrator\workspace\backend-manage-system\src\const\enum.js'
    # syncFiles(p)
    generateJsEnum(approveStatusDict, p)