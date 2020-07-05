class Config:

    ext_path = "extension_6_2_3_0.crx"
    chrome_path = "chromedriver"
    pin_code = "10115"
    address_btn = "glow-ingress-line1"
    id_box = "GLUXZipUpdateInput"
    apply_btn = "GLUXZipUpdate"
    ok_btn = "a-autoid-3-announce"
    base_url = "https://www.amazon.de/"


class Development(Config):
    def __init__(self):
        pass


class Production(Config):
    def __init__(self):
        pass


config = {
    'branch': Development,
}
