# AIMultiple Skill Kurulumu (Ekip)

Bu doküman, Berkk'in kullandığı handoff + YouTrack + Session PM düzenini kendi Claude Code kurulumunda çalıştırmak için. Adımları sırayla, kendi Claude'unla birlikte uygula: bu dosyayı Claude'a ver ve "adım adım kuralım" de; komutları o koşar, hesap gerektiren yerlerde sana sorar.

Ön koşullar: Claude Code kurulu; bu repoya GitHub erişimin var; aimresearcher.youtrack.cloud hesabın var (yoksa Berkk davet eder).

## 1. Çalışma klasörü ve skill'ler

Bir çalışma klasörü seç (ör. `~/aimultiple-work`) ve iskeletini kur:

```bash
mkdir -p ~/aimultiple-work/{skills,handoffs,weekly-plan,drafts}
git clone https://github.com/berkkl/aimultiple-skills.git ~/aimultiple-skills
cp -r ~/aimultiple-skills/skills/* ~/aimultiple-work/skills/
```

Bu kurulum sana zip olarak geldiyse: zip'teki `skills/` klasörünü `~/aimultiple-work/skills/` içine kopyalaman yeterli, clone şart değil; repo erişimi güncellemeler için lazım olur. Güncelleme almak istediğinde: `cd ~/aimultiple-skills && git pull` ve kopyayı yenile. Kendi skill değişikliklerin varsa PR aç, herkese dağılsın.

## 2. CLAUDE.md

`~/aimultiple-work/CLAUDE.md` dosyasını oluştur, şablon (KENDİ proje kodunu yaz, aşağıda `XXX` gördüğün her yer):

```markdown
# AIMultiple Çalışma Alanı

Çalışmaya başlamadan bu dosyayı oku, ilgili skill'i skills/ altından yükle.

## Always-On

### Context Window Handoff (her session)
Uzun işlerde context dolmadan handoff yaz: skills/aimultiple-context-handoff/SKILL.md.
Komutlar: /save-handoff <ad>, /load-handoff [ad], /list-handoffs. Dosyalar handoffs/ altında.

### Session PM (her session, hafif)
Session başında weekly-plan/ altındaki güncel hafta dosyasına bak. İş oradaki bir
satıra bağlıysa skills/aimultiple-session-pm/SKILL.md checkin prosedürünü koş
(hangi kart, haftalık sayaç, duran işler, tek cümle öneri; 10 satırı geçme).
Session sonunda dokunulan satırları checkout ile güncelle. Plan dosyası yoksa
bunu tek satırla söyle, sessizce atlama.
NOT: Skill'deki YouTrack sorgularında proje kodu olarak XXX kullan (AIM değil).
Skill'deki INBOX/Gelen İşler bölümü Berkk'in intake sistemine özel, ATLA.

## Skill yönlendirmesi
- YouTrack kartı açma/güncelleme: skills/aimultiple-youtrack-tasks/SKILL.md
- Haftalık PM: skills/aimultiple-session-pm/SKILL.md
- Handoff: skills/aimultiple-context-handoff/SKILL.md
- Yazı editi (OLD/NEW): skills/aimultiple-article-edit/SKILL.md
- Yazım kuralları: skills/aimultiple-anti-slop-writing/SKILL.md
```

Diğer skill'leri (fact-check, benchmark zinciri vb.) ihtiyacın oldukça aynı listeye ekle; hepsinin ne yaptığı repo README'sinde.

## 3. YouTrack projesi ve board

Ortak instance kullanıyoruz ama herkes kendi projesinde çalışıyor:

1. Berkk'ten kendi projeni iste (proje kodu = baş harflerin, ör. `SVL`). Kartların `SVL-1, SVL-2...` diye gider; Berkk'in AIM kartlarıyla karışmaz ama gerektiğinde birbirimizin kartına link verebiliriz.
2. Kendi agile board'unu aç: Agile Boards -> New board, projen seçili.
3. Board ayarında otomatik ekleme aç: Board Settings -> General -> Sprints altında "Automatically add new issues" seçeneğini işaretle (ya da sprint kullanmayacaksan sprint'leri kapat; sprint'siz board query eşleşmesiyle her kartı kendiliğinden gösterir). Bunu yapmazsan her kartı elle board'a taşımak zorunda kalırsın.

## 4. YouTrack MCP

Claude'un YouTrack'e erişimi MCP ile:

1. Token al: YouTrack -> profil -> Account Security -> New token (kalıcı token, `perm:` ile başlar). Tokenı kimseyle paylaşma, chat'e yapıştırma; Claude'a "MCP konfigürasyonuna ekle" de ve değeri kendin gir.
2. MCP'yi ekle (Berkk'in kullandığı düzen YouTrack'in kendi MCP sunucusu):

```bash
claude mcp add --transport http youtrack https://aimresearcher.youtrack.cloud/mcp --header "Authorization: Bearer <TOKEN>"
```

3. Test: yeni bir Claude session'ında "YouTrack'te projemdeki açık kartları listele" de. `search_issues` çalışıyorsa tamam. Çalışmıyorsa Berkk'e sor, kurulumu birlikte yaparsınız.

## 5. Skill uyarlamaları (tek seferlik)

Kendi kopyanda (`~/aimultiple-work/skills/`) iki küçük değişiklik:

1. `aimultiple-session-pm/SKILL.md`: sorgulardaki `project: AIM` ifadelerini kendi proje kodunla değiştir; "Gelen kutusu" (INBOX) adımını ve "Triaging an INBOX card" bölümünü sil (Berkk'in form intake'i, sende yok).
2. `aimultiple-youtrack-tasks/SKILL.md`: varsa AIM proje referanslarını kendi kodunla değiştir.

Claude'a "bu iki dosyada AIM'i XXX yap, INBOX bölümlerini çıkar" demen yeterli.

## 6. Doğrulama

Sırayla test et, üçü de geçmeden kuruluma bitti deme:

1. **Handoff:** Claude'a küçük bir iş yaptır, `/save-handoff deneme` de; `handoffs/deneme.md` oluşmalı. Yeni session aç, `/load-handoff deneme` ile kaldığın yerden devam edebilmeli.
2. **YouTrack:** Claude'a "kendime deneme kartı aç" de; kartın board'da otomatik göründüğünü kontrol et, sonra kartı kapattır.
3. **PM:** `weekly-plan/` altına Claude'la birlikte bu haftanın dosyasını kur (skill'deki tablo formatı: iş | kart | hedef gün | durum | kalan). Yeni session aç; Claude checkin çıktısıyla açılmalı: hangi karta çalışıyorsun, haftada kaç iş bitti, ne duruyor.

## 7. Çalışma düzeni

- Hafta başı: haftalık iş listeni weekly-plan dosyasına döktür, her satırı bir karta bağla.
- Her session: checkin ile başla, checkout ile bitir; kart yorumu formatı "Yapılan / Sıradaki / Blocker".
- Uzun projelerde context %50'yi geçmeden handoff yaz; devam eden işin hafızası handoff dosyasıdır, chat geçmişi değil.
- Cuma: haftalık özetini weekly-plan dosyasından ürettir (düz bullet, tek satır, birinci tekil).

Takıldığın adımda Berkk'e yaz; kurulum toplamda 30-45 dakika.
