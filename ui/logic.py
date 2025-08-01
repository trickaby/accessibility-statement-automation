from django.core.exceptions import ValidationError

from accessibility_scraper.src.modules.web_scraper import (
    get_prepared_date, get_last_reviewed_date, get_last_tested_date, who_tested_by, check_header_present,
    check_technical_information, check_compliance_status, wcag_version, check_feedback_contact_email,
    check_feedback_contact_phone, reporting_contact_email, reporting_contact_phone, check_non_accessible_content,
    open_page
)
from ui.models import Product, Report
import csv
from django.conf import settings
from ui.models import Report


def scrape_page(driver, product):
    field_funcs = {
        'prepared_by_date': lambda: False,
        'last_reviewed_date': lambda: get_last_reviewed_date(driver),
        'last_tested_date': lambda: get_last_tested_date(driver),
        'tested_by': lambda: who_tested_by(driver),
        'feedback_header': lambda: check_header_present(driver, 'Feedback and contact information'),
        'reporting_problems': lambda: check_header_present(driver, 'Reporting accessibility problems with this website'),
        'enforcement_procedure': lambda: check_header_present(driver, 'Enforcement procedure'),
        'technical_information_wording': lambda: check_technical_information(driver),
        'compliance_status': lambda: check_compliance_status(driver),
        'wcag': lambda: wcag_version(driver),
        'feedback_contact_email': lambda: check_feedback_contact_email(driver),
        'feedback_contact_phone': lambda: check_feedback_contact_phone(driver),
        'reporting_problems_contact_email': lambda: reporting_contact_email(driver),
        'reporting_problems_contact_phone': lambda: reporting_contact_phone(driver),
        'non_accessible_content': lambda: check_non_accessible_content(driver, product.name),
    }
    report = Report(product=product)

    for field, func in field_funcs.items():
        try:
            setattr(report, field, func())
            report.full_clean(exclude=[f for f in field_funcs.keys() if f != field])
        except Exception as e:
            print(f"Failed to get {field} for {product.name}: {e}")
            setattr(report, field, None)

    try:
        report.save(force_insert=True)
        print(f"Report saved for {product.name} (id={report.id})")
        return report
    except ValidationError as e:
        print(f"Validation error for {product.name}: {e}")
    except Exception as e:
        print(f"Failed to save report for {product.name}. Error: {e}")
        return report

def run_logic(config):
    products = Product.objects.exclude(statement_url__isnull=True).exclude(statement_url__exact="")
    for product in products:
        url = product.statement_url
        try:
            driver = open_page(url, config.headless_mode)
            scrape_page(driver, product)
            driver.quit()
        except Exception as e:
            print(f"Row {product.name if hasattr(product, 'name') else 'not found'}: Failed to scrape {url}. Error: {e}")


def output_db_to_csv():
    output_file = settings.BASE_DIR / 'reports.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [field.name for field in Report._meta.fields]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for report in Report.objects.all():
            writer.writerow({field: getattr(report, field) for field in fieldnames})

    return str(output_file.resolve())