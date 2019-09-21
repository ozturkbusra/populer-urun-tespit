from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import requests
from bs4 import BeautifulSoup

# siteHaritasi
kategori_url, kategori_isim = [], []
def siteHaritasi():
    sayfaKaynak = requests.get("https://www.n11.com/site-haritasi")  # Sayfa kaynagı cekıldı
    soup = BeautifulSoup(sayfaKaynak.content, "html.parser")  # sayfa kaynagını güzellestırıp soup sabıtıne atadı
    gelen_veri = soup.find("div", {"class": "cols col4"})  # bu class a sahip olan div deki html kodlarını aldı
    kategori_bilgiler = gelen_veri.find_all("a", {"class": "link"})

    for link in kategori_bilgiler:
        kategori_url.append(link.get("href"))  # Linkleri listeye ekledik

    for isim in kategori_bilgiler:
        kategori_isim.append(isim.text)  # Kategori isimlerini aldık

# urunMagaza
altKategori, alt_URL, urun_ad, magaza_ad = [], [], [], []
def urunMagaza():
    kategori_URL = kategori_url[28]  # Fotograf ve Kamera kategorı URL sını aldık
    sayfa_kaynak = requests.get(kategori_URL)
    soup = BeautifulSoup(sayfa_kaynak.content, "html.parser")
    gelen_veri = soup.find_all("li", {"class": "filterItem parent"})
    gelen_veri = gelen_veri[0].find_all("li", {"class": "filterItem"})  # Tek tek alt kategori bilgileri listesi

    for veriler in gelen_veri:
        alt_kategori_bilgiler = veriler.find_all("a")
        for altLink in alt_kategori_bilgiler:
            altKategori.append(altLink.get("href"))  # Alt Kategori linklerini listeye ekledik 7 adet

    # Tum Alt Kategorilerin içeriklerini sorgulayacak
    for kategori in altKategori:

        # Sayfa kaynagını cektik
        sayfa_kaynak = requests.get(kategori)
        altSoup = BeautifulSoup(sayfa_kaynak.content, "html.parser")

        # 2 alt kategoriden
        gelen2_veri = (altSoup.find_all("li", {"class": "filterItem parent"})[0].find_all("li", {"class": "filterItem"}))

        # 2 ALT KATEGORIYI SORGULA
        if len(gelen2_veri) > 0:

            # 2 ALT KATEGORI LINK LISTESI
            alt2Kategori = []
            for veriler in gelen2_veri:
                alt2_kategori_bilgiler = veriler.find_all("a")
                for alt2Link in alt2_kategori_bilgiler:
                    alt2Kategori.append(alt2Link.get("href"))

            for alt2Link in alt2Kategori:

                # Alt 2 Kategorideki toplam sayfa sayısı
                alt2sayfa_kaynak = requests.get(alt2Link)
                alt2Soup = BeautifulSoup(alt2sayfa_kaynak.content, "html.parser")
                sayi = alt2Soup.find("input", {"name": "pageCount"})
                toplamSayfa = sayi.get("value")

                for sayfaNo in range(1, int(toplamSayfa) + 1):
                    # SAYFA KAYNAGI
                    alt2URL = alt2Link + "?pg=" + str(sayfaNo)
                    alt2_sayfa_kaynak = requests.get(alt2URL)
                    alt2SayfaSoup = BeautifulSoup(alt2_sayfa_kaynak.content, "html.parser")

                    gelen2_veri2 = alt2SayfaSoup.find("div", {"class": "listView"})

                    # Urunleri urun_ad'e atadık
                    urun_bilgiler = gelen2_veri2.find_all("a", {"class": "plink"})
                    for urun in urun_bilgiler:
                        urun_ad.append(urun.get("title"))
                        alt_URL.append(alt2URL)  # Sayfa linkini listeye ekledik

                    # Magazaları magazaAdiList'e atadık
                    magaza_bilgiler = gelen2_veri2.find_all("a", {"class": "sallerInfo"})
                    for magaza in magaza_bilgiler:
                        magaza_ad.append(magaza.get("title"))

        # 2 ALT KATEGORI YOKSA BURAYA GIRECEK
        else:
            # Alt Kategorideki toplam sayfa sayısı
            sayi = altSoup.find("input", {"name": "pageCount"})
            toplamSayfa = sayi.get("value")

            # Tüm sayfaları döndür
            for sayfaNo in range(1, int(toplamSayfa) + 1):

                altURL = kategori + "?pg=" + str(sayfaNo)
                alt_sayfa_kaynak = requests.get(altURL)
                altSayfaSoup = BeautifulSoup(alt_sayfa_kaynak.content, "html.parser")

                gelen_veri = altSayfaSoup.find_all("div", {"class": "listView"})
                # 5 content var. bizimkinin indisi 3
                gelen_veri = (gelen_veri[0].contents)[len(gelen_veri[0].contents) - 2]  # ul kısmını aldı html kodlarının

                # Urun Adlarını urun_ad'a ekledik
                urun_bilgiler = gelen_veri.find_all("a", {"class": "plink"})
                for urun in urun_bilgiler:
                    urun_ad.append(urun.get("title"))
                    alt_URL.append(altURL)  # Sayfa linkini listeye ekledik (esit sayıda olması ıcın)

                # Magaza Adlarını magaza_ad'a ekledik
                magaza_bilgiler = gelen_veri.find_all("a", {"class": "sallerInfo"})
                for magaza in magaza_bilgiler:
                    magaza_ad.append(magaza.get("title"))

# magazaYorum
urunYorum, yorum, tarih, yorum2 = [], [], [], []
def magazaYorum():
    sayfa_kaynak = requests.get("https://www.n11.com/magaza/photoaksesuar/magaza-yorumlari")
    soup = BeautifulSoup(sayfa_kaynak.content, "html.parser")

    toplamSayfa = soup.find_all("span", {"class": "pageCount"})
    toplamSayfa = toplamSayfa[0].text

    for sayfaNo in range(1, int(toplamSayfa)+1):
        yorumSayfa_kaynak = requests.get("https://www.n11.com/component/render/sellerShopFeedbacks?page=" + str(sayfaNo) + "&sellerId=" + str(77301))
        yorumSoup = BeautifulSoup(yorumSayfa_kaynak.content, "html.parser")

        gelen_veri = yorumSoup.find_all("div", {"class": "list"})
        gelen_veri = (gelen_veri[0].contents)[len(gelen_veri[0].contents) - 2]  # ul kısmını aldık. tüm li'ler burada

        # URUNLER
        urun_bilgiler = gelen_veri.find_all("div", {"class": "productInfo"})  # yorumdaki title'sız a taglerınden kurtulmak ıcın
        for i in range(len(urun_bilgiler)):
            urun_bilgi = urun_bilgiler[i].find_all("a")
            for urun in urun_bilgi:
                urunYorum.append(urun.get("title"))
        # YORUMLAR
        yorum_bilgiler = gelen_veri.find_all("div", {"class": "comment"})
        for i in range(len(yorum_bilgiler)):
            yorum.append(yorum_bilgiler[i].find("p").get_text().split("\n"))
        for i in yorum:
            yorum2.append(" ".join(i).strip()) # paragrafı tek satıra ındırmek ıcın
        # TARIH
        tarihBilgi = yorumSoup.find_all("span", {"class": "commentDate"})
        for i in range(len(tarihBilgi)):
            tarih.append(tarihBilgi[i].text.strip())

# populerUrun
tekrarUrun, unique, populer = [], [], []
def populerUrun():

    # Urunlerin tekrarlanma sayılarını buluyoruz
    for i in range(len(urunYorum)):
        tekrar = 0
        for j in range(len(urunYorum)):
            if urunYorum[i] == urunYorum[j]:
                tekrar += 1
        tekrarUrun.append(str(tekrar) + " ADET " + urunYorum[i])

    # Listedeki aynı verilerin sadece 1'ini aldık
    for urun in tekrarUrun:
        if urun not in unique:
            unique.append(urun)

    # POPULER URUNLERIN LISTESI
    for i in range(len(unique)):
        ayir = unique[i].split()  # bosluklardan ayırarak yenı bı dızı olusturduk
        adet = int(ayir[0])
        if adet > 30:
            del ayir[0:2]  # basta yazan x ADET yazısını sıldık
            birlestir = " ".join(ayir)
            populer.append(birlestir)

# Dosya metodlari
def dosyaSiteHaritasi():
    yazSite = open("siteDosya.txt", "w")
    for i in range(len(kategori_url)):
        yazSite.write(str(kategori_isim[i]))
        yazSite.write("\n")
        yazSite.write("\t")
        yazSite.write(str(kategori_url[i]))
        yazSite.write("\n")
    yazSite.close()

    yazSiteIsım = open("siteDosyaIsım.txt", "w")
    for i in range(len(kategori_url)):
        yazSiteIsım.write(str(kategori_isim[i]))
        yazSiteIsım.write("\n")
    yazSiteIsım.close()

    yazSiteURL = open("siteDosyaURL.txt", "w")
    for i in range(len(kategori_url)):
        yazSiteURL.write(str(kategori_url[i]))
        yazSiteURL.write("\n")
    yazSite.close()
def dosyaUrunMagaza():
    yaz = open("urunMagazaVerileri.txt", "w", encoding="utf-8")
    for i in range(len(urun_ad)):
        yaz.write(str(urun_ad[i]))
        yaz.write("\n")
        yaz.write("\t")
        yaz.write(str(magaza_ad[i]))
        yaz.write("\n")
        yaz.write("\t")
        yaz.write(str(alt_URL[i]))
        yaz.write("\n")
    yaz.close()

    yazUrun = open("urunVerileri0.txt", "w", encoding="utf-8")
    for i in range(len(urun_ad)):
        yazUrun.write(str(urun_ad[i]))
        yazUrun.write("\n")
    yazUrun.close()

    yazMagaza = open("magazaVerileri0.txt", "w", encoding="utf-8")
    for i in range(len(magaza_ad)):
        yazMagaza.write(str(magaza_ad[i]))
        yazMagaza.write("\n")
    yazMagaza.close()

    yazURL = open("urlVerileri0.txt", "w", encoding="utf-8")
    for i in range(len(alt_URL)):
        yazURL.write(str(alt_URL[i]))
        yazURL.write("\n")
    yazURL.close()
def dosyaMagazaYorum():
    yazUrunY = open("urunYorumDosya.txt", "w", encoding="utf-8")
    for i in range(len(urunYorum)):
        yazUrunY.write(str(urunYorum[i]))
        yazUrunY.write("\n")
    yazUrunY.close()

    yazYorum = open("yorumDosya.txt", "w", encoding="utf-8")
    for i in range(len(yorum)):
        yazYorum.write(str(yorum2[i]))
        yazYorum.write("\n")
    yazYorum.close()

    yazTarih = open("tarihDosya.txt", "w", encoding="utf-8")
    for i in range(len(tarih)):
        yazTarih.write(str(tarih[i]))
        yazTarih.write("\n")
    yazTarih.close()

    yazYorumVeriler = open("yorumSayfaVerileri.txt", "w", encoding="utf-8")
    for i in range(len(urunYorum)):
        yazYorumVeriler.write(str(i+1))
        yazYorumVeriler.write(". ")
        yazYorumVeriler.write(str(urunYorum[i]))
        yazYorumVeriler.write(" >> ")
        yazYorumVeriler.write(str(yorum2[i]))
        yazYorumVeriler.write(" >> ")
        yazYorumVeriler.write(str(tarih[i]))
        yazYorumVeriler.write("\n")
    yazYorumVeriler.close()
def dosyaPopulerUrun():
    yazUnique = open("uniqueDosya.txt", "w")
    for i in range(len(unique)):
        yazUnique.write(str(unique[i]))
        yazUnique.write("\n")
    yazUnique.close()

    yazPopuler = open("populerDosya.txt", "w")
    for i in range(len(populer)):
        yazPopuler.write(str(populer[i]))
        yazPopuler.write("\n")
    yazPopuler.close()

# PYQT5

kat_isimler, kat_url = [], []
urun_oku, magaza_oku, url_oku = [], [], []
urunY_oku, yorum_oku, tarih_oku = [], [], []
adet_oku = []
pop_oku = []

def oku():
    # Site Haritası
    siteIsimOku = open("siteDosyaIsım.txt", "r")
    for satir in siteIsimOku:
        kat_isimler.append(satir)

    siteUrlOku = open("siteDosyaURL.txt", "r")
    for satir in siteUrlOku:
        kat_url.append(satir)
    siteUrlOku.close()

    # Urunler
    urunOku = open("urunVerileri0.txt", "r", encoding="utf-8")
    for satir in urunOku:
        urun_oku.append(satir)
    urunOku.close()

    magazaOku = open("magazaVerileri0.txt", "r", encoding="utf-8")
    for satir in magazaOku:
        magaza_oku.append(satir)
    magazaOku.close()

    urlOku = open("urlVerileri0.txt", "r", encoding="utf-8")
    for satir in urlOku:
        url_oku.append(satir)
    urlOku.close()

    # Yorumlar
    urunYorumOku = open("urunYorumDosya.txt", "r", encoding="utf-8")
    for satir in urunYorumOku:
        urunY_oku.append(satir)
    urunYorumOku.close()

    yorumOku = open("yorumDosya.txt", "r", encoding="utf-8")
    for satir in yorumOku:
        yorum_oku.append(satir)
    yorumOku.close()

    tarihOku = open("tarihDosya.txt", "r", encoding="utf-8")
    for satir in tarihOku:
        tarih_oku.append(satir)
    tarihOku.close()

    # Adet
    adetOku = open("uniqueDosya.txt", "r")
    for satir in adetOku:
        adet_oku.append(satir)
    adetOku.close()

    # Populer
    popOku = open("populerDosya.txt", "r")
    for satir in popOku:
        pop_oku.append(satir)
    popOku.close()

def pencere():
    app = QApplication(sys.argv)
    pencere = QWidget()

    # TABLE SITE HARITASI
    tableKategori = QTableWidget()
    tableKategori.setRowCount(len(kat_isimler))
    tableKategori.setColumnCount(2)
    tableKategori.setFixedHeight(350)
    # TABLE URUN
    tableUrun = QTableWidget()
    tableUrun.setRowCount(len(urun_oku))
    tableUrun.setColumnCount(3)
    tableUrun.setFixedHeight(350)
    # TABLE YORUM
    tableYorum = QTableWidget()
    tableYorum.setRowCount(len(urunY_oku))
    tableYorum.setColumnCount(3)
    tableYorum.setFixedHeight(350)
    # TABLE ADET
    tableAdet = QTableWidget()
    tableAdet.setRowCount(len(adet_oku))
    tableAdet.setColumnCount(1)
    tableAdet.setFixedHeight(350)
    # TABLE POPULER
    tablePopuler = QTableWidget()
    tablePopuler.setRowCount(len(pop_oku))
    tablePopuler.setColumnCount(1)
    tablePopuler.setFixedHeight(200)

    # KATEGORI BASLIKLARI
    sutunKatIsım = QTableWidgetItem("KATEGORI AD")
    sutunKatIsım.setFont(QFont("Ariel", 10, QFont.Bold))

    sutunKatUrl = QTableWidgetItem("KATEGORI URL")
    sutunKatUrl.setFont(QFont("Ariel", 10, QFont.Bold))

    tableKategori.setHorizontalHeaderItem(0, sutunKatIsım)
    tableKategori.setHorizontalHeaderItem(1, sutunKatUrl)

    # URUN BASLIKLARI
    sutunUrun = QTableWidgetItem("URUN")
    sutunUrun.setFont(QFont("Ariel", 10, QFont.Bold))

    sutunMagaza = QTableWidgetItem("MAGAZA")
    sutunMagaza.setFont(QFont("Ariel", 10, QFont.Bold))

    sutunUrl = QTableWidgetItem("URL")
    sutunUrl.setFont(QFont("Ariel", 10, QFont.Bold))

    tableUrun.setHorizontalHeaderItem(0, sutunUrun)
    tableUrun.setHorizontalHeaderItem(1, sutunMagaza)
    tableUrun.setHorizontalHeaderItem(2, sutunUrl)

    # YORUM BASLIKLARI
    sutunUrunY = QTableWidgetItem("URUN")
    sutunUrunY.setFont(QFont("Ariel", 10, QFont.Bold))

    sutunYorum = QTableWidgetItem("YORUM")
    sutunYorum.setFont(QFont("Ariel", 10, QFont.Bold))

    sutunTarih = QTableWidgetItem("TARIH")
    sutunTarih.setFont(QFont("Ariel", 10, QFont.Bold))

    tableYorum.setHorizontalHeaderItem(0, sutunUrunY)
    tableYorum.setHorizontalHeaderItem(1, sutunYorum)
    tableYorum.setHorizontalHeaderItem(2, sutunTarih)

    # ADET BASLIK
    sutunBilgi = QTableWidgetItem("URUN ADET BILGISI")
    sutunBilgi.setFont(QFont("Ariel", 10, QFont.Bold))

    tableAdet.setHorizontalHeaderItem(0, sutunBilgi)

    #POPULER BASLIK
    sutunPop = QTableWidgetItem("POPULER URUNLER")
    sutunPop.setFont(QFont("Ariel", 10, QFont.Bold))

    tablePopuler.setHorizontalHeaderItem(0, sutunPop)

    # Verileri donduruyor
    for i in range(len(kat_isimler)):
        katIsim = QTableWidgetItem(kat_isimler[i])
        katUrl = QTableWidgetItem(kat_url[i])
        tableKategori.setItem(i,0,katIsim)
        tableKategori.setItem(i,1,katUrl)

    for i in range(len(urun_oku)):
        urun = QTableWidgetItem(urun_oku[i])
        magaza = QTableWidgetItem(magaza_oku[i])
        url = QTableWidgetItem(url_oku[i])
        tableUrun.setItem(i, 0, urun)
        tableUrun.setItem(i, 1, magaza)
        tableUrun.setItem(i, 2, url)

    for i in range(len(urunY_oku)):
        urun = QTableWidgetItem(urunY_oku[i])
        yorum = QTableWidgetItem(yorum_oku[i])
        tarih = QTableWidgetItem(tarih_oku[i])
        tableYorum.setItem(i, 0, urun)
        tableYorum.setItem(i, 1, yorum)
        tableYorum.setItem(i, 2, tarih)

    for i in range(len(adet_oku)):
        adet = QTableWidgetItem(adet_oku[i])
        tableAdet.setItem(i, 0, adet)

    for i in range(len(pop_oku)):
        pop = QTableWidgetItem(pop_oku[i])
        tablePopuler.setItem(i, 0, pop)

    # Column ve Row boyutlarını içeriğe eşitliyor
    tableKategori.resizeColumnsToContents()
    tableKategori.resizeRowsToContents()

    tableUrun.resizeColumnsToContents()
    tableUrun.resizeRowsToContents()

    tableYorum.resizeColumnsToContents()
    tableYorum.resizeRowsToContents()

    tableAdet.resizeColumnsToContents()
    tableAdet.resizeRowsToContents()

    tablePopuler.resizeColumnsToContents()
    tablePopuler.resizeRowsToContents()

    # Layout olustur
    v_box = QFormLayout()
    v_box.addWidget(tableKategori)
    v_box.addWidget(tableUrun)
    v_box.addWidget(tableYorum)
    v_box.addWidget(tableAdet)
    v_box.addWidget(tablePopuler)

    groupB = QGroupBox()
    groupB.setLayout(v_box)

    scroll = QScrollArea()
    scroll.setWidget(groupB)
    scroll.setWidgetResizable(True)

    v_box2 =QVBoxLayout()
    v_box2.addWidget(scroll)

    # Layoutu pencereye ekle
    pencere.setLayout(v_box2)
    pencere.setGeometry(600,600,600,600)
    pencere.setWindowTitle("N11 VERILERI")
    pencere.show()

    #Bitis
    sys.exit(app.exec())

oku()
pencere()