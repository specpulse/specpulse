# AI-SpecPulse CLI Integration Guide

This guide explains how AI assistants (Claude/Gemini) use the SpecPulse CLI tool and what happens when CLI commands fail.

## 🤖 AI-CLI İşbirliği

### AI Rollü
- **İçerik Üretimi**: Spesifikasyon, plan, task detayları
- **Stratejik Planlama**: Mimari kararları, bağımlılıklar
- **Implementasyon**: Kod yazma, test etme
- **Validasyon**: Kalite kontroli, doğrulama

### CLI Rollü
- **Strüktür Yönetimi**: Dizin oluşturma, dosya organizasyonu
- **Metadata**: ID atama, versiyon takibi, durum yönetimi
- **Validasyon**: Sözdizimi kontrolü, yapısal bütünlük
- **Cross-platform**: Windows/macOS/Linux uyumluluğu

### İşbirliği Deseni
```
1. AI: "Kullanıcı kimlik doğrulama spec'i oluştur" → CLI: specpulse spec create
2. CLI: Dizin ve dosya oluşturur → AI: İçeriği doldurur ve detaylandırır
3. AI: "Bu spec için plan oluştur" → CLI: specpulse plan create
4. CLI: Plan yapısı oluşturur → AI: Plan detaylarını geliştirir
5. AI: "Taskları böl" → CLI: specpulse task breakdown
6. CLI: Task dosyaları oluşturur → AI: Task içeriğini zenginleştirir
7. AI: "Taskleri çalıştır" → CLI: specpulse execute status
8. CLI: Durumu gösterir → AI: Taskları implemente eder ve tamamlar
```

## 🛡️ CLI Başarısızlık Senaryoları

### Yaygın CLI Hataları
1. **Command Not Found**: Komut mevcut değil
2. **Permission Denied**: Dosya izinleri yok
3. **Path Issues**: Yol bulunamadı
4. **Dependencies**: Eksik bağımlılıklar
5. **Unicode/Encoding**: Karakter kodlama sorunları
6. **Timeout**: Komut zaman aşımı

### AI'nın Cevabı
**KESİNLİK**: AI asla durmaz, her zaman alternatif yol kullanır

## 🔄 Fallback Mekanizmaları

### Seviye 1: CLI Retry
```bash
# AI ilk denemesi
specpulse spec create "Kullanıcı kimlik doğrulama"
```

### Seviye 2: Manuel Strüktür
```bash
# CLI başarısız olursa
mkdir -p .specpulse/specs/001-user-authentication
touch .specpulse/specs/001-user-authentication/spec-001.md
# Manuel içerik ekleme...
```

### Seviye 3: Gömülü Template
```markdown
# CLI başarısız olursa
<!-- AI: Gömülü template kullanarak spec oluştur -->
# Specification: Kullanıcı kimlik doğrulama

<!-- FEATURE_DIR: 001-user-authentication -->
<!-- FEATURE_ID: 001 -->
<!-- SPEC_NUMBER: 001 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-11-02T12:00:00 -->

## Description
Kullanıcı kimlik doğrulama sistemi

## Requirements
[AI tarafından doldurulacak...]
```

## 📋 AI Komutları ve CLI Kullanımı

### /sp-spec Komutu
```bash
# AI komutu
/sp-spec "Kullanıcı kimlik doğrulama JWT ile"

# CLI denemesi
Bash: specpulse spec create "Kullanıcı kimlik doğrulama JWT ile"

# Başarılı → AI spec'i genişletir
# Başarısız → AI manuel spec oluşturur
```

### /sp-plan Komutu
```bash
# AI komutu
/sp-plan "Güvenli kimlik doğrulama akışı"

# CLI denemesi
Bash: specpulse plan create "Güvenli kimlik doğrulama akışı"

# Başarılı → AI planı detaylandırır
# Başarısız → AI manuel plan oluşturur
```

### /sp-task Komutu
```bash
# AI komutu
/sp-task 001

# CLI denemesi
Bash: specpulse task breakdown 001

# Başarılı → AI task'ları detaylandırır
# Başarısız → AI manuel task oluşturur
```

### /sp-execute Komutu
```bash
# AI komutu
/sp-execute

# CLI denemesi
Bash: specpulse execute status

# Başarılı → AI durumu görür ve task'ları çalıştırır
# Başarısız → AI manuel task takibi yapar
```

## 🚨 CLI Olmadığında Ne Olur?

### Tam Manuel Mod
AI SpecPulse CLI olmadan bile çalışmaya devam eder:

```python
# AI'nin manuel prosedürü
def create_spec_without_cli(description):
    # 1. Dizin yapısı oluştur
    feature_dir = create_feature_directory()

    # 2. Spec dosyası oluştur
    spec_file = f"{feature_dir}/spec-001.md"

    # 3. İçerik oluştur
    content = f"""# Specification: {description}

    ## Description
    {description}

    ## Requirements
    [AI tarafından doldurulacak...]
    """

    # 4. Dosyayı kaydet
    with open(spec_file, 'w') as f:
        f.write(content)

    return spec_file
```

### Sınırlı Mod
CLI olmadığında bazı özellikler sınırlı olabilir:
- ✅ Spec, plan, task oluşturma (manuel)
- ✅ İçerik üretimi (AI)
- ✅ Dosya yönetimi (Read/Write/Edit)
- ❌ Otomatik ID atama (manuel)
- ❌ Otomatik validasyon (manuel)
- ❌ Cross-platform optimizasyonu (manuel)

## 📊 Başarı Oranları

### CLI Çalıştığında
- ✅ Hız: 3-5x daha hızlı
- ✅ Tutarlılık: %99+ başarı oranı
- ✅ Özellikler: Tüm özellikler mevcut
- ✅ Kalite: Otomatik validasyon ve hata kontrolü

### CLI Başarısız Olduğunda
- ⚠️ Hız: 2-3x daha yavaş
- ✅ Tutarlılık: %95+ başarı oranı (fallback ile)
- ✅ Özellikler: %80-90 özellikler mevcut
- ⚠️ Kalite: Manuel validasyon gerekir

## 🔧 Kurulum ve Kurulum

### AI Asistanları İçin
AI komutları zaten SpecPulse ile birlikte gelir:
- **Claude Code**: `.claude/commands/sp-*.md` dosyaları
- **Gemini CLI**: `.gemini/commands/sp-*.toml` dosyaları

### Manuel Kurulum
```bash
# AI komutlarının kurulu olduğunu kontrol et
ls .claude/commands/
ls .gemini/commands/

# Eğer eksikse, SpecPulse'yi yeniden kur
pip install --upgrade specpulse
```

## 🧪 Test Senaryoları

### Test 1: CLI Mevcut
```bash
# Normal durum
/spec-spec "Test specification"
# Beklenen: CLI başarılı, AI spec'i genişletir
```

### Test 2: CLI Eksik
```bash
# CLI kaldırıldığında
mv /usr/local/bin/specpulse /usr/local/bin/specpulse.backup
/spec-spec "Test specification"
# Beklenen: CLI başarısız, AI fallback kullanır
```

### Test 3: CLI Bozuk
```bash
# CLI bozuk olduğunda
echo "#!/bin/bash\necho 'CLI command failed'\nexit 1" > /usr/local/bin/specpulse
chmod +x /usr/local/bin/specpulse
/sp-spec "Test specification"
# Beklenen: CLI başarısız, AI fallback kullanır
```

## 📞 Sorun Çözümü

### AI Komutları Çalışmıyorsa
1. **SpecPulse kurulumunu kontrol et**:
   ```bash
   specpulse --version
   ```

2. **AI komut dosyalarını kontrol et**:
   ```bash
   ls .claude/commands/sp-spec.md
   ls .gemini/commands/sp-spec.toml
   ```

3. **Python path kontrolü**:
   ```bash
   python -c "import specpulse; print('OK')"
   ```

4. **Fallback logunu kontrol et**:
   ```bash
   cat .specpulse/fallback.log
   ```

### Manuel Kurtarma
CLI tamamen kullanılamıyorsa:

1. **Dizin yapısını manuel oluştur**:
   ```bash
   mkdir -p .specpulse/{specs,plans,tasks,memory,templates}
   ```

2. **Template'leri kopyala**:
   ```bash
   # Gömülü template'leri kullan
   ```

3. **Manuel ID atama**:
   ```bash
   # 001-, 002- formatında ID'ler kullan
   ```

4. **AI komutlarını kullanmaya devam et**:
   ```bash
   # AI komutları fallback ile çalışmaya devam edecek
   ```

## ✅ Başarı Kriterleri

AI-SpecPulse entegrasyonu başarılı sayılır when:

- [ ] CLI mevcut olduğunda AI onu öncelikli kullanır
- [ ] CLI başarısız olduğunda otomatik fallback kullanır
- [ ] Tüm AI komutları fallback ile çalışmaya devam eder
- [ ] Kullanıcıya fallback kullanıldığı bildirilir
- [ ] Fallback logları tutulur ve debugging için kullanılır
- [ ] Manuel modda bile temel işlevler çalışır

**Unutma**: AI asla tamamen başarısız olmamalı! Her zaman bir alternatif yol vardır. 🚀