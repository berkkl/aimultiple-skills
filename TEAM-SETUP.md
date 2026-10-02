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

`~/aimultiple-work/CLAUDE.md` dosyasını oluştur, şablon:

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

Bütün ekip tek projede çalışıyor: **RES "AIM Researcher"**. Kartlar `RES-1, RES-2...` diye gider. Board "AIM Researcher" her ISO haftası için bir sprint tutar (`2026-W41`). Yeni kart güncel sprinte kendiliğinden düşer. Board'da her kişi ayrı satırda görünür.

Kendi projeni veya board'unu açma. Hesabın proje ekibinde değilse Berkk'e yaz.

Kart yazım kuralı, güncelleme sıklığı ve mühendis saati: `skills/aimultiple-youtrack-tasks/SKILL.md`. Kartlarda kişi adı, mention veya sohbet alıntısı yer almaz.

## 4. YouTrack MCP

Claude'un YouTrack'e erişimi MCP ile:

1. Token al: YouTrack -> profil -> Account Security -> New token (kalıcı token, `perm:` ile başlar). Tokenı kimseyle paylaşma, chat'e yapıştırma; Claude'a "MCP konfigürasyonuna ekle" de ve değeri kendin gir.
2. MCP'yi ekle (Berkk'in kullandığı düzen YouTrack'in kendi MCP sunucusu):

```bash
claude mcp add --transport http youtrack https://aimresearcher.youtrack.cloud/mcp --header "Authorization: Bearer <TOKEN>"
```

3. YouTrack profilinde saat dilimini ayarla: Profil > General > Time zone: **Europe/Istanbul**. "Etc/GMT+3" seçme, o UTC-3 demek; mühendis saati kayıtları bir gün önceye kayar.
4. Test: yeni bir Claude session'ında "YouTrack'te projemdeki açık kartları listele" de. `search_issues` çalışıyorsa tamam. Çalışmıyorsa Berkk'e sor, kurulumu birlikte yaparsınız.

## 5. Skill uyarlamaları (tek seferlik)

Proje kodu herkes için RES, değiştirme. Tek uyarlama: `aimultiple-session-pm/SKILL.md` içindeki "Gelen kutusu" (INBOX) adımını ve "Triaging an INBOX card" bölümünü sil. Bu bölüm Berkk'in form intake'ine özel. Pazartesi sprint adımı (`new_sprint.py`) da board sahibine özel, sende atlanır.

## 6. Doğrulama

Sırayla test et, üçü de geçmeden kuruluma bitti deme:

1. **Handoff:** Claude'a küçük bir iş yaptır, `/save-handoff deneme` de; `handoffs/deneme.md` oluşmalı. Yeni session aç, `/load-handoff deneme` ile kaldığın yerden devam edebilmeli.
2. **YouTrack:** Claude'a RES'te kendine bir iş kartı açtır (gerçek bir iş seç, deneme kartı açma). Kart güncel sprintte, senin satırında görünmeli. Session sonunda kartta bir güncelleme yorumu ve bir mühendis saati kaydı olmalı.
3. **PM:** `weekly-plan/` altına Claude'la birlikte bu haftanın dosyasını kur (skill'deki tablo formatı: iş | kart | hedef gün | durum | kalan). Yeni session aç; Claude checkin çıktısıyla açılmalı: hangi karta çalışıyorsun, haftada kaç iş bitti, ne duruyor.

## 7. Çalışma düzeni

- Hafta başı: haftalık iş listeni weekly-plan dosyasına döktür, her satırı bir karta bağla.
- Her session: checkin ile başla, checkout ile bitir. Checkout kart yorumunu (Yapılan / Sıradaki / Engel) ve mühendis saati kaydını yazar.
- Kart kapanınca kapanış yorumu toplam mühendis saatini ve kanıt linkini verir.
- Uzun projelerde context %50'yi geçmeden handoff yaz; devam eden işin hafızası handoff dosyasıdır, chat geçmişi değil.
- Cuma: haftalık özetini weekly-plan dosyasından ürettir (düz bullet, tek satır, birinci tekil).

Takıldığın adımda Berkk'e yaz; kurulum toplamda 30-45 dakika.
