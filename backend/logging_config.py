import logging
import time
from flask import request, g

def setup_logging(app):
    """Sets up clean structured request logging for Flask."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger("taskmate.http")

    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        # Skip logging static asset requests if desired, or keep all
        if hasattr(g, "start_time"):
            duration = round((time.time() - g.start_time) * 1000, 2)
        else:
            duration = 0.0

        # Safe logging: only method, path, status, and duration
        # No request bodies or headers logged to prevent credential leakage
        logger.info(
            f"{request.method} {request.path} -> {response.status_code} ({duration}ms)"
        )
        return response

    return logger
