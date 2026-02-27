# Zimbra to Stalwart MVP Migration Platform - Kurulum Rehberi

Bu proje, bir belediyenin veya kurumun Zimbra mail altyapısından Stalwart mail sunucusuna kullanıcı bazlı geçişini (migration) sağlamak amacıyla geliştirilmiş "Enterprise-Grade" (kurumsal seviye) bir MVP (Minimum Viable Product) uygulamasıdır.

## 🌟 Proje Özeti
Zimbra ve Stalwart sunucuları yerelde ayağa kaldırılmış ve web tabanlı bir panel aracılığıyla göç işlemleri izlenebilir ve yönetilebilir hale getirilmiştir.
Sistem, paralel worker mantığıyla çalışarak senkronizasyon araçlarını (`imapsync`) arkada Celery ve Redis ile sıraya dizer.

### Mimari Bileşenler:
1. **Stalwart (Mail Sunucusu):** E-postaların taşınacağı hedef e-posta platformu. 
2. **PostgreSQL:** Göç işlemleri ve kuyruğun (metadata ve süreçler) durumlarını kaydetmek için bağlanan veritabanı.
3. **Migration API (FastAPI):** Python ve FastAPI üzerine kurulan asistan arkaplan servisi. Kullanıcıları kaydeder, durumlarını günceller ve Celery işlerini yönlendirir.
4. **Worker (Celery + Redis):** `imapsync` komutlarını arkaplanda asenkron çalıştıran servis.
5. **Frontend (React + Tailwind):** Göç işlemlerinin yönetildiği canlı izleme paneli (Dashboard/Arayüz).

---

## 🛠️ Nasıl Çalıştırılır?

Bu projeyi farklı bir test ortamına taşımak veya baştan kurmak için temel docker-compose komutlarını kullanabilirsiniz.

### 1- Repoyu İndirip Klasöre Girme
```bash
git clone https://github.com/coruhoorhan/zimbrastalwart.git
cd zimbrastalwart
```

### 1.1- Ortam Değişkenlerini Hazırlama (.env)
Önerilen güvenli kullanım için varsayılanları kopyalayın ve parolaları düzenleyin:
```bash
cp .env.example .env
```

### 2- Docker Üzerinden Servisleri Başlatma
Sistemi arka planda güncel baz kalıplarla derleyip ayağa kaldırmak için:
```bash
docker compose up -d --build
```
Bu komut, hem `migration-api` hem de `migration-frontend` dahil tüm yapılası başlatır.

### 3- Yedekleme Betiğinin (Backup) İzinlerini Açma
(Eğer veritabanını planlı olarak yedeklemek isterseniz)
```bash
chmod +x backup/backup.sh
```

---

## 💻 Panele Erişim & Kullanım Kılavuzu

Sunucu adresine giderek migration panosuna doğrudan erişebilirsiniz:  
👉 **http://<SUNUCU_IP_ADRESI>:3000**

### Adım 1: Migration Settings (Zimbra'ya Bağlanma)
* Panel açıldığında üst kısımdaki **"Zimbra Server IP / Host"** alanına, veri çekeceğimiz kaynak Zimbra sunucusunun (Örn: `mail.domain.com` veya `192.168.x.x`) adresini girin.
* "Save Config" (Kaydet) diyerek yönlendirmeyi onaylayın.

### Adım 2: Bağlantıyı Doğrulama (Dry-run Test)
* Alt kısımdaki test formuna Zimbra üzerindeki bir e-posta adresini ve parolasını girin.
* **"Dry-run Test"** düğmesine tıkladığınızda `imapsync` servisi bir login denemesi yapar ve size "Success/Error" bildirimi döndürür. 

### Adım 3: Migration (Göç) Listesi
* Doğrulama yaptıktan sonra kullanıcıları panele **"Add to Migration List"** (Göç Listesine Ekle) diyerek alt kısımdaki tabloya ekleyebilirsiniz.
* Birden çok kullanıcı test işlemi için **"Mock LDAP Import"** düğmesi doğrudan kuyruğa yapay hedef hesaplar ekleyebilir.

### Adım 4: Taşıma İşlemi (Full & Delta Sync)
* **Start Full Sync:** Bekleyen kullanıcı statülerindeki tüm e-postaları hedef sisteme taşıma (kopya) işlemini başlatır. (Arkaplanda Celery görevleri tetiklenir ve statü "FULL_SYNC_RUNNING" olur).
* İlerleme Çubukları (Progress Bar) üzerinden o anki ilerlemeyi ve sonucunda "DONE/ERROR" raporlarını anlık görebilirsiniz.
* **Start Delta Sync:** Süreç bitiminde kayıp olma riskine karşı aradaki zamanda gelen yeni mailleri çekmek için "Delta" senkronizasyonunu tetiklersiniz.

---

## 🐛 Sorun Giderme (Troubleshooting)

* **Panelde "Network Error" Vermesi:** Backend (API) servisinin başlatıldığından emin olun.
  ```bash
  docker compose logs migration-api
  ```
* **İlerlemeler Askıda Kalırsa:** Arkaplandaki celery kuyruğuna (işçiye) erişin:
  ```bash
  docker compose logs worker
  ```

---

> *Not: Github entegrasyonu için ayarlar 27 Şubat 2026 itibariyle MVP aşaması üzerine Orhan ÇORUH hesabına yedeklenmiştir.*
