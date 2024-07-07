import csv_utils
import db_query
import pdf_utils
import selenium_utils as sutils
import oai_utils


DOWNLOAD_PATH = "/Users/josh.mac/Desktop/drs_test_data"
AD_PREFIX_STRING = "<p>"
PDF_OUTPUT_PATH = "/Users/josh.mac/Desktop/drs_test_data"


def main():
    make = "Beechcraft"
    model = "J35"
    set_limit = "1"


    db_results = db_query.lookup_ad(make, model, set_limit)
    print(db_results)

    if not db_results:
        print("No ADs found in Database")
        return

    for ad_number, unid in db_results:
        drs_request_url = sutils.build_drs_request_url(unid)
        ad_content = sutils.download_ad_content(drs_request_url)
        ad_html_file = sutils.save_ad_content(ad_content, ad_number, DOWNLOAD_PATH)

        if ad_html_file:
            temp_pdf_path = pdf_utils.convert_html_to_pdf(ad_html_file, AD_PREFIX_STRING, DOWNLOAD_PATH)
            pdf_utils.process_pdf(temp_pdf_path, f"{DOWNLOAD_PATH}/{ad_number}-processed.pdf")

            png_path = pdf_utils.pdf_to_png(f"{DOWNLOAD_PATH}/{ad_number}-processed.pdf", f"{DOWNLOAD_PATH}/{ad_number}.png")
            base64_string = pdf_utils.encode_image(png_path)

            oai_response = oai_utils.upload_base64_image(base64_string, make, model)
            oai_content = oai_response['choices'][0]['message']['content']

            csv_utils.save_table_to_csv(oai_content, F"{DOWNLOAD_PATH}/ad-results.csv")
        else:
            print(f"Skipping PDF conversion for AD Number {ad_number} due to missing content.")

if __name__ == "__main__":
    main()
