// Tests for preview-only-portfolio-import.js(2026-10-21). Run: node --test pipeline/portfolio/test_portfolio_import.mjs
// 가짜 티커·금액만 쓴다(공개 저장소). 실제 Robinhood 내역으로 10-19 계산과 같은지는 저장소 밖에서 맞춰 봤다.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseCSV, importTable } from '../../preview-only-portfolio-import.js';

const RH_HEAD = '"Activity Date","Process Date","Settle Date","Instrument","Description","Trans Code","Quantity","Price","Amount"';
const rh = (...lines) => [RH_HEAD, ...lines].join('\n');
const L = (d, sym, desc, code, q, price, amt) => `"${d}","${d}","${d}","${sym}","${desc}","${code}","${q}","${price}","${amt}"`;

test('parseCSV: 따옴표 안 쉼표·줄바꿈·"", BOM, 빈 줄', () => {
  const rows = parseCSV('﻿a,b,c\r\n"x, y","line1\nline2","say ""hi"""\n\n1,2,3\n');
  assert.deepEqual(rows, [['a', 'b', 'c'], ['x, y', 'line1\nline2', 'say "hi"'], ['1', '2', '3']]);
});

test('Robinhood: 매수·매도(평균 원가)·역분할·배당·원천징수·입금·이자, 최신이 위인 파일, 잔량 버림', () => {
  const csv = rh(
    L('3/2/2026', 'BBB', 'Bee Corp\nCUSIP: 1', 'Sell', '0.00005', '$10.00', '$0.00'),   // 잔량만 남김
    L('3/1/2026', 'AAA', 'Aye Inc', 'CDIV', '', '', '$1.50'),
    L('3/1/2026', 'AAA', 'Aye Inc', 'NRAT', '', '', '($0.45)'),
    L('2/1/2026', 'CCC', ' | CUSIP: 9', 'SPR', '10', '', ''),                          // 역분할: 40주 → 10주
    L('2/1/2026', 'CCC', 'Sea ETF', 'SPR', '40S', '', ''),
    L('1/20/2026', 'AAA', 'Aye Inc', 'Sell', '5', '$30.00', '$150.00'),
    L('1/15/2026', 'AAA', 'Aye Inc', 'Buy', '10', '$25.00', '($250.00)'),
    L('1/10/2026', 'AAA', 'Aye Inc', 'Buy', '10', '$20.00', '($200.00)'),
    L('1/10/2026', 'CCC', 'Sea ETF', 'Buy', '40', '$5.00', '($200.00)'),
    L('1/10/2026', 'BBB', 'Bee Corp', 'Buy', '0.0001', '$10.00', '($0.00)'),
    L('1/5/2026', '', 'Brokerage-held Cash Interest Payment', 'INT', '', '', '$0.16'),
    L('1/2/2026', '', 'ACH Deposit', 'ACH', '', '', '$1,000.00'),
    '"","","","","","","","",""',
    '"","","","","","","","","","The data provided is for informational purposes only."',
  );
  const r = importTable(parseCSV(csv));
  assert.equal(r.kind, 'robinhood');
  assert.deepEqual(r.warnings, []);
  const rows = Object.fromEntries(r.holdings.rows.map((x) => [x.ticker, x]));
  assert.equal(rows.AAA.qty, 15);
  assert.equal(rows.AAA.avgPrice, 22.5);          // 20주 평균 22.5, 5주 팔아도 평균 그대로
  assert.equal(rows.AAA.name, 'Aye Inc');
  assert.equal(rows.CCC.qty, 10);
  assert.equal(rows.CCC.avgPrice, 20);            // 원가 200 그대로, 수량 10
  assert.equal(rows.BBB, undefined);               // 0.00005주 잔량은 버림
  assert.equal(rows[''].avgPrice, 1000 + 0.16 - 200 - 200 - 250 + 150 + 1.5 - 0.45);
  assert.equal(r.holdings.asOf, '2026-03-02 거래까지');
  assert.match(r.holdings.note, /2026-01-02~2026-03-02/);
  assert.match(r.holdings.note, /BBB/);
  assert.equal(r.holdings.rows.at(-1).ticker, '');   // 현금 줄은 맨 끝
});

test('Robinhood: 보유보다 많이 판 기록·수량 있는 모르는 코드는 경고, 깨진 금액은 오류', () => {
  const r = importTable(parseCSV(rh(
    L('1/3/2026', 'AAA', 'Aye', 'ACATI', '5', '', ''),
    L('1/2/2026', 'AAA', 'Aye', 'Sell', '3', '$10.00', '$30.00'),
    L('1/1/2026', 'AAA', 'Aye', 'Buy', '1', '$10.00', '($10.00)'),
  )));
  assert.equal(r.warnings.length, 2);
  assert.match(r.warnings[0], /많이 판/);
  assert.match(r.warnings[1], /ACATI 1건/);
  assert.throws(() => importTable(parseCSV(rh(L('1/1/2026', '', 'x', 'ACH', '', '', '$abc')))), /금액/);
  assert.throws(() => importTable(parseCSV(rh('"","","","","","","","",""'))), /날짜/);
});

test('보유 표: 한글·영문 머리, 현금 줄, 통화, 중복·빈 평균 단가 경고, 필수 열 없으면 오류', () => {
  const r = importTable(parseCSV('종목명,티커,수량,평균 단가,통화\n에이,aaa,"1,000",12.345,usd\n비,BBB,2,,\n,CASH,500.5,,\n에이2,AAA,1,10,USD\n'));
  assert.equal(r.kind, 'table');
  assert.deepEqual(r.holdings.rows.map((x) => [x.ticker, x.qty, x.avgPrice, x.currency]),
    [['AAA', 1000, 12.35, 'USD'], ['BBB', 2, null, 'USD'], ['AAA', 1, 10, 'USD'], ['', 1, 500.5, 'USD']]);
  assert.equal(r.holdings.asOf, null);
  assert.equal(r.warnings.length, 2);
  const e = importTable(parseCSV('Symbol,Shares,Average Cost\nAAA,3,9.5\n'));
  assert.deepEqual(e.holdings.rows.map((x) => [x.ticker, x.qty, x.avgPrice]), [['AAA', 3, 9.5]]);
  assert.match(e.warnings[0], /현금/);
  assert.throws(() => importTable(parseCSV('이름,가격\na,1\n')), /티커와 수량/);
  assert.throws(() => importTable(parseCSV('Ticker,Qty\n1AB,3\n')), /티커/);
  assert.throws(() => importTable(parseCSV('Ticker,Qty\nAAA,0\n')), /수량/);
});
