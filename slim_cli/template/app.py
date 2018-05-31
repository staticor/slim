from slim import Application, CORSOptions
import config


app = Application(
    log_level=config.DEBUG,
    cookies_secret=config.COOKIE_SECRET,
    cors_options=CORSOptions('*', allow_credentials=True, expose_headers="*", allow_headers="*")
)
