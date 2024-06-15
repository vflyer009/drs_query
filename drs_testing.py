import db_query
import pdf_utils
import selenium_utils as sutils


DOWNLOAD_PATH = "/Users/josh.mac/Desktop/drs_test_data"
AD_PREFIX_STRING = "<p>"
PDF_OUTPUT_PATH = "/Users/josh.mac/Desktop/drs_test_data"


def main():
    make = "Beechcraft"
    model = "J35"

    db_results = db_query.lookup_ad(make, model) 

    if not db_results:
        print("No ADs found in Database")

    drs_request_url = sutils.build_drs_request_url(db_results[0][1])
    ad_content = sutils.download_ad_content(drs_request_url)
    ad_html_file = sutils.save_ad_content(ad_content, db_results[0][0], DOWNLOAD_PATH)

    pdf_utils.convert_html_to_pdf(ad_html_file, AD_PREFIX_STRING, DOWNLOAD_PATH)
    pdf_utils.cleanup_html_file(ad_html_file)


if __name__ == "__main__":
    main()