# Adlandırma sözleşmesi

`benchmark-push` için ZORUNLU. Registry'nin bugünkü hâlinin bozuk olmasının sebebi tam
olarak bu sözleşmenin olmaması: `name` / `description` / `url` birbirinden bağımsız
bozulmuş 265 kayıt. Kural kitabının tamamı: `playbook.md`.

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
