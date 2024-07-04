import db_query
import pdf_utils
import selenium_utils as sutils


DOWNLOAD_PATH = "/Users/$HOME/Desktop/drs_test_data"
AD_PREFIX_STRING = "<p>"
PDF_OUTPUT_PATH = "/Users/$HOME/Desktop/drs_test_data"


def main():
    make = "Beechcraft"
    model = "J35"
    set_limit = "5"

    db_results = db_query.lookup_ad(make, model, set_limit) 
    print(db_results)

    if not db_results:
        print("No ADs found in Database")

    for ad in db_results:
        ad_number, unid = ad
        drs_request_url = sutils.build_drs_request_url(unid)
        ad_content = sutils.download_ad_content(drs_request_url)
        ad_html_file = sutils.save_ad_content(ad_content, ad_number, DOWNLOAD_PATH)

        if ad_html_file:
            pdf_utils.convert_html_to_pdf(ad_html_file, AD_PREFIX_STRING, DOWNLOAD_PATH)
            pdf_utils.cleanup_html_file(ad_html_file)
        else:
            print(f"Skipping PDF conversion for AD Number {ad_number} due to missing content.")


if __name__ == "__main__":
    main()
