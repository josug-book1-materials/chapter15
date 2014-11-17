import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class SampleAppGet extends Simulation {
  //プログラム実行のためのパラメータ
  // リクエストのターゲットURL
  val targetUrl = System.getProperty("url") 
  require(targetUrl != null)
  // 繰り返し回数
  val repeatCount: Int = Integer.getInteger("repeat", 1)
  // 同時実行ユーザ数
  val userCount: Int = Integer.getInteger("user", 1)
  // 同時実行ユーザの起動時間
  val duration: Int = Integer.getInteger("duration", 0)  
  // シナリオ名(条件を付加)
  val name = System.getProperty("name", "")
  val scname = s"${name}Get_u${userCount}_r${repeatCount}_s${duration}"

  //(a) httpプロトコル定義
  val httpConf = http
    .baseURL(targetUrl)                  // リクエストURLと基本ヘッダの指定
    .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    .acceptEncodingHeader("gzip,deflate,sdch")
    .acceptLanguageHeader("ja,en-US;q=0.8,en;q=0.6")
    .userAgentHeader("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36")
    
  //(b) 付加 header 定義
  val headers_0 = Map("Cache-Control" -> "max-age=0")

  //(c) 実行シナリオ
  val scn = scenario(scname)
    .exitBlockOnFail{                   // エラーハンドリング
      repeat(repeatCount , "n"){        // ループ条件
        exec(                           // テスト実行
          http("request_get_${n}")      // HTTPリクエスト動作定義
            .get("")                    // Getメソッド呼び出し(パス)
            .headers(headers_0)         // HTTPオプション
          ) 
      }
  }

  //(d) 実行条件
  setUp(scn.inject(
    rampUsers(userCount) over (duration seconds)  //テスト実行条件
  )).protocols(httpConf)

}
