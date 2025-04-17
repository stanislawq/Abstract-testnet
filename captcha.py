import requests
from twocaptcha import TwoCaptcha

FAUCET_URL = 'https://faucet.triangleplatform.com/api/request'
SITEKEY_V2 = '6LfuM6giAAAAAOSzQAA57VwKBSEOgcRstYXUGqTa'
FAUCET_PAGE_URL = 'https://faucet.triangleplatform.com/abstract/testnet'
CAPTCHA_API_KEY = 'bd4d3ef0cd278588efb7e552c0a16336'

solver = TwoCaptcha(CAPTCHA_API_KEY)


def send_faucet_request(wallet_address, proxy, max_retries):
    captcha_proxy = proxy['https'][8:]
    try:
        print("Solving captcha...")
        token_v2 = solver.recaptcha(
            sitekey=SITEKEY_V2,
            url=FAUCET_PAGE_URL,
            proxy={'type': 'HTTPS', 'uri': captcha_proxy}
        )
        print("Captcha solved!")

        payload = {
            "address": wallet_address,
            "network": "abstract_testnet",
            "token_v2": token_v2['code']
        }

        retry = 0
        while retry < max_retries:
            try:
                response = requests.post(
                    url=FAUCET_URL,
                    json=payload,
                    proxies=proxy,
                    timeout=10,
                    verify=False
                )
                if 'explorer_url' in response.text:
                    print('Successfully funded 0.001 ETH!')
                    return True
                else:
                    print("Failed to fund. Response:", response.text)
                    return False
            except requests.exceptions.RequestException:
                print("Proxy failed")
            print('retrying...')
            retry += 1

        print('Max retries reached. Exiting.')
        return False
    except Exception as err:
        print('Captcha error', err)

