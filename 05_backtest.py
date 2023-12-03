import pybithumb
import numpy as np
import openpyxl
import datetime


k = 0.5
coinName = "BTC"
checkDayPeriod = 30 # K값을 구하기 위한 일자별 기록 구간
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=checkDayPeriod)
start_price = 500000

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
# df = pybithumb.get_ohlc(coinName)

# all_data = pybithumb.get_ohlcv(coinName, interval="hour12")
all_data = pybithumb.get_ohlcv(coinName, interval="day")
df = all_data.loc[start_date:end_date].copy()


# 변동폭 * k 계산, (고가-저가) * k값
df['range'] = (df['high'] - df['low']) * k
# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# # target의 1% 수익
# df['target_1%'] = df['target'] + df['target']*0.01
# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

# df['ror_1%'] = np.where(df['high'] > df['target'],
#                      df['target_1%'] / df['target'],
#                      1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()
# df['hpr_1%'] = df['ror_1%'].cumprod()

# Draw Down 계산(누적 최대 값과 현재 hpr 차이 / 누적 최대값 *100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['dd'].max())

# 자산 계산
df['자산보유금액'] = df['hpr'] * start_price

# 엑셀로 출력
df.to_excel("bithumb.xlsx")

# 엑셀파일 쓰기
write_wb = openpyxl.load_workbook('bithumb.xlsx')

# Sheet1에 입력

# k_str = str(k)
day_str = str(checkDayPeriod)

# write_ws = write_wb.active
# write_ws['A1'] = stock
# write_ws['M1'] = "K값" + k_str
# write_ws['N1'] = day_str + "일"
# write_ws['B1'] = 'open(시가)'
# write_ws['C1'] = 'high(고가)'
# write_ws['D1'] = 'low(저가)'
# write_ws['E1'] = 'close(종가)'
# write_ws['F1'] = 'volume(거래량)'
# write_ws['G1'] = 'value(??)'
# write_ws['H1'] = 'range(변동폭*k)'
# write_ws['I1'] = 'target(매수가)'
# write_ws['J1'] = 'ror(수익률)'
# write_ws['K1'] = 'hpr(누적 수익률)'
# write_ws['L1'] = 'dd(낙폭)'

# # 엑셀 저장
# tday = datetime.today()
# tday_s = tday.strftime('%b_%d')
filename = coinName+"_"+day_str+""'_thumb.xlsx'
write_wb.save(filename)


