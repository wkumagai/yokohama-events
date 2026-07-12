# 情報源カタログ（2026-07-05 調査）

馬車道・桜木町を中心に、関内・みなとみらい・山下公園・元町・山手・中華街・三溪園・横浜駅周辺までの
イベント情報源を実地調査（全URLをWebFetchで取得確認）した結果。

凡例 — 難易度: ◎=静的HTML+RSS / ○=静的HTML / △=構造に癖あり / ×=JSレンダリング必須 or bot遮断

## Tier 1: 横断アグリゲータ（巡回の柱）

| 情報源 | URL | 形式 | 難易度 | 備考 |
|---|---|---|---|---|
| 横浜市観光情報サイト | https://www.welcome.city.yokohama.jp/eventinfo/ | 静的HTML(PHP) | ○ | 約150件掲載。エリア絞込はPOST(`areacd`: 1=MM21, 3=関内・馬車道・伊勢佐木町, 5=桜木町・野毛, 元町・山手・中華街・山下公園/横浜駅周辺区分あり)。ページ送りはGET `?page=N`(10件/頁)。`?flg=TODAY`あり。詳細は `ev_detail.php?bid=xxx`。robots.txt: `/eventinfo/calendar*.php`, `back.php` がDisallow(一覧は可) |
| ヨコハマ・アートナビ | https://artnavi.yokohama/event/ | 静的HTML(WP) | ○ | 年間約2,000件。エリア別: `/area/minatomirai/`(みなとみらい・桜木町・新港), `/area/kannai/`(関内・馬車道・日本大通り)。検索GET `?keyword=&date=period&period_from=&period_to=`。旧LOD/SPARQL APIは2024年6月終了 |
| みなとみらい21公式 | https://minatomirai21.com/eventcampaign | 静的HTML | ○ | ほぼ毎日更新・約6頁。屋外(汽車道・グランモール・臨港パーク)もカバー。※`/event-cal` はJS必須なので使わない |
| 横浜市 区版イベント検索 | https://cgi.city.yokohama.lg.jp/common/event2/naka/event_list.html (西区は `/nishi/`) | 静的HTML | ○ | **GETパラメータ完備で最も機械取得しやすい**: `?term_after=YYYY-MM-DD&num=20&pos=20`。中区158件/西区57件。公共施設系中心 |
| はまこれ横浜 | https://hamakore.yokohama/eventcal/ | WP+RSS | ◎ | RSS: `https://hamakore.yokohama/feed/`(直近10件)。sitemapあり。商用メディアのため転載範囲は要注意 |
| ヨルノヨ(冬期ハブ) | https://yorunoyo.yokohama/ | HTML | △ | 11〜2月の都心臨海部イルミ54プログラムの横断ハブ。冬期のみ巡回 |

## Tier 2: 施設・団体別（エリア順）

### 馬車道・関内・日本大通り

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| 関内ホール | https://www.kannaihall.jp/event/ | ○ | カード型一覧。料金は詳細ページ |
| 横浜市役所アトリウム | https://www.atrium.city.yokohama.lg.jp/event/ | ○ | 毎月確実に月間カレンダー掲載(`/news/`)。馬車道駅直結 |
| 県立歴史博物館 | https://ch.kanagawa-museum.jp/exhibitions | ○ | **休館中→2026-10-17再開館**。旧パス`/exhibition`は404 |
| BankART Station/KAIKO | https://www.bankart1929.com/info/ | △ | 会期・会場は個別ページ参照が必要 |
| 北仲ブリック&ホワイト | https://kitanaka-brickandwhite.yokohama/news/ | ○ | 北仲マルシェ(毎月第3土日)の詳細はSNS中心 |
| 馬車道商店街 | http://www.bashamichi.or.jp/ | ○ | HTTPS非対応。年次イベント(馬車道まつり)中心、更新低頻度 |
| 横浜BUNTAI | https://yokohama-buntai.jp/event/ | ◎ | RSS: `/feed/`。一部料金も一覧に掲載 |
| 横浜武道館 | https://www.yokohama-budokan.com/event/ | ○ | HTMLテーブル2表。スポーツ大会中心 |
| 横浜スタジアム | https://www.baystars.co.jp/event/ | △ | スタジアム公式`/events/`はJS必須×。ベイスターズ側で代替 |
| KAAT神奈川芸術劇場 | https://www.kaat.jp/calendar | ○ | カレンダー/リスト切替。静的取得できた |
| 開港記念会館 | https://www.kaikokinenkaikan.com/topic | △ | 2024-04再開済。月次「催し物案内」記事のパースが必要 |
| 開港資料館 | https://kaikou.yokohama-history.org/ | ○ | `/exhibition/` `/events/`。旧ドメインは接続不可 |
| ユーラシア文化館・都市発展記念館 | https://eurasia.yokohama-history.org/ | ○ | 同一建物・同財団。yokohama-history.org系はCMS共通 |
| ニュースパーク(新聞博物館) | https://newspark.jp/ | ○ | 企画展 `/exhibition/ex{n}.html` |
| 東京藝大 馬車道校舎 | https://fm.geidai.ac.jp/topics/ | △ | 上映会・修了展など無料公開イベントあり。会場判別に本文解析必要 |
| イセザキ・モール | https://www.isezaki.jp/conts/event.html | ○ | **更新停滞(2022年で停止)**。優先度低、SNS補完前提 |

### 桜木町・野毛・紅葉ケ丘

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| 横浜能楽堂 | https://yokohama-nohgakudou.org/schedule/ | ○ | **2026-06-28再開館**(2024-01〜改修休館)。チケットは `/ticket/` |
| 県立音楽堂 | https://www.kanagawa-ongakudo.com/event/calendar | ○ | 検索型 `/event/search` もあり |
| 県立青少年センター | https://www.pref.kanagawa.jp/docs/ch3/cnt/f602/p7193.html | △ | 紅葉坂ホール等。県庁CMSでURL変更リスク |
| 横浜にぎわい座 | https://nigiwaiza.yafjp.org/perform/ | ◎ | RSS: `/feed/`。落語・演芸 |
| 野毛大道芸 | https://nogedaidogei.com/ | ◎ | RSS明示あり。現行は春のみ開催(第51回=2026/4/18-19) |
| 野毛本通会 | http://www.nogehondoorikai.com/ | △ | サイト更新停滞、一次情報はSNS。ジャズde盆踊り・サンバde花火 |
| 伊勢山皇大神宮 | https://www.iseyama.jp/news/ | ○ | 年間祭典表 `/about/annual_events`(例大祭5/15固定) |
| 成田山横浜別院 | https://yokohamanaritasan.jp/gyouji/ | ○ | 行事は毎年ほぼ固定。年1回取得で足りる |
| 市中央図書館(野毛) | https://www.city.yokohama.lg.jp/kurashi/kyodo-manabi/library/lib-event/ | ○ | 全館横断ページ側が本体 |
| 県立図書館(紅葉ケ丘) | https://www.klnet.pref.kanagawa.jp/yokohama/new-info/event/ | ○ | カテゴリタグ・ページネーションあり |
| コレットマーレ | https://colettemare-yokohama.com/event | ○ | 旧ドメインcolette-mare.comは証明書切れ・使用不可 |

### みなとみらい・新港

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| 横浜美術館 | https://yokohama.art.museum/exhibition/ | ○ | 開催中/予告タブ+年間スケジュール |
| みなとみらいホール | https://yokohama-minatomiraihall.jp/concert/ | ○ | **料金(席種別)まで一覧で取れる唯一級**。`/concert/calendar.html`はJS×
| Kアリーナ横浜 | https://k-arena.com/schedule/ | ◎ | RSS: `/feed/`(ニュース中心)。`/event/`は404 |
| ぴあアリーナMM | https://pia-arena-mm.jp/event/ | ○ | 月別タブ。タイトル+日付のみで情報薄 |
| パシフィコ横浜 | https://www.pacifico.co.jp/eventInfo | × | Nuxt SPA(Studio CMS API)。国立大ホールは2027-05〜2028-03改修休館予定。補完: tenjikai.biz等 |
| 赤レンガ倉庫(広場催事) | https://www.yokohama-akarenga.jp/event/ | ○ | ビール祭・クリスマスマーケット等はここ |
| 赤レンガ1号館(ホール) | https://akarenga.yafjp.org/event | ◎ | RSS: `/feed/`。yafjp系 |
| ランドマークプラザ | https://yokohama-landmark.jp/plaza_news/ | ○ | `/event/`は404 |
| マークイズみなとみらい | https://www.mec-markis.jp/mm/event/ | × | 一覧はJS動的読込 |
| クイーンズスクエア | https://qsy-tqc.jp/event/ | ○ | ステージイベント系 |
| ワールドポーターズ | https://www.yim.co.jp/news | △ | SPA寄りだが本文取得可。`/event/`は404 |
| ハンマーヘッド | https://www.hammerhead.co.jp/eventinfo/ | ○ | `/news/`は無関係デモページ・使用不可 |
| 大さん橋ホール | https://osanbashi.jp/event/ | ○ | 月間カレンダー+カード。数ヶ月先まで充実 |
| 象の鼻テラス | https://zounohana.com/events/ | ○ | 日付・時間・カテゴリ付き |
| みなと博物館・帆船日本丸 | https://www.nippon-maru.or.jp/event/ | ○ | 月間カレンダー併設 |
| カップヌードルミュージアム | https://www.cupnoodles-museum.jp/ja/yokohama/news/ | △ | ニュースにイベント混在、分別必要 |
| 三菱みなとみらい技術館 | https://www.mhi.com/jp/company/overview/museum/minatomirai/news/event.html | ○ | 旧パス404注意 |
| 原鉄道模型博物館 | https://www.hara-mrm.com/event/index.html | ○ | 旧来型静的HTML |
| 京急ミュージアム | https://www.keikyu.co.jp/museum/ | × | **403 bot遮断**。keikyu.co.jpニュースリリースかwelcome.cityで代替 |
| ビルボードライブ横浜 | https://www.billboard-live.com/yokohama/schedules | × | SPA。北仲だがJS必須 |
| はまぎんホール | https://yokohama-viamare.or.jp/event.html | ○ | 掲載点数少 |
| 市民ギャラリー | https://ycag.yafjp.org/ | ○ | `/schedule_exhibition` `/our_exhibition` |
| Music Port YOKOHAMA | https://musicport-yokohama.jp/ | 未確認 | MM音楽イベント特化。構造未調査 |

### 山下公園・中華街・元町・山手

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| (山下公園) | — | — | **公園自体の公式イベントページは存在しない**。welcome.city のエリア絞込(元町・山手・中華街・山下公園)で捕捉。市関与イベントは市記者発表/PR TIMES |
| 横浜市緑の協会 | https://www.hama-midorinokyokai.or.jp/kyokai/event/ | ○ | 横浜公園・山下公園の指定管理側。主催イベントのみ |
| マリンタワー | https://marinetower.yokohama/events/ | ○ | RSSは形骸化(イベントはカスタム投稿で流れない) |
| 氷川丸 | https://hikawamaru.nyk.com/event_list.asp | ○ | クラシックASP。定例ツアー中心 |
| 横浜人形の家 | https://www.doll-museum.jp/exhibition | ◎ | RSS: `/feed/` **活発** |
| 神奈川近代文学館 | https://www.kanabun.or.jp/event/ | ◎ | RSS: `/feed/` **活発**。申込状況まで詳細 |
| 大佛次郎記念館 | https://osaragijiro-museum.jp/event | ◎ | RSS: `/feed` 活発。旧yafjp.orgドメインは証明書不整合・使用不可 |
| 山手西洋館(7館) | https://www.hama-midorinokyokai.or.jp/yamate-seiyoukan/event/ | ○ | 世界のクリスマス(12/1-25)・山手芸術祭(1月下旬〜2月)もここ。`eventcal.php`はJS× |
| アメリカ山公園 | https://www.seibu-la.co.jp/mt_america/event/ | ○ | america-yama.jpはDNS消滅 |
| 元町SS会 | https://www.motomachi.or.jp/event/ | △ | チャーミングセール(2月・9月)。RSSは死んでいる。VIEW MOREはAjaxの可能性 |
| 横浜中華街発展会 | https://www.chinatown.or.jp/event/ | △ | 春節等は年号入り特設URL(`shunsetu2026`等)、一覧から辿る |
| 神奈川県民ホール | https://www.kanagawa-kenminhall.com/event/search | △ | **本館2025-03-31から休館(建替検討)**。掲載は県内他会場が多く対象外イベント混入注意 |

### 三溪園・本牧

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| 三溪園 | https://www.sankeien.or.jp/event/ + `/schedule/` | ○ | **年間スケジュールページが巡回本命**。RSSは存在するがitem空で実用不可。蛍の夕べは2026年見送り。観蓮会7月下旬〜、観月会9月下旬、大茶会10/31-11/1(開園120周年) |

### 横浜駅周辺

| 情報源 | URL | 難易度 | 備考 |
|---|---|---|---|
| アソビル | https://asobuild.com/event/ | ◎ | RSS: `/feed/`。体験型催事の主力 |
| 横浜ポルタ | https://www.yokohamaporta.jp/news/ | ◎ | RSS: `/feed/`。独自催事は少なめ |
| 横浜西口エリアマネジメント | https://yokohamanishiguchi.or.jp/archives/archives-01 | ◎ | RSS: `/feed`。**帷子川カヤック・西口広場系の実質的告知元** |
| YOKOHAMA Station City | https://yokohamastationcity.com/event/ | ○ | 駅アトリウムのジャズLIVE等、駅空間イベント |
| ベイクォーター | https://www.yokohama-bayquarter.com/event/ | ○ | ランタンナイト・毎月マルシェ |
| そごう横浜 | https://www.sogo-seibu.jp/yokohama/topics/ | ○ | 物産展・ビアガーデン等デパ催事の主力 |
| そごう美術館 | https://sogo-museum.jp/exhibitions/current.jsp | ○ | 開催中/次回/予定の構造化一覧 |
| 横浜高島屋 | https://www.takashimaya.co.jp/yokohama/event/index.html | × | **WebFetch/curl接続遮断**。welcome.city等で代替 |
| 相鉄ジョイナス | https://www.sotetsu-joinus.com/news | ○ | `/event/`は404 |
| ニュウマン横浜 | https://www.newoman.jp/yokohama/topics/ | ○ | ARTカテゴリあり |
| CIAL横浜 | https://www.jryscc.co.jp/cial/yokohama/news/ | ○ | 週替わり食物販催事 |
| ルミネ横浜 | https://www.lumine.ne.jp/yokohama/topics/ | ○ | セール中心・優先度低 |
| 横浜モアーズ | https://www.yokohama-mores.jp/eventinfo/ | ○ | 屋上ビアガーデン等 |
| 横浜ビブレ | https://www.vivre-shop.jp/yokohama/news-event/news | △ | リダイレクトの癖 |
| スカイビル | https://www.yokohama-sky.co.jp/information/ | × | **403 WAF**。イベントスペースbyマルイの企画展・はまテラスマーケットはPR TIMES/welcome.cityで代替 |
| ベイシェラトン | https://ybsh.sotetsu-hotels.com/news/ | ○ | ビアフェスタ・ディナーコンサート等パブリック催事あり |
| 日産グローバル本社ギャラリー | https://www.nissan.co.jp/GALLERY/HQ/ | ○ | 車両展示・ファミリー企画が通年 |

## Tier 3: 汎用・補完

| 情報源 | 可否 | 備考 |
|---|---|---|
| connpass | API可 | **2024-09からスクレイピング全面禁止**。公式API v2(要申請・審査、1req/秒)。IT系補完用 |
| Peatix | 実質不可 | 完全JSレンダリング+公開APIなし。対象外とする |
| Walkerplus | 慎重 | 静的HTMLだがrobots.txtで`ClaudeBot Crawl-delay 3`指定。商用転載制限。参照程度 |
| いこーよ | 慎重 | 検索結果URLはDisallow。対象外推奨 |
| 横浜市オープンデータ | 不可 | イベント系データセットは実質なし(CKAN APIはメタデータのみ) |
| PR TIMES(横浜市/スカイビル等) | ○ | bot遮断サイトの代替初報源 |
| マイ広報紙(mykoho.jp) | ○ | 広報よこはま区版のテキスト化再配信。PDFパース回避に有効 |

## 毎年恒例イベント（静的データ化推奨）

サイト巡回より「恒例リスト」として手持ちデータ化し、年1回日付だけ確認する方が確実なもの:

| イベント | 時期 | 一次URL |
|---|---|---|
| 横浜中華街 春節 | 旧正月前後(2026: 2/16-3/3) | chinatown.or.jp(年号入りURL) |
| 元町チャーミングセール | 2月・9月 | motomachi.or.jp |
| ガーデンネックレス横浜 | 3月下旬〜6月 | gardennecklace.city.yokohama.lg.jp |
| 野毛大道芸 | 4月中旬土日 | nogedaidogei.com |
| Live!横浜(旧・音祭り系) | 4月上旬 | liveyokohama.jp |
| ザ よこはまパレード | 5/3固定 | yokohama-cci.com |
| 伊勢山皇大神宮 例大祭 | 5/15固定 | iseyama.jp |
| 横浜開港祭 | 6/1-2固定 | kaikosai.com(JS×→welcome.cityで代替) |
| 横浜ナイトフラワーズ(旧スパークリングトワイライト) | 5〜9月・年約30日 | yokohama-nightflowers.com ※日程変動大・要巡回 |
| 三溪園 早朝観蓮会 | 7月下旬〜8月上旬 | sankeien.or.jp/schedule/ |
| みなとみらい大盆踊り | 8月末金土(2026: 8/28-29) | pacifico.co.jp/event/MM_BonOdori |
| 三溪園 観月会 | 9月下旬 | sankeien.or.jp |
| オクトーバーフェスト | 9月下旬〜10月中旬 | yokohama-akarenga.jp/oktoberfest/ |
| 横浜マラソン | 10月下旬(2026: 10/25) | yokohamamarathon.jp/{年}/ ※年ディレクトリ式 |
| 馬車道まつり | 10/31-11/3固定 | bashamichi.or.jp/event/festival.html |
| ヨコハマミライト | 11月上旬〜2月上旬 | ymm21-illumination.jp ※オフシーズンはサーバー閉鎖 |
| ヨルノヨ | 11月〜2月 | yorunoyo.yokohama |
| クリスマスマーケット(赤レンガ) | 11月下旬〜12/25 | yokohama-akarenga.jp/christmas/ |
| 山手西洋館 世界のクリスマス | 12/1-25 | hama-midorinokyokai.or.jp/yamate-seiyoukan/ |
| アートリンク(赤レンガ) | 11月末〜2月中旬 | akarenga-artrink.yafjp.org |
| 横浜山手芸術祭 | 1月下旬〜2月下旬 | 西洋館サイト内 |
| 横浜トリエンナーレ | 3年周期・第9回=2026年予定(会期未発表) | yokohamatriennale.jp |

## 施設の休廃止・注意メモ（2026-07時点）

- 横浜能楽堂: 2026-06-28 再開館(改修完了)
- 神奈川県立歴史博物館: 休館中 → 2026-10-17 再開館予定
- 神奈川県民ホール本館: 2025-03-31から休館・建替検討中
- パシフィコ国立大ホール: 2027-05-17〜2028-03-31 改修休館予定
- 横浜市開港記念会館: 2024-04 再開済み
- モーション・ブルー・ヨコハマ: 2021年閉店(対象外)
- マルイシティ横浜: 2021年閉店(スカイビルの「イベントスペースbyマルイ」として継続)
- Dance Dance Dance @ YOKOHAMA: 2021年を最後に事実上休止状態
- 横浜音祭り: 2025年開催なし、Live!横浜(毎年型)に実質移行

## スクレイピング方針

- 巡回は1日1回・リクエスト間に2秒以上の待機。User-Agentに連絡先を明記
- 各サイトのrobots.txtを尊重(welcome.cityのcalendar*.php、いこーよの検索URL等)
- 保存するのは タイトル/日時/会場/カテゴリ/元URL のみ。本文・画像は転載しない(リンクで誘導)
- connpassはAPI以外での取得禁止。Peatix・高島屋・スカイビル・京急ミュージアムは直接取得せず代替源(welcome.city/PR TIMES)で補完
- JS必須サイト(パシフィコ・マークイズ・ビルボード等)は第2段階でPlaywright導入時に対応
