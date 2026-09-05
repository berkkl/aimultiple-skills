# Benchmark push playbook — yeni tablo kurma + veri basma

`benchmark-push` skill'inin kural kitabı. Buradaki her "ZORUNLU" bir kontrol noktasıdır, atlanamaz.
Hepsi ölçüldü, dokümandan alınmadı — kaynak: 2026-09-04'te `b_390` + `b_391` push'u.

Kaynak: Ekrem Sarı'nın `benchmark-push` skill'i (2026-09-04, b_390/b_391 push'larında ölçüldü), AIMultiple
skill setine 2026-09-05'te uyarlandı. Ekrem'in tarafında fazlası var (`registry-ops`: API.md, CHANGELOG.md,
OPEN.md, `push/agentic-rag-v22/` referans push); bir kural buradakiyle çelişirse Ekrem'e sor.

---

## 0. Ön koşullar  (ZORUNLU, her push öncesi)

| | Kontrol | Nasıl |
|---|---|---|
| K1 | API anahtarı var | `AIMULTIPLE_BENCHMARK_API_KEY` env'de (asla dosyaya/chat'e yazma; Berkk session başında verir) |
| K2 | **Anahtarda şema yönetimi yetkisi açık** | sahte slug + `dry_run:true` ile `table/create` yokla |
| K3 | Base URL **sondaki slash olmadan** | `https://research-api.test.v5.aimultiple.com` |
| K4 | Token taze | `GET /benchmark/authorize` |

**K2 nasıl yoklanır** (hiçbir şey yazmaz — var olmayan ama biçimi geçerli bir slug kullan):

```bash
echo '{"benchmark_id":"b_999","dry_run":true,"table":{"comment":"probe",
      "columns":[{"name":"probe_value","type":"int","nullable":true}]}}' \
| curl -s -X POST "$API/benchmark/table/create" -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" -d @-
```

**Doğrulama zinciri (2026-09-04 ölçüldü), sırayla:**
1. `schema management not allowed for this api key` → **DUR**, yetki kapalı. Vedat'tan iste,
   anahtarın kendisini mesaja yapıştırma.
2. `benchmark_id must look like b_379, p_379 or d_379` → biçim hatası. **3–4 haneli** olmalı;
   `b_99999` reddediliyor.
3. `benchmark b_999 not found, register it with /benchmark/create first` → **yetki AÇIK.** Probe amacına
   ulaştı.
4. `table already exists, use /benchmark/table/update to change <slug>_results` → kayıt zaten tablolu;
   `table/create` değil `table/update` gerekiyor.

⚠️ **K3 neden ZORUNLU:** Confluence kılavuzu `$API`'yi sondaki slash'la tanımlıyor. `"$API/benchmark/x"`
çift slash üretir ve **HTTP 404** döner (2026-09-04 ölçüldü). Skill base URL'i normalize etmeli.

---

## 1. Keşif — yazmadan önce  (ZORUNLU)

**Altın kural: kaydın adına göre hüküm verme.** `name` / `description` / `url` birbirinden bağımsız
bozulmuş olabilir; tek güvenilir çıpa prod tablosundaki veri ile canlı makale.

1. **Aynı makaleye kayıt var mı?** — `POST /benchmark/all {"search":"<konu>","status":"all"}`
   (`search` name + slug + responsible + url üzerinde arar).
2. Varsa **ne taşıyor?** — `describe` (şema) + `get` (satırlar). Eski nesil veri mi, boş mu?
3. **Makale canlı mı, başlığı ne?** — `curl -sI https://aimultiple.com/<slug>` 200 dönmeli; başlık için
   sayfanın `<title>`ı okunabilir ama **varsayılan: `page_title`'ı boş bırak**, sunucu makaleden doldurur (R2.4).
4. **Karar:** yeni kayıt mı, mevcut kaydın tablosunu güncellemek mi?
   - `table/create` **yalnız deposu olmayan** kayıtta çalışır. Mevcut tablolu kayıt → `table/update`
     (+ `allow_drop`), ki bu iki nesli tek tabloda karıştırır.
   - **Varsayılan: yeni kayıt.** Eski kayıt tarihsel olarak durur. Bir makaleye birden çok kayıt
     normaldir (`graph-databases`'te 5 tane var).

---

## 2. Kaydı aç — `POST /benchmark/create`

```json
{ "name": "...", "type": "benchmark", "description": "...", "responsible": "Berk Kalelioğlu",
  "urls": [{ "url": "https://aimultiple.com/<slug>", "page_title": "<canlı makale başlığı>" }] }
```

- Zorunlu: `name` + **en az bir geçerli URL**. `urls` bir **obje dizisi**, düz string kabul edilmiyor.
- `type`: `benchmark` | `price` | `data` — varsayılan `benchmark`. Perf/kalite → benchmark,
  fiyat endeksi → price, vendor listesi / market haritası → data.
- **Cevaptaki `benchmark_id` (`b_XXX`) tablo kimliğin.** Not al, sonraki her adım buna bağlı.

### ZORUNLU kurallar
- **R2.1 — Apostrof kullanma.** `name` / `description` / kolon `comment`lerinin hiçbirinde. Sunucu
  `query's` → `query\'s` yazıyor, ters bölü metinde kalıyor. İyelik yapısını yeniden kur.
- **R2.2 — `type`'ı doğru seç, geri dönüşü yok.** Slug önekini belirler, `update` ile değiştirilemez
  ("id and slug can never change"), silme ucu da yok. Yanlışsa kayıt kurtarılamaz, yalnız `status:0`.
- **R2.3 — Slug'ı sen seçemezsin.** Gönderdiğin `benchmark_id` sessizce yok sayılır; sunucu sıradakini
  verir. Var olan bir tabloyu yeni kayda bağlamak API'den mümkün değil.
- **R2.4 — `page_title` = canlı makale başlığı, verbatim** (gerçek `&`, `&amp;` değil). Emin değilsen
  **boş bırak**: sunucu makaleden dolduruyor. Sonradan başlık düzeltmek API'den neredeyse imkânsız.
- **R2.5 — Slug numarası ≠ Houston ID.** `b_384` ↔ row_id 383. `describe`/`get`/`update` hep slug
  numarasını ister; `benchmark_urls` lookup'ı row_id tutar.

---

## 3. Prompt'u TAZE çek  (ZORUNLU)

```bash
curl -s "$API/benchmark/schema-prompt?format=raw" -H "Authorization: Bearer $TOKEN" -o prompt.md
```

**R3.1 — Her yeni tabloda yeniden çek, eski kopyayı kullanma.** İzinli tip listesi ve ilişki
kurulabilecek tablo listesi runtime'da dolduruluyor; eski kopya validator'ın uygulamadığı kural
anlatabilir. Çekilen kopyayı push klasörüne tarihli olarak sakla (kanıt), ama bir dahakine yine çek.

**R3.2 — Prompt ile `/benchmark/shared-tables` çelişirse `shared-tables` doğrudur.** (2026-09-04:
prompt 13 tablo sayıyor, `ai_chat_tools` dahil; `shared-tables` 12 döndürüyor, o yok.)

---

## 4. Şema JSON — sunucunun kurallarının ÜSTÜNE bizim kurallarımız

Sunucunun kuralları prompt'ta (tip allowlist, yasak sistem kolonları, ad kuralları, limitler). Bunlara
ek olarak, AIMultiple tarafında ZORUNLU:

- **R4.1 — Kolon adları SEMANTİK.** Literal `x` / `y` / `value` / `category` / `metric` asla.
  Birim adın içinde: `median_response_ms`, `price_usd_per_hr`, `throughput_tokens_per_sec`.
  Makale kısaltmasını (FRA, EX, FCA) **kolon adına değil `comment`e** yaz.
- **R4.2 — Toplam satırı ile parça satırları aynı kolonda duruyorsa `is_total` (ya da eşdeğeri) koy.**
  `all` + onu bölen bucket'lar aynı tabloda ise `SUM`/`AVG` sessizce iki kat sayar. Comment bir
  `GROUP BY`'ı durdurmaz, kolon durdurur. Ve bölüntü olduğunu **script'te assert et**.
- **R4.3 — Ölçümde eksik kalabilecek her kolon `nullable: true`.** Emin olduğun kolon `false`.
- **R4.4 — Ondalık her yerde `decimal`, asla `float`.** Oran (0–1) için `decimal(6,4)`; işaretli
  olduğunu unutma — negatif olabilen bir metrik (net recovery gibi) buraya sığar.
- **R4.5 — `enum` yerine `varchar`.** `enum`a değer eklemek tablo değişikliği gerektirir.
- **R4.6 — Her ilişki kolonu indeksli.** Ayrıca sık filtreleyeceğin kolonlar (bucket, versiyon).
- **R4.7 — İleriye dönük ayrım kolonlarını şimdi koy.** `set_version` / `run_date` gibi bir sürüm
  ayracı tek değerliyken bile dursun; ikinci nesil veri geldiğinde tabloyu değiştirmek zorunda kalma.
- **R4.8 — Sistem kolonlarını YAZMA:** `id`, `status`, `created_at`, `updated_at`, `deleted_at`,
  `data_version`, `insert_api_key_id`. (OpenAPI 6, prompt 7 sayıyor — **7'sini de yazma.**)
- **R4.9 — Bilimsel şartı taşıyan kolonu düşürme.** Ölçümün geçerliliğini sınırlayan bir koşul varsa
  (harness sürümü, degraded bayrağı, payda farkı) o kolon tabloda durmalı; yoksa sıralama elmayla
  armudu karşılaştırır ve kimse fark etmez.

---

## 5. Tabloyu kur — `POST /benchmark/table/create`

```bash
jq --arg s "b_XXX" '. + {benchmark_id:$s, dry_run:true}' schema.json \
| curl -s -X POST "$API/benchmark/table/create" -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" -d @-
```

- **R5.1 — `dry_run` ZORUNLU ve planı gerçekten OKU.** Kolonlar, tipler, ilişkiler beklediğin gibi mi?
  Kullanıcıya göster, onay al, sonra `dry_run`'ı çıkarıp aynı isteği tekrarla.
- **R5.2 — `benchmark_id` burada ÖNEKLİ slug** (`b_379`). Bir sonraki adımda çıplak numara istenecek;
  karıştırma.
- **R5.3 — Aux tablo varsa slug'ı önceden bil.** İlişkide hedef adı `<slug>_<suffix>` olarak yazılır,
  yani `create`'ten dönen slug'sız şema yazılamaz. Aux tablo yoksa şema slug'dan bağımsızdır.
- **R5.4 — `table/update` kullanıyorsan TAM kolon listesini gönder.** Eksik kolon = silme talebi
  (`allow_drop` ister). **İstisna: `indexes`** — alanı hiç yazmamak "dokunma", `[]` yazmak "hepsini sil".
  Değişiklik saf ekleme değilse tablo `bak_<tablo>_<zaman>` olarak kopyalanır, adı cevapta döner.

---

## 6. Yapıyı doğrula — `POST /benchmark/describe`

```bash
curl -s -X POST "$API/benchmark/describe" -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" -d '{"id":"XXX","type":"benchmark"}'
```

- **R6.1 — Burada ÇIPLAK NUMARA + doğru `type`.** `type` yanlışsa yanlış tabloya bakar ve sessizce
  başka bir kaydın şemasını gösterir.
- **R6.2 — Dönen `table_structure`'ı gönderdiğin şemayla satır satır karşılaştır.** Feed'in yerel
  doğrulaması bu çıktıyı kullanacak.

---

## 7. Veriyi bas — `POST /benchmark/feed`  (geri alınamaz)

**`feed`'in `dry_run`ı YOK. Insert-only: update yok, delete yok. Test DB yok — `test:true` bile
prod'a yazıyor. Sistemin tek geri alınamaz adımı budur.** Bu yüzden kendi merdivenimiz zorunlu:

| | Adım | Neden |
|---|---|---|
| F1 | **Satırları script PARSE etsin** | Elle rakam yazmak yasak. Eksik hücre = anahtarı JSON'dan çıkar (SQL NULL), asla 0 / uydurma / literal `"NULL"` |
| F2 | **Çapraz doğrulama** | İki kaynak aynı büyüklüğü veriyorsa aynı olduklarını assert et, tutmazsa `exit 1` |
| F3 | **Yerel dry-run** | `describe` çıktısına karşı her satır: bilinmeyen kolon, eksik NOT NULL, tip/aralık, decimal basamak taşması, sistem kolonu sızması |
| F4 | **İlişki ön-çözümü** | Her lookup değerini `get` ile hedef tablodan doğrula. **`deleted_at` dolu ve `status != active` satırları ELE** — sunucu onları görmüyor, elemezsen yanlış yeşil alırsın (ölçüldü: `gpt-oss-120b` silinmiş, `GPT OSS 120B` canlı). Eşleşmeyen varsa **push'a başlama** |
| F4b | **Anahtar-imzasına göre grupla** | 🐞 Sunucu toplu INSERT kolon listesini batch'in İLK satırından türetiyor. Anahtar kümesi farklı satırlar aynı batch'te olursa `1136 Column count doesn't match value count`. **Grup başına bir `feed` çağrısı at**, her grup içinde anahtarları sırala |
| F5 | **Yedek** | Push öncesi tablonun mevcut hâlini `get` ile çekip `restore/` altına yaz |
| F6 | **İmza başına 1 kanarya** | Bas → `get` ile geri oku → gönderdiğinle karşılaştır → sonra kalanı. **Kanarya da F4b'ye uymak zorunda**: farklı imzadan iki satırı aynı çağrıya koyarsan kanaryanın kendisi 1136 ile patlar (b_391'de oldu). İmza başına bir satır seçmek hem kuralı korur hem her şekli test eder |
| F7 | **Son doğrulama** | Satır sayısı, `last_insert_at`, ilişkilerin doğru id'ye bağlandığı |

### ZORUNLU kurallar
- **R7.1 — `autoCreateRelation` KAPALI.** Açık bırakırsan bilinmeyen bir ad paylaşılan tabloya
  (`companies`, `ai_models`) `status=2` satır olarak düşer. Eşleşmeyen değer varsa **önce çöz**:
  ya hedef tablodaki mevcut adı kullan, ya Vedat'tan satır iste.
- **R7.2 — Lookup adları benzersiz olmayabilir.** `ai_models.name`'de `llama-4-maverick` ve `glm-4.7`
  üçer satır. İlişkinin hangi id'ye bağlandığını feed sonrası `get` ile doğrula.
- **R7.2b — `feed` ATOMİK.** Hatalı batch'te hiçbir satır yazılmaz (`"no data inserted because of
  errors"`). Yani bir hata aldığında güvenle düzeltip tekrar gönderebilirsin — kısmi yazma yok.
  Bu, `feed`'in tek iyi haberi; yine de başarılı bir insert geri alınamaz.
- **R7.2c — 🐞 Metin alanlarında TIRNAK ve SATIR SONU KULLANMA.** Sunucu `'`, `"` ve `\n`
  karakterlerinin üçünü de kaçırıyor ve ters bölüyü saklanan metinde bırakıyor — naif bir
  `addslashes()` gibi davranıyor. Ölçüldü (2026-09-04, b_392):
  `{"M":64}` → `{\\"M\\":64}` · çok satırlı SQL → her satır sonu literal `\n` dizisine dönüşüyor
  (885 karakterlik sorgu 898 olarak geri geldi, +13 = satır sonu sayısı).
  **Bu `feed` için de `update`in `list_query` alanı için de geçerli.** Yapılandırma değerlerini
  tırnaksız yaz (`M=64, ef_construction=128`); SQL'i **tek satır** gönder. Apostrof gerekiyorsa
  tipografik `’` (U+2019) güvenli. Yazdıktan sonra **geri okuyup birebir karşılaştır**.
- **R7.2d — Markdown'dan parse ediyorsan işaretleri temizle.** `**kalın**` ve `` `kod` `` işaretleri
  ham dosyada var, render edilmiş sayfada yok; temizlemezsen veritabanına backtick girer.
- **R7.3 — `data_version` yanlış veriyi düzeltmenin TEK yolu.** Sildiremezsin; yeni sürümü basıp
  okurken filtrelersin. Baştan bir sürüm politikası belirle (varsayılan 1).
- **R7.4 — Push'u `CHANGELOG.md`'ye yaz:** ne değişti, hangi kanıtla, nasıl geri alınır.

---

## 8. Push sonrası

- `POST /benchmark/urls {"benchmark_id":"b_XXX"}` → URL gerçekten bağlandı mı, başlık doğru mu
- `POST /benchmark/all {"search":"..."}` → kayıt Houston listesinde beklediğin gibi mi
- Makale dinamik tablo kullanacaksa `update` ile `list_query` + `downloadble` set edilebiliyor

---

## 9. ASLA

- `feed`'i "denemek için" kullanma — test DB yok, geri alınamaz
- Şemaya sistem kolonu yazma (7 tanesi)
- `dry_run` planını okumadan gerçek `table/create` atma
- Apostrof kullanma (name / description / comment)
- `benchmark_id`'yi tek anahtar varsayma — benzersiz değil (`b_333` iki kayda atanmış)
- Saklanan URL'i API'den okuduğunla eşit sayma — host normalize ediliyor
- Bir kaydın son URL'ini silmeden önce yenisini eklediğini varsayma — `assign` dedupe eder
- Kaydın adına göre hüküm verme — ad, açıklama ve URL birbirinden bağımsız bozulmuş olabilir
- Elle rakam yazma; eksik hücreye 0 yazma

---

## 10. Ölçülmüş hata mesajları

| Mesaj | Anlamı |
|---|---|
| `schema management not allowed for this api key` | Anahtarda şema yetkisi kapalı (K2) |
| `name is required`, `at least one valid url is required` | `create` payload'ı eksik |
| `invalid benchmark id` | `update`'e slug yerine `id`+`type` gönderilmiş |
| `Table not found` | Kayıt var ama `<slug>_results` hiç yaratılmamış |
| `url is not assigned to this benchmark` | Host normalizasyonu — saklanan hâli `research.` olabilir |
| `nothing to update` | `update` fark görmedi (kısmi patch) |
| HTTP 404 tüm uçlarda | Base URL'de çift slash (K3) |

---

## 11. Adlandırma sözleşmesi  (ZORUNLU — registry'nin okunabilirliği buna bağlı)

Registry'nin bugünkü hâlinin bozuk olmasının sebebi tam olarak bu sözleşmenin olmaması:
`name` / `description` / `url` birbirinden bağımsız bozulmuş 265 kayıt.

### Kayıt alanları
| Alan | Kural | Örnek |
|---|---|---|
| `responsible` | Sabit: **Berk Kalelioğlu** (kendi işinse) | `Berk Kalelioğlu` |
| `url` | **`https://aimultiple.com/<slug>`** — `research.` yok, sondaki slash yok | `https://aimultiple.com/agentic-rag` |
| `page_title` | Canlı makale başlığı **verbatim** (`v_posts.title`, gerçek `&`, `&amp;` değil). Emin değilsen **boş bırak**, sunucu doldurur | `Agentic RAG Benchmark: Multi-Database Routing Across 36 LLMs` |
| `name` | **Kısa konu.** "Top N…", "vs X vs Y", "benchmark results" kuyruklarını at. Aynı makalede birden çok kayıt varsa **ölçümün eksenini ekle** — registry'deki mevcut desen: `<Konu>: <Eksen>` | `Graph Databases: Query Latency Averages` · `Agentic RAG: Multi-Database Routing` |
| `type` | perf/kalite → `benchmark` · fiyat endeksi → `price` · vendor listesi / market haritası → `data`. **Kalıcı, değiştirilemez** | `benchmark` |
| `description` | CSV'den beslenen **2–3 somut cümle**. Ne ölçüldü, kaç birim üzerinde, hangi metrik raporlanıyor. Slop yok, **apostrof yok** | — |

### Tablo tarafı
- **Kolon adı:** snake_case, İngilizce, semantik, **birim adın içinde** (`median_response_ms`,
  `price_usd_per_hr`). Literal `x` / `y` / `value` / `category` / `metric` **yasak**. Makale kısaltması
  (FRA, EX, FCA) kolon adına değil `comment`e.
- **CI kolonları:** `<metrik>_ci_low` / `<metrik>_ci_high`. Support sayısı: `<metrik>_n`.
- **Ayraç kolonları:** sürüm `set_version` / `run_date`, toplam-parça ayrımı `is_total`.
- **İlişki kolonu:** `<tekil>_id` (`company_id`, `ai_model_id`, `gpu_id`).
- **Aux tablo suffix'i:** küçük harf, ≤21 karakter, çoğul (`urls`, `scenarios`, `devices`).
  Tam ad `<slug>_<suffix>` olarak kurulur.
- **Snake-case çakışmasına dikkat:** `ΔHit@1` ve `Hit@1` ikisi de `hit_1` olur. Adları benzersizleştir.

---

## 12. Skill araçları

| Araç | Ne yapar |
|---|---|
| `scripts/api.py` | token, base URL normalizasyonu (K3), **`preflight`** (K1-K4 + şema yetkisi probu), `prompt` / `describe` / `get` / `shared` / `all` / `urls` / ham `post`. Anahtar `$DATABASES/benchmark_cent/.env`ten, mutlak path yok. Sadece stdlib |
| `scripts/validate_rows.py` | **F3 + F4** — canlı `describe` sözleşmesine karşı her satır, ilişki lookup'ları **canlı** satırlara karşı (soft-delete elenir), imza grubu sayımı. Hiçbir şey yazmaz |
| `scripts/feed_ladder.py` | **F4b-F7** — imza gruplama, yedek, imza başına kanarya, geri okuma, grup grup feed, tam hücre doğrulaması. `--apply` olmadan hiçbir şey yazmaz |

### Çağrı

`/benchmark-push` (cwd) veya `/benchmark-push <benchmark-klasörü>`. Skill kullanıcı kapsamındadır
(`skills/aimultiple-benchmark-push/`), yani her klasörden çalışır.

**Skill kendi kendine yeter:** API sözleşmesi her koşuda canlı API'den (`schema-prompt`), anahtar
env'den (`AIMULTIPLE_BENCHMARK_API_KEY`), makale başlığı canlı sayfadan ya da boş bırakılarak sunucudan,
kurallar bu dosyadan gelir. Hiçbiri başka bir proje klasörüne bağımlı değil.

### Veri girdisi — bizim `output/db-ready.csv` ve Orçun'un `benchmark-csv`'si

Girdi CSV değil, **ölçülmüş veridir**. Öncelik sırası:

- **A. Klasörün kendi sonuç dosyaları** (varsayılan yol): `results/` · `data/` · kök `*.csv` / `*.json`.
  Skill kendi extractor'ını yazar (F1/F2 kuralları). `push/agentic-rag-v22/build_rows.py` bunun
  çalışan örneği — o klasörde `output/` yok, veri doğrudan `results/final/`den parse edildi.
- **A2. AIMultiple repolarında `output/db-ready.csv`** (`scripts/build_db_csv.py`, centralization skill'i):
  bizim CSV zaten "provider/model başına tek satır, eksik hücre boş" sözleşmesiyle üretiliyor, yani
  registry tablosunun grain'iyle uyumlu. **Tablo tasarımının başlangıç noktası olarak kullan**, ama
  kolon tiplerini ve nullable'ları prompt + R4 kurallarıyla yeniden karar ver; CSV header'ı şema değildir.
- **B. Orçun'un `/benchmark-csv` çıktısı varsa** (`output/*.csv`, N dosyaya bölünmüş): **keşif kısayolu ve
  çapraz doğrulama kaynağı** olarak kullan. **Tablo tasarımı olarak KULLANMA.** İki çıktının sözleşmesi
  kasten farklı:

  | | `benchmark-csv` (Orçun'un MySQL ingest'i) | registry tablosu |
  |---|---|---|
  | temel kural | **boş cell yok** → column-signature'a göre N dosyaya böler | **eksik hücre = SQL NULL**, nullable kolon normal |
  | satır | entity × `source_type` (aynı entity birden çok satır olabilir) | entity başına tek satır |
  | zorunlu kolonlar | `benchmark`, `source_type`, `run_id` | bunlar registry tablosuna girmez |
  | ilişki | yok, düz metin | paylaşılan tabloya (`ai_models.name` vb.) |

  `output/`u doğrudan feed'e verirsen tek benchmark N kayda bölünür ve entity başına mükerrer satır
  oluşur. **N CSV → kaç registry kaydı** sorusu semantik bir karardır, checkpoint'e girer.
- **C. Hiçbiri yoksa:** dur ve kullanıcıya sor. Veri üretmek bu skill'in işi değil.

`benchmark-csv`'yi bu skill'in içine ALMA — çıktı sözleşmeleri çelişiyor ve o skill'in kendi
extraction mantığı (shape detection, pivot, signature grouping) burada gereksiz. İçeri alınan tek şey
**disiplindir**: parse et/transkribe etme, eksik hücreye 0 yazma, çapraz doğrula (F1/F2).

**Skill'in GARANTİ ETTİĞİ (deterministik):** yetki probu · base URL normalizasyonu · iki id biçiminin
doğru yerde kullanılması · `dry_run` zorunluluğu · sistem kolonu filtresi · tip allowlist doğrulaması ·
apostrof taraması · ilişki ön-çözümü · yedek + kanarya + son doğrulama · `CHANGELOG` kaydı.

**GARANTİ ETMEDİĞİ (semantik, checkpoint gerektirir):** tablonun grain'i (satır neyi temsil ediyor) ·
hangi kolonun neyi ölçtüğü · `is_total` gerekli mi · kaydın `name` / `description` / `type`'ı.
Skill bunları **üretir ve onaylatır**, körlemesine basmaz. Her checkpoint `AskUserQuestion`.


## Referans uygulama

`push/agentic-rag-v22/` — 36 modelli v2.2 paneli, iki ayrı kayda (routing + text-to-SQL) bölünmüş.
`build_rows.py` F1/F2'yi gösteriyor: parse eder, bracket ile `results_long`u karşılaştırır, bucket'ların
bölüntü olduğunu assert eder, geçmezse `exit 1`. `README.md` o push'un durumunu ve kararlarını tutuyor.
