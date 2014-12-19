#!/usr/bin/python
# -*- coding: utf-8 -*-

#(a)必要ライブラリのインポート
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#(b)実行環境の起動
# 仮想GUI環境の起動
display = Display(visible=0, size=(1024, 768))
display.start()
# Firefox の起動
driver= webdriver.Firefox()

#(c)リクエストの送信
# get リクエスト
driver.get("http://192.168.0.99/")
#(d)text 要素の表示待ち
WebDriverWait(driver, 10).until(
expected_conditions.visibility_of_element_located((By.ID, "text"))
)

#(e)text要素の操作
# text 要素への文字列入力
driver.find_element_by_id("text").send_keys("example")
# text 要素にフォーカスした状態でリターンキー押下
driver.find_element_by_id("text").send_keys(Keys.RETURN)

#(f)ブラウザーのスナップショットの保存
driver.save_screenshot("/root/snapshot.png")

#(g)仮想GUI環境のクローズ
# Firefoxのクローズ
driver.close()
# 仮想GUI 環境の停止
display.stop()

