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
orderPayTypeList = [
    {
        'annotation': '// 运营商类型 1 电信 2 联通 3 移动 4 其它运营商',
        'name': 'operatorType', 
         'value': [('ct', 1, '电信'),('cu', 2, '联通'),('cm', 3, '移动'),('other', 4, '其它运营商')]}
    # {
    #     'annotation': '// 运营商认证结果 1一致 2不一致 3未找到',
    #     'name': 'operatorResult', 
    #      'value': [('consistent', 1, '一致'),('inconsistent', 2, '不一致'),('notFound', 3, '未找到')]}
#     {
# 'annotation': '//orderContractType 合同选择状态 默认1 爱签  2赋强黄金公证 3永川公证',
#         'name': 'ContractType', 
#          'value': [('AiQian', 1,'爱签'),('FuQiang',2, '赋强黄金公证'),('YongChuan',3, '永川公证' )
#                    ]
#     },
#     {
# 'annotation': '//ExamineStatus 审核状态 1 未分配  2 已分配',
#         'name': 'ExamineStatus', 
#          'value': [('UnAssign', 1,'未分配'),('Assigned',2, '已分配') 
#                    ]
#     },
#     {
# 'annotation': '//ExamineResult 审核结果 1 未审核  2 已审核',
#         'name': 'ExamineResult', 
#          'value': [('UnExamine', 1,'未审核'),('examined',2, '已审核') 
#                    ]
#     },
#     {
# 'annotation': '//app APP ;  web app的H5 "wechat", //微信浏览器 "mobile", // 移动端本地浏览器 "desktop", // 桌面浏览器',
#         'name': 'DeviceType', 
#          'value': [('web', 'web','APP-H5'),('app','app', 'APP'),('wechat','wechat', '微信' )
#                    ,('mobile','mobile', '移动端'),('desktop', 'desktop','桌面'),]
#     },
#     {
# 'annotation': '// 风控等级 1 S+ 2 S 999 拒绝',
#         'name': 'risklevel', 
#          'value': [('SS', 1, 'S+'),('S', 2, 'S'),('A', 3, 'A'),('B', 4, 'B'),('C', 5, 'C'),('reject', 999, '拒绝')]
#     },
#     {
# 'annotation': '// 风险等级 1 命中 0 未命中 -1 未认证',
#         'name': 'riskText', 
#           'value': [('SS', 1, '极低风险'),('S', 2, '低风险'),('A', 3, '正常风险'),('B', 4, '高风险'),('C', 5, '极高风险'),('reject', 999, '拒绝')]
#     },
#     {
# 'annotation': '//  1 命中 0 未命中 -1 未认证',
#         'name': 'shelves', 
#          'value': [('miss', 1, '销售中'),('hit', 2, '仓库中'),('unauth', -1, '草稿')]
#     },
#     {
# 'annotation': '//  1 命中 0 未命中 -1 未认证',
#         'name': 'industryBlacklist', 
#          'value': [('miss', 0, '未命中'),('hit', 1, '命中'),('unauth', -1, '未认证')]
#     },
    
#     {
# 'annotation': '// isTrack  跟踪状态 0 未跟进 1 已跟进',
#         'name': 'trackStatus', 
#          'value': [('unTrack', 0, '未跟进'),('tracked', 1, '已跟进')]
#     }
]

orderPayTypeDict = [
    { 'annotation': '// 商品的状态 销售中 仓库中 草稿',
        'name': 'goodsStatus', 
         'value': [('sale', 1, '销售中'),('storage', 2, '仓库中'),('manuscript', 3, '草稿')]},
    
    { 'annotation': '// 渠道状态 1 启用 2 停用',
        'name': 'channelStatus', 
         'value': [('active', 1, '启用'),('deactive', 2, '停用')]},
         ]

orderPayTypeDict6 = {
    'annotation': '// IOS :  1 ANDROID :  2 H5 :  3 微信小程序 :  4支付宝小程序 :  5',
        'name': 'supportPlatformType', 
         'value': [('IOS', 1, 'IOS'),('ANDROID', 2, 'ANDROID'),('H5', 3, 'H5'),('wechat', 4, '微信小程序'),('aliapy', 5, '支付宝小程序')]}

orderPayTypeDict5 = {
        'annotation': '//捷券发放状态：recharge:处理中; success:处理成功；fail:失败',
        'name': 'couponProcessStatus', 
         'value': [('recharge', 'recharge', '处理中'),('success', 'success', '处理成功'),('fail', 'fail', '失败')]}


orderPayTypeDict4 = {
        'annotation': '//couponStatus 捷券状态    1上架、0下架',
        'name': 'couponStatus', 
         'value': [('up', 1, '上架'),('down', 0, '下架')]}

orderPayTypeDict3 = {
        'annotation': '//couponType 捷券类型    商品类型 1、直充 2、卡密 3、话费',
        'name': 'couponType', 
         'value': [('direct', 1, '直充'),('card', 2, '卡密'),('phone', 3, '话费')]}

orderPayTypeDict2 = {
        'annotation': '//payState 流水支付状态   1 : 支付中 2：支付成功 3：支付失败 （条件赛选）UN_PAY(0,"未支付"),PAY_PROGRESSING(1,"支付中"),PAY_SUCCESS(2,"支付成功"),PAY_FAIL(3,"支付失败")',
        'name': 'payStatus', 
         'value': [('unpay', 0, '未支付'),('paying', 1, '支付中'),('payed', 2, '支付成功'),('payFail', 3, '支付失败')]}

orderPayTypeDict1 = {
        'annotation': '//payChannelModel 支付方式   0 芝麻免押 1 汇付宝',
        'name': 'payChannelModel', 
         'value': [('sesame', 0, '芝麻免押'),('hfb', 1, '汇付宝')]}

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
        # print('---d', d.get('value') )
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
    if(isinstance(orderPayTypeList, list)):
        for item in orderPayTypeList:
            generateJsEnum(item, p)
    else:
        generateJsEnum(orderPayTypeList, p)