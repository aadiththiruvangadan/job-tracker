"""
Scrapes remote software/tech jobs from RemoteOK's public jobs feed and
saves the ones that look software-related into the Job model.

Usage:
    python manage.py scrape_jobs
    python manage.py scrape_jobs --limit 50
"""
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from jobs.models import Job
from playwright.sync_api import sync_playwright


class Command(BaseCommand):
    help = "Scrapes job listings from Internshala and Wellfound"

    def handle(self, *args, **options):
        self.stdout.write("Scraping Internshala...")
        self.scrape_internshala()

        self.stdout.write("Scraping Wellfound...")
        self.scrape_wellfound()

        self.stdout.write(self.style.SUCCESS("Scraping completed!"))

    def scrape_internshala(self):
        """Your existing Internshala scraper logic."""
        # Add or keep your working Internshala scraper code here
        pass

    def fetch_wellfound_rendered(self):
        """Uses Headless Chromium via Playwright with realistic settings and explicit wait."""
        with sync_playwright() as p:
            # 1. Launch Chromium with anti-detection flags
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )

            # 2. Create context with typical browser viewport and user agent
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )

            page = context.new_page()

            # 3. Wait for DOM content instead of networkidle
            page.goto(
                "https://wellfound.com/role/l/software-engineer/india",
                wait_until="domcontentloaded",
                timeout=60000,  # 60s timeout
            )

            # 4. Give React components a few seconds to hydrate and mount job cards
            page.wait_for_timeout(5000)

            content = page.content()
            browser.close()
            return content
    def scrape_wellfound(self):
        """Parses Wellfound job cards and saves them to the database."""
        try:
            html_content = self.fetch_wellfound_rendered()
            soup = BeautifulSoup(html_content, "html.parser")

            job_elements = soup.find_all("a", href=re.compile(r"/jobs/\d+"))

            fresher_keywords = [
                "fresher",
                "junior",
                "jr",
                "entry level",
                "intern",
                "0-1",
                "graduate",
                "sde-1",
                "sde 1",
            ]
            scraped_count = 0

            for el in job_elements:
                title = el.get_text(strip=True)
                href = el.get("href", "")
                full_url = (
                    f"https://wellfound.com{href}"
                    if href.startswith("/")
                    else href
                )

                match = re.search(r"/jobs/(\d+)", href)
                ext_id = match.group(1) if match else None

                # Filter for entry level / fresher roles
                if any(
                    kw in title.lower() for kw in fresher_keywords
                ) or not any(
                    sen in title.lower()
                    for sen in ["senior", "lead", "staff", "principal", "sr."]
                ):
                    job, created = Job.objects.get_or_create(
                        apply_link=full_url,
                        defaults={
                            "job_title": title,
                            "company_name": "Startup (via Wellfound)",
                            "location": "India / Remote",
                            "source": "Wellfound",
                            "external_id": ext_id,
                            "description": "Software role scraped from Wellfound.",
                        },
                    )
                    if created:
                        scraped_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully saved {scraped_count} jobs from Wellfound."
                )
            )

        except Exception as e:
            self.stderr.write(f"Error scraping Wellfound: {e}")