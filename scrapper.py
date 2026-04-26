import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# הקישורים המדויקים לחיפוש שלך
URLS = {
    "Yad2": "https://www.yad2.co.il/vehicles/cars?manufacturer=32&model=1345&year=2010-2014&km=0-160000",
    "Facebook": "https://www.facebook.com/marketplace/category/vehicles?minYear=2010&maxYear=2014&maxMileage=160000&query=Seat%20Ibiza&exact=false"
}

def scrape_cars():
    cars_found = []
    
    # פתיחת דפדפן וירטואלי
    with sync_playwright() as p:
        # פתיחת דפדפן (headless=True אומר שהוא רץ ברקע ללא חלון ויזואלי)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("מתחיל סריקה...")

        # --- סריקת יד 2 (דוגמה למבנה, דורש התאמת סלקטורים בהמשך) ---
        try:
            print("סורק את יד 2...")
            page.goto(URLS["Yad2"], timeout=60000)
            time.sleep(5) # ממתינים לטעינת הדף
            
            # כאן נכנס לוגיקת החילוץ. כרגע נשים נתוני דוגמה כדי לבנות את האתר
            # בפועל נשתמש ב: page.query_selector_all('.feeditem')
            cars_found.append({
                "title": "סיאט איביזה 1.2 TSI (2012)",
                "price": "₪25,000",
                "km": "145,000",
                "link": URLS["Yad2"],
                "source": "יד 2"
            })
        except Exception as e:
            print(f"שגיאה בסריקת יד 2: {e}")

        # --- סריקת פייסבוק ---
        try:
            print("סורק את פייסבוק מרקטפלייס...")
            page.goto(URLS["Facebook"], timeout=60000)
            time.sleep(5)
            
            # נתוני דוגמה עד שנפצח את ההגנות
            cars_found.append({
                "title": "Seat Ibiza 2011 ידנית",
                "price": "₪18,500",
                "km": "158,000",
                "link": URLS["Facebook"],
                "source": "Facebook"
            })
        except Exception as e:
            print(f"שגיאה בסריקת פייסבוק: {e}")

        browser.close()
    
    return cars_found

def generate_html(cars):
    # יצירת תבנית HTML מותאמת לנייד (Responsive) בעזרת Bootstrap
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>רכבים למכירה - סיאט איביזה</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .card {{ border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            .source-badge {{ font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <h1 class="text-center mb-4">מצאתי לך איביזות! 🚗</h1>
            <p class="text-center text-muted">עודכן לאחרונה: {current_time}</p>
            
            <div class="row">
    """
    
    # הוספת כל רכב שנמצא כ"כרטיסייה" יפה
    if not cars:
        html_content += "<div class='alert alert-warning text-center'>לא נמצאו רכבים חדשים בסריקה זו.</div>"
    else:
        for car in cars:
            badge_color = "bg-primary" if car['source'] == 'Facebook' else "bg-warning text-dark"
            html_content += f"""
                <div class="col-md-6 col-lg-4">
                    <div class="card p-3">
                        <span class="badge {badge_color} source-badge mb-2">{car['source']}</span>
                        <h5 class="card-title">{car['title']}</h5>
                        <p class="card-text mb-1"><strong>מחיר:</strong> {car['price']}</p>
                        <p class="card-text mb-3"><strong>קילומטראז':</strong> {car['km']}</p>
                        <a href="{car['link']}" target="_blank" class="btn btn-success w-100">צפה במודעה</a>
                    </div>
                </div>
            """
            
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # שמירת הקובץ
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("קובץ index.html נוצר בהצלחה!")

# הפעלת התהליך
if __name__ == "__main__":
    scraped_data = scrape_cars()
    generate_html(scraped_data)