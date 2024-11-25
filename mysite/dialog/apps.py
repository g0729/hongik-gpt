from django.apps import AppConfig
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os


class DialogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialog"

    def ready(self):
        from .corn import main

        main()
