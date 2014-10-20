#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import argparse, time,os , sys, datetime, calendar


def get_test(driver, host, outdir):
    
    print "-- 1. Get test start."
    # get リクエスト
    driver.get("http://" + host + "/")
    # text要素の表示を待つ
    try :
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "text"))
        )    
    except TimeoutException as e:
        print "  Response is too late timeout" , e
        return False    

    try :
        driver.find_element_by_id("upload")
        return True;

    except Exception as e:
        print "  No upload Element. It may be v1app." 
        return False    

    finally:
        # 実行後スクリーンショットの保存
        snap=os.path.join(outdir, '1.get_after.png')
        driver.save_screenshot(snap)
        print "  save snap " +  snap


def upload_test(driver, host , text , upfile, outdir):

    print "-- 2. Upload test start"

    # text要素の表示を待つ
    try :
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "text"))
        )

    except TimeoutException as e:
        print "  Response is too late timeout" , type(e)
        return False    

    try :
        # 実行前スクリーンショットの保存
        snap = os.path.join(outdir, '2-1.pre_upload.png')
        driver.save_screenshot(snap)
        print "  save snap " +  snap

        try :
        # 1番目の書き込みの時刻を取得する
            latest=driver.find_element_by_xpath("//td[1]").text
        except NoSuchElementException as e:
            print "It is first writing"
            latest=""

        # フォームへのパラメータの設定とEnterキーの押下
        driver.find_element_by_id("text").send_keys(text)
        driver.find_element_by_id("upload").send_keys(upfile)
        driver.find_element_by_id("text").send_keys(Keys.RETURN);
        
        # img要素の表示待ち(10秒)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "img"))
        )
        
        #表示直後、最上行データを実行前と比較
        if latest is not driver.find_element_by_xpath("//td[1]").text:
            return True
        else:
            print "can't upload files"
            return False

    except TimeoutException as e:
        print "Response is too late timeout" , type(e)
        return False    

    except Exception as e:
        print "Expected TimeoutException but got " + str(e)
        return False

    finally:
        # 実行後スクリーンショットの保存
        snap = os.path.join(outdir, '2-2.after_upload.png')
        driver.save_screenshot(snap)
        print "  save snap " +  snap



def unupload_test(driver, host , text , outdir):

    try :

        print "-- 3. Unupload test start."
        # 実行前スクリーンショットの保存
        snap = os.path.join(outdir, '3-1.pre_unupload.png')
        driver.save_screenshot(snap)
        print "  save snap " +  snap

        # 1番目の書き込みの時刻を取得する
        latest=driver.find_element_by_xpath("//td[1]").text    
    
        # フォームへのパラメータの設定とEnterキーの押下
        driver.find_element_by_id("text").send_keys(text)
        driver.find_element_by_id("text").send_keys(Keys.RETURN);
    

        # 時間が更新されていないことを確認
        if latest != driver.find_element_by_xpath("//td[1]").text:
            print "  NG : The writing was uploaded to the site."
            return False
    
        return True

    except Exception as e:
        print "  Unexpected Exception occurd " , str(e)

    finally :
        # 実行後スクリーンショットの保存
        snap = os.path.join(outdir, '3-2.after_unupload.png')
        driver.save_screenshot(snap)
        print "  save snap " +  snap


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', dest='host'  , action='store', type=str ,help='target host', required=True)
    parser.add_argument('-t', dest='text'  , action='store', type=str ,help='input text' , required=True)
    parser.add_argument('-u', dest='upfile', action='store', type=str ,help='upload file', required=True)
    parser.add_argument('-o', dest='outbase' , action='store', type=str ,help='result file base path' ,required=True)
    parser.add_argument('-n', dest='name'   , action='store', type=str ,help='test name ()' ,default="SampleApp_v2test")
    args = parser.parse_args()

    # 仮想ディスプレイの生成
    display = Display(visible=0, size=(1024, 768))
    display.start()

    # Firefoxの起動
    driver= webdriver.Firefox()

    try:

        # タイムスタンプの取得
        date = datetime.datetime.utcnow()
        timestamp = str(calendar.timegm(date.timetuple()))

        # ファイルの存在チェック
        if not os.path.exists(args.upfile) or not os.path.isfile(args.upfile):
            sys.exit(2)
        else :
            # 絶対パスに修正
            absupfile = os.path.abspath(args.upfile)


        # 出力フォルダが存在しない場合は作成する
        outdir = os.path.join(args.outbase, args.name + "-" + timestamp)
        if not os.path.exists(outdir) :
            os.makedirs(outdir)
            
        # 同名ファイルが存在する場合はエラー
        elif not os.path.isdir(outdir) :
            print "Output dir is exists and not directory."
            sys.exit(2)
            
        continus = True
        
        if get_test(driver, args.host, outdir):
            print "-- 1. OK: Get test is succes."
        else:
            print "-- 1. NG: Get test is failed.  Skip the rest. "
            continus = False
            
        if not continus:
            print "-- 2. Skip: Upload test."
            
        elif upload_test(driver, args.host ,args.text, absupfile, outdir) :
            print "-- 2. OK: Upload test is success."
        else:
            print "-- 2. NG: Upload test is failed. Skip the rest."
            continus = False
            
        if not continus:
            
            print "-- 3. Skip: Unupload test."
        elif unupload_test(driver, args.host ,args.text, outdir):
            print "-- 3. OK: Unupload test is success."
            print "All test completed"
        else:
            print "-- 3. NG: Unupload test is failed."


    finally:
        #driver,displayの停止
        driver.quit()
        display.stop()

