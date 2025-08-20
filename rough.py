import json
import urllib.parse

from playwright.sync_api import sync_playwright


def search_snomed_js(page, term: str):
    # Properly encode the term (e.g., spaces → %20)
    encoded_term = urllib.parse.quote(term)

    # Build the full JSONP URL
    jsonp_url = (
        f"https://nextgen.ehospital.gov.in/csnoserv/api/search/search?"
        f"term={encoded_term}&state=active&semantictag=disorder++finding"
        f"&acceptability=synonyms&returnlimit=3000&groupbyconcept=false"
        f"&refsetid=null&parentid=null&excludeparentconcept=false"
        f"&fullconcept=true&callback=__my_callback__"
    )

    # Inject script using JS inside the browser
    result = page.evaluate(f"""
        () => {{
            return new Promise((resolve, reject) => {{
                const script = document.createElement('script');
                script.src = "{jsonp_url}";

                window.__my_callback__ = (data) => {{
                    resolve(data);
                    delete window.__my_callback__;
                }};

                script.onerror = reject;
                document.body.appendChild(script);
            }});
        }}
    """)

    return result

with sync_playwright() as p :
    b  = p.chromium.launch(headless=True)
    context = b.new_context()
    pag = context.new_page()
    s = search_snomed_js(page=pag, term='femur neck')
    print(json.dumps(s, indent=2))
    print(len(s))